// References
// https://github.com/webdeveloppro/golang-websocket-client
// https://webdevelop.pro/blog/guide-creating-websocket-client-golang-using-mutex-and-channel
// https://eodhd.com/financial-apis/new-real-time-data-api-websockets/

package jobs

import (
	"context"
	"encoding/json"
	"fmt"
	"net/url"
	"os"
	"os/signal"
	"strings"
	"sync"
	"syscall"
	"time"

	redistimeseries "github.com/RedisTimeSeries/redistimeseries-go"
	"github.com/go-co-op/gocron"
	"github.com/go-redis/redis"
	"github.com/gorilla/websocket"
	log "github.com/sirupsen/logrus"
)

// Send pings to peer with this period
const pingPeriod = 60 * time.Second
const quoteRefreshToRedisDelayMilliSeconds = 1000 // Delay quote refresh to redis by 1 second
const USTradeClientType = "us-quotes"
const CryptoClientType = "crypto"
const USQuotesClient = "us"
const USTradeClientTypeInitial = "us-quotes" // TODO: Fix initial
const CryptoClientTypeInitial = "c"
const USQuotesClientInitial = "u"

// {"action": "subscribe", "symbols": "ETH-USD,BTC-USD"}
// Used to make call to the websocket
type Request struct {
	Action  string `json:"action"`
	Symbols string `json:"symbols"`
}

// Go redis will use this method to convert the struct to json
func (r RealTimeQuote) MarshalBinary() ([]byte, error) {
	return json.Marshal(r)
}

type RealTimeCryptoQuote struct {
	Ty   string  `json:"ty"`
	S    string  `json:"s"`
	P    float64 `json:"p,string"`
	Q    float64 `json:"q,string"`
	A    float64 `json:"a"`
	B    float64 `json:"b"`
	Ap   float64 `json:"ap"`
	Bp   float64 `json:"bp"`
	As   float64 `json:"as"`
	Bs   float64 `json:"bs"`
	Dc   string  `json:"dc"`
	Dd   string  `json:"dd"`
	Ppms bool    `json:"ppms"`
	T    int64   `json:"t"`
}

type RealTimeQuote struct {
	Ty   string  `json:"ty"`
	S    string  `json:"s"`
	P    float64 `json:"p"`
	V    float64 `json:"v"`
	Q    float64 `json:"q"`
	A    float64 `json:"a"`
	B    float64 `json:"b"`
	Ap   float64 `json:"ap"`
	Bp   float64 `json:"bp"`
	As   float64 `json:"as"`
	Bs   float64 `json:"bs"`
	Dc   string  `json:"dc"`
	Dd   string  `json:"dd"`
	Ppms bool    `json:"ppms"`
	T    int64   `json:"t"`
}

// WebSocketClient return websocket client connection
type WebSocketClient struct {
	configStr string
	sendBuf   chan []byte
	ctx       context.Context
	ctxCancel context.CancelFunc

	mu                    sync.RWMutex
	wsconn                *websocket.Conn
	redisClient           *redis.Client
	redisTimeSeriesClient *redistimeseries.Client
	fullClientType        string
	clientType            string
	tickerLastUpdated     map[string]RealTimeQuote
	initialRequest        Request
	sendInitialRequest    bool
	goCron                *gocron.Scheduler
}

// NewWebSocketClient create new websocket connection
func NewWebSocketClient(clientType string, url url.URL) (*WebSocketClient, error) {
	conn := WebSocketClient{
		fullClientType:    clientType,
		clientType:        clientType[0:1],
		sendBuf:           make(chan []byte, 1),
		tickerLastUpdated: make(map[string]RealTimeQuote),
		goCron:            gocron.NewScheduler(time.UTC),
	}
	conn.ctx, conn.ctxCancel = context.WithCancel(context.Background())
	// u := url.URL{Scheme: "wss", Host: host, Path: channel}
	conn.configStr = url.String()
	conn.log("NewWebSocketClient", nil, "Connecting to redis at: redis:6379")
	conn.goCron.Every("1m").Do(conn.pingRedis)
	conn.redisClient = redis.NewClient(&redis.Options{
		Addr:     "redis:6379",
		Password: "password",
		DB:       0,
	})
	password := "password"
	conn.redisTimeSeriesClient = redistimeseries.NewClient("redis:6379", "nohelp", &password)
	// Listen on the websocket and write the quotes to redis
	go conn.listen()
	// List of sendBuf channel and write to the websocket
	go conn.listenWrite()
	// Run ping pong look on the redis connection
	go conn.ping()
	conn.goCron.StartAsync()
	return &conn, nil
}

