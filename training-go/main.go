package main

import (
	"context"
	"flag"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strings"
	"time"
	"training-go/pkg/background"
	"training-go/pkg/config"
	"training-go/pkg/crypto"
	"training-go/pkg/db"

	"github.com/gorilla/mux"
)

func main() {
	var wait time.Duration
	var symbols string
	flag.DurationVar(&wait, "graceful-timeout", time.Second*15, "the duration for which the server gracefully wait for existing connections to finish - e.g. 15s or 1m")
	flag.StringVar(&symbols, "symbols", "ETHBTC,BTCUSDC", "Comma separted symbols list")
	flag.Parse()

	crypto.Cryptos = make(map[string]crypto.Crypto)
	crypto.Symbols = strings.Split(symbols, ",") // []string{"ETHBTC", "BTCUSDC"}

	r := mux.NewRouter()
	r.HandleFunc("/currency/{symbol}", crypto.GetCrypto).Methods("GET")
	r.HandleFunc("/db/", db.GetData).Methods("GET")
	config.AppInstance.Router = r

	srv := &http.Server{
		Addr:         "0.0.0.0:8081",
		WriteTimeout: time.Second * 15,
		ReadTimeout:  time.Second * 15,
		IdleTimeout:  time.Second * 60,
		Handler:      r, // Pass our instance of gorilla/mux in.
	}

	// Run our server in a goroutine so that it doesn't block.
	go func() {
		log.Println("Server listening at localhost:8081")
		if err := srv.ListenAndServe(); err != nil {
			log.Println(err)
		}
	}()

	// Set up cron job
	background.Background()

	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)
	<-c
	ctx, cancel := context.WithTimeout(context.Background(), wait)
	defer cancel()
	srv.Shutdown(ctx)
	log.Println("shutting down")
	os.Exit(0)
}
