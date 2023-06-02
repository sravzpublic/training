package background

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/sravzpublic/training/training-go/pkg/config"
	"github.com/sravzpublic/training/training-go/pkg/crypto"
)

func GetTickers() {
	c := make(chan crypto.Crypto, len(crypto.Symbols))
	for _, v := range crypto.Symbols {
		go func(v string) {
			// log.Println("Processing symbol: ", v)
			response, err := http.Get(fmt.Sprintf("https://api.hitbtc.com/api/3/public/symbol/%s", v))

			if err != nil {
				fmt.Print(err.Error())
				os.Exit(1)
			}

			responseData, err := ioutil.ReadAll(response.Body)
			if err != nil {
				log.Fatal(err)
			}
			// fmt.Println(string(responseData))

			bytes := []byte(responseData)
			res := crypto.Crypto{DateTime: time.Now().String()}
			err = json.Unmarshal(bytes, &res)
			// crypto.Crypto.DateTime = time.Now().String()
			if err != nil {
				panic(err)
			}
			// log.Println("Sending to channel: ", res)
			c <- res
		}(v)
	}

	for _, v := range crypto.Symbols {
		res := <-c
		// log.Println("Received from channel: ", res)
		crypto.Cryptos[v] = res
	}
}

func Background() {
	// Set up cron job
	GetTickers()
	ticker := time.NewTicker(10 * time.Second)
	go func() {
		for range ticker.C {
			GetTickers()
		}
	}()

	// Sets up logger
	go func() {
		for message := range config.GetConfig().LogChannel {
			log.Println("Message in the logger", message)
		}
	}()

	// Stateful goroutine
	go func() {
		for {
			select {
			case msg := <-config.GetConfig().MiddleWareTracker:
				log.Println("MiddleWareTracker: ", msg)
			case msg := <-config.GetConfig().ContollerTracker:
				log.Println("ControllerTracker: ", msg)
			}
		}
	}()

}