// https://redis.io/commands/ping/
func (conn *WebSocketClient) pingRedis() {
	_, err := conn.redisClient.Ping().Result()
	if err != nil {
		log.Error("Redis ping unsuccessful: ", err)
	}
}

// Connect to websocket, retry every 1 sec if connection failed.
func (conn *WebSocketClient) Connect() *websocket.Conn {
	conn.mu.Lock()
	defer conn.mu.Unlock()
	if conn.wsconn != nil {
		return conn.wsconn
	}

	ticker := time.NewTicker(time.Second)
	defer ticker.Stop()
	for ; ; <-ticker.C {
		select {
		case <-conn.ctx.Done():
			return nil
		default:
			ws, _, err := websocket.DefaultDialer.Dial(conn.configStr, nil)
			if err != nil {
				conn.log("connect", err, fmt.Sprintf("Cannot connect to websocket: %s", conn.configStr))
				continue
			}
			conn.log("connect", nil, fmt.Sprintf("connected to websocket to %s", conn.configStr))
			conn.wsconn = ws
			return conn.wsconn
		}
	}
}

// Listen to the messages on the websocket and write the quotes to redis
func (conn *WebSocketClient) listen() {
	conn.log("listen", nil, fmt.Sprintf("listen for the messages: %s", conn.configStr))
	ticker := time.NewTicker(time.Second)

	defer ticker.Stop()
	for {
		select {
		case <-conn.ctx.Done():
			return
		case <-ticker.C:
			for {
				ws := conn.Connect()
				if ws == nil {
					return
				}
				if conn.sendInitialRequest {
					conn.log("listen", nil, fmt.Sprintf("Sending initial request: %s", conn.initialRequest))
					err := conn.Write(conn.initialRequest)
					if err != nil {
						log.Info("write:", err)
						return
					}
					conn.sendInitialRequest = false
				}
				_, bytMsg, err := ws.ReadMessage()
				if err != nil {
					conn.log("listen", err, "Cannot read websocket message: "+conn.fullClientType)
					conn.closeWs()
					conn.sendInitialRequest = true
					break
				}
				conn.log("listen", nil, fmt.Sprintf("websocket msg: %s\n", string(bytMsg)))
				conn.writeQuoteToRedis(nil, bytMsg)
			}
		}
	}
}

// Write data to conn.sendBuf channel
func (conn *WebSocketClient) Write(payload interface{}) error {
	data, err := json.Marshal(payload)
	if err != nil {
		return err
	}
	ctx, cancel := context.WithTimeout(context.Background(), time.Millisecond*50)
	defer cancel()

	for {
		select {
		case conn.sendBuf <- data:
			return nil
		case <-ctx.Done():
			return fmt.Errorf("context canceled")
		}
	}
}

// Read data from conn.sendBuf channel and write to the websocket
func (conn *WebSocketClient) listenWrite() {
	for data := range conn.sendBuf {
		ws := conn.Connect()
		if ws == nil {
			err := fmt.Errorf("conn.ws is nil")
			conn.log("listenWrite", err, "No websocket connection")
			continue
		}

		if err := ws.WriteMessage(
			websocket.TextMessage,
			data,
		); err != nil {
			conn.log("listenWrite", nil, "WebSocket Write Error")
		}
		conn.log("listenWrite", nil, fmt.Sprintf("send: %s", data))
		conn.writeQuoteToRedis(nil, data)
	}
}

// Close will send close message and shutdown websocket connection
func (conn *WebSocketClient) Stop() {
	conn.ctxCancel()
	conn.closeWs()
	conn.redisClient.Close()
}

// Close will send close message and shutdown websocket connection
func (conn *WebSocketClient) closeWs() {
	conn.mu.Lock()
	if conn.wsconn != nil {
		conn.wsconn.WriteMessage(websocket.CloseMessage, websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""))
		conn.wsconn.Close()
		conn.wsconn = nil
	}
	conn.mu.Unlock()
}

