package middleware

import (
	"log"
	"net/http"
	"sync/atomic"

	"github.com/sravzpublic/training/training-go/pkg/config"
)

func LoggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Do stuff here
		log.Println("LoggingMiddleware", r.RequestURI)
		config.GetConfig().MiddleWareTracker <- "LoggingMiddleware called!"
		// Call the next handler, which can be another middleware in the chain, or the final handler.
		next.ServeHTTP(w, r)
	})
}

func RateLimitterMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Println("RateLimitterMiddleware")
		<-config.GetConfig().Limiter // Blocking call, blocks for every 1 ms
		config.GetConfig().MiddleWareTracker <- "RateLimitterMiddleware called!"
		next.ServeHTTP(w, r)
	})
}

func RequestNumberTracker(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		atomic.AddUint64(&config.GetConfig().NoRequests, 1)
		log.Println("RequestNumberTracker: No of requests", config.GetConfig().NoRequests)
		config.GetConfig().MiddleWareTracker <- "RequestNumberTracker called!"
		next.ServeHTTP(w, r)
	})
}

func RequestNumberTrackerByUrl(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		config.GetConfig().MiddleWareTracker <- "RequestNumberTrackerByUrl called!"
		go func(uri string) {
			config.GetConfig().Mutex.Lock()
			config.GetConfig().NoRequestsByUrlCounters[uri]++
			log.Println("RequestNumberTrackerByUrl: ", " URI:", uri, " No of requests", config.GetConfig().NoRequestsByUrlCounters[uri])
			defer config.GetConfig().Mutex.Unlock()
		}(r.RequestURI)
		next.ServeHTTP(w, r)
	})
}
