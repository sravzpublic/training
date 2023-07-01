package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"sort"
	"strings"
	"time"

	"github.com/gorilla/mux"
	"github.com/sravzpublic/training/training-go/pkg/asset"
	"github.com/sravzpublic/training/training-go/pkg/background"
	"github.com/sravzpublic/training/training-go/pkg/collections"
	"github.com/sravzpublic/training/training-go/pkg/config"
	"github.com/sravzpublic/training/training-go/pkg/crypto"
	"github.com/sravzpublic/training/training-go/pkg/db"
	"github.com/sravzpublic/training/training-go/pkg/futures"
	"github.com/sravzpublic/training/training-go/pkg/middleware"
	"github.com/sravzpublic/training/training-go/pkg/util"
)

func main() {
	var wait time.Duration
	var symbols string
	flag.DurationVar(&wait, "graceful-timeout", time.Second*15, "the duration for which the server gracefully wait for existing connections to finish - e.g. 15s or 1m")
	flag.StringVar(&symbols, "symbols", "BTCUSDC,ETHBTC", "Comma separted symbols list")
	flag.Parse()

	crypto.Cryptos = make(map[string]crypto.Crypto)
	crypto.Symbols = strings.Split(symbols, ",") // []string{"ETHBTC", "BTCUSDC"}
	sort.Sort(util.StringSlice(crypto.Symbols))
	log.Println("Crypto symbols after sort", crypto.Symbols)

	r := mux.NewRouter()
	r.HandleFunc("/currency/{symbol}", crypto.GetCrypto).Methods("GET")
	r.HandleFunc("/db/", db.GetData).Methods("GET")
	config.AppInstance.Router = r
	config.GetConfig().NoRequestsByUrlCounters = make(map[string]int)
	r.Use(middleware.RateLimitterMiddleware)
	r.Use(middleware.LoggingMiddleware)
	r.Use(middleware.RequestNumberTracker)
	r.Use(middleware.RequestNumberTrackerByUrl)
	// Set rate limier
	go func() {
		for t := range time.Tick(1 * time.Millisecond) {
			config.GetConfig().Limiter <- t
		}
	}()

	srv := &http.Server{
		Addr:         "0.0.0.0:80",
		WriteTimeout: time.Second * 15,
		ReadTimeout:  time.Second * 15,
		IdleTimeout:  time.Second * 60,
		Handler:      r, // Pass our instance of gorilla/mux in.
	}

	// Run our server in a goroutine so that it doesn't block.
	go func() {
		log.Println("Server listening at localhost:80")
		if err := srv.ListenAndServe(); err != nil {
			log.Println(err)
		}
	}()

	// Set up cron job
	background.Background()

	// Usage of interface and struct
	var instruments = [...]crypto.Instrument{
		&crypto.Crypto{Type: "Crypto", InsturmentSettlementType: crypto.InsturmentSettlementType{
			Type: "Cash",
		}},
		&crypto.Future{Type: "Future",
			InsturmentSettlementType: crypto.InsturmentSettlementType{
				Type: "Physical",
			},
		}}
	for _, i := range instruments {
		log.Println("This is the instrument ID: ", i.GetType(), " Settlement type: ", i.GetSettlementType())
	}

	// Usage of struct - create a linked list
	collections.Collection()

	// Generics Usage
	asset.Print(1)
	asset.Print(1.0)
	futures.PrintFutures(futures.FuturesChain)
	// Usage of compare function
	fmt.Println("Comparing two futures", futures.Compare(futures.FuturesChain[0], futures.FuturesChain[1]))

	// Context usage
	c := make(chan os.Signal, 1)
	// ctrl + c = sigint
	signal.Notify(c, os.Interrupt)
	<-c
	ctx, cancel := context.WithTimeout(context.Background(), wait)
	srv.Shutdown(ctx)
	log.Println("shutting down")

	defer cancel()
	os.Exit(0)

}