// Keep the connection alive, by pinging redis
func (conn *WebSocketClient) ping() {
	conn.log("ping", nil, "ping pong started")
	ticker := time.NewTicker(pingPeriod)
	defer ticker.Stop()
	for {
		select {
		case <-ticker.C:
			ws := conn.Connect()
			if ws == nil {
				continue
			}
			if err := conn.wsconn.WriteControl(websocket.PingMessage, []byte{}, time.Now().Add(pingPeriod/2)); err != nil {
				conn.closeWs()
			}
		case <-conn.ctx.Done():
			return
		}
	}
}

// Log function
func (conn *WebSocketClient) log(f string, err error, msg string) {
	if err != nil {
		log.Errorf("Error in func: %s, err: %v, msg: %s\n", f, err, msg)
	} else {
		log.Debugf("Log in func: %s, %s\n", f, msg)
	}
}

// Writes quotes to redis
func (conn *WebSocketClient) writeQuoteToRedis(err error, msg []byte) {
	if err != nil {
		log.Errorf("Error in func: err: %v, msg: %s\n", err, msg)
	} else {
		// log.Printf("Log in writeQuoteToRedis: %s\n", msg)
		var realTimeQuote RealTimeQuote
		if conn.clientType == CryptoClientTypeInitial {
			var realTimeCryptoQuote RealTimeCryptoQuote
			err = json.Unmarshal(msg, &realTimeCryptoQuote)
			realTimeQuote.Ty = conn.clientType
			realTimeQuote.Ap = realTimeCryptoQuote.P
			realTimeQuote.Bp = realTimeCryptoQuote.P
			realTimeQuote.P = realTimeCryptoQuote.P
			realTimeQuote.Q = realTimeCryptoQuote.Q
			realTimeQuote.S = realTimeCryptoQuote.S
			realTimeQuote.Dc = realTimeCryptoQuote.Dc
			realTimeQuote.Dd = realTimeCryptoQuote.Dd
			realTimeQuote.Ppms = realTimeCryptoQuote.Ppms
			realTimeQuote.T = realTimeCryptoQuote.T
		} else {
			err = json.Unmarshal(msg, &realTimeQuote)
			realTimeQuote.Ty = conn.clientType

			// us-stock quotes
			if conn.clientType == USQuotesClientInitial {
				realTimeQuote.Q = realTimeQuote.V                               //(realTimeQuote.Ap + realTimeQuote.Bp)/2
				realTimeQuote.Dd = fmt.Sprintf("%f", (realTimeQuote.P - 0))     // quote.Change
				realTimeQuote.Dc = fmt.Sprintf("%f", (realTimeQuote.P-0)/(100)) // quote.ChangeP
			}
		}

		if err != nil {
			log.Error(err)
		}

		// If this is no quote message - For eg: connection success etc skip...
		if realTimeQuote.T == 0 {
			return
		}

		if val, ok := conn.tickerLastUpdated[realTimeQuote.S]; ok {
			// If quote is within quoteRefreshToRedisDelayMilliSeconds period
			// or quote price is same as previous quote price
			// do not send an update
			// Index quotes are very late, so just display always
			if realTimeQuote.T-val.T < quoteRefreshToRedisDelayMilliSeconds {
				return
			}
		}

		conn.tickerLastUpdated[realTimeQuote.S] = realTimeQuote
		if err := conn.redisClient.Publish("realtime-quotes", realTimeQuote).Err(); err != nil {
			log.Error(err)
		} else {
			log.Debugf("Quote sent on redis, msg: %s\n", msg)
		}

		// Add quote to timeseries
		_, err := conn.redisTimeSeriesClient.Add(realTimeQuote.S, realTimeQuote.T, realTimeQuote.P)
		if err != nil {
			log.Error("Error:", err)
		} else {
			log.Debugf("TS.ADD - %v\n", realTimeQuote)
		}
	}
}

