package config

import (
	"sync"

	"github.com/gorilla/mux"
)

type Config struct {
	LogChannel chan string
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
		singleton = &Config{LogChannel: make(chan string, 100)}
	})
	return singleton
}
