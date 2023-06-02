package config

import (
	"sync"
	"time"

	"github.com/gorilla/mux"
)

type Config struct {
	LogChannel              chan string
	Limiter                 chan time.Time
	NoRequests              uint64
	Mutex                   sync.Mutex
	NoRequestsByUrlCounters map[string]int
	MiddleWareTracker       chan string
	ContollerTracker        chan string
}

// Need for testing
type App struct {
	Router *mux.Router
}

var singleton *Config
var once sync.Once
var AppInstance App

func GetConfig() *Config {
	once.Do(func() {
		singleton = &Config{
			LogChannel:        make(chan string, 100),
			Limiter:           make(chan time.Time, 100),
			MiddleWareTracker: make(chan string, 10),
			ContollerTracker:  make(chan string, 10),
		}
	})
	return singleton
}
