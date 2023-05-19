package config

import (
	"sync"
)

type Config struct {
	LogChannel chan string
}

var singleton *Config
var once sync.Once

func GetConfig() *Config {
	once.Do(func() {
		singleton = &Config{LogChannel: make(chan string, 100)}
	})
	return singleton
}