// Start the websocket client
func startClient(clientType string, request Request) *WebSocketClient {
	baseURL := fmt.Sprintf("ws.eodhistoricaldata.com/ws/%s", clientType)
	eodURL, err := url.Parse(baseURL)
	eodURL.Scheme = "wss"
	eodParms := url.Values{}
	eodParms.Add("api_token", "demo")
	eodURL.RawQuery = eodParms.Encode()
	if err != nil {
		log.Fatal(err)
	}
	// log.Printf("connecting to %s", eodURL.String())
	client, err := NewWebSocketClient(clientType, *eodURL)
	if err != nil {
		panic(err)
	} else {
		log.Info("Connected to websocket endpoint: " + clientType)
	}

	requestJSON, err := json.Marshal(request)
	if err != nil {
		log.Fatal(err)
	}
	log.Info("Sending message:", string(requestJSON[:]))
	client.initialRequest = request
	err = client.Write(client.initialRequest)
	if err != nil {
		log.Error("write:", err)
		return nil
	}

	// Create redis keys
	// If the key is not present create it, else update it.
	rules := map[string]uint{
		"1m_avg":  60000,
		"5m_avg":  60000 * 5,
		"10m_avg": 60000 * 10,
		"15m_avg": 60000 * 15,
		"30m_avg": 60000 * 30,
		"1h_avg":  60000 * 60,
		"1d_avg":  60000 * 60 * 24,
	}

	for _, key := range strings.Split(request.Symbols, ",") {
		labels := map[string]string{
			"asset_type": client.fullClientType,
			"asset":      key,
		}
		key = strings.TrimSpace(key)
		keys := []string{key}
		for rule := range rules {
			keys = append(keys, key+"_"+rule)
		}
		for _, keyname := range keys {
			_, haveit := client.redisTimeSeriesClient.Info(keyname)
			retention, _ := time.ParseDuration("720h0m0s") // 30 days
			if haveit != nil {
				// Retain for a Month
				client.redisTimeSeriesClient.CreateKeyWithOptions(keyname, redistimeseries.CreateOptions{DuplicatePolicy: redistimeseries.LastDuplicatePolicy, RetentionMSecs: retention, Labels: labels})
			} else {
				client.redisTimeSeriesClient.AlterKeyWithOptions(keyname, redistimeseries.CreateOptions{DuplicatePolicy: redistimeseries.LastDuplicatePolicy, RetentionMSecs: retention, Labels: labels})
			}
		}
		// Create the rules
		for rule := range rules {
			client.redisTimeSeriesClient.CreateRule(key, redistimeseries.AvgAggregation, rules[rule], key+"_"+rule)
		}

	}
	return client
}

func ClientNew() {
	var cryptoClient *WebSocketClient
	var stockClient *WebSocketClient
	var stockTradeClient *WebSocketClient
	var redisClient *redis.Client
	goCron := gocron.NewScheduler(time.UTC)

	// Start redis client
	redisClient = redis.NewClient(&redis.Options{
		Addr:     "redis:6379",
		Password: "password",
		DB:       0,
	})

	// Start redis ping
	goCron.Every("1m").Do(func() {
		_, err := redisClient.Ping().Result()
		if err != nil {
			log.Info("Redis ping unsuccessful: ", err)
		}
	})

	// wss://ws.eodhistoricaldata.com/ws/us-quote?api_token=XXX
	USQuotesSymbols := "AAPL,MSFT,TSLA"
	if USQuotesSymbols != "" {
		log.Info("US Trade client started: ", USQuotesSymbols)
	} else {
		log.Info("US Quotes client not enabled")
	}

	CryptoSymbols := "ETH-USD,BTC-USD"
	if CryptoSymbols != "" {
		log.Info("Crypto client started: ", CryptoSymbols)
		cryptoClient = startClient(CryptoClientType, Request{Action: "subscribe", Symbols: CryptoSymbols})
	} else {
		log.Info("Crypto client not enabled")
	}

	// Start cron
	goCron.StartAsync()

	// Close connection correctly on exit
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	// The program will wait here until it gets the
	<-sigs
	if CryptoSymbols != "" {
		cryptoClient.Stop()
	}
	if USQuotesSymbols != "" {
		stockClient.Stop()
		stockTradeClient.Stop()
	}

	goCron.Stop()
	redisClient.Close()

	log.Info("Goodbye")
}
