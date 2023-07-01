# Sravz Golang Crash Course

### References:
https://gobyexample.com/
https://semaphoreci.com/community/tutorials/building-and-testing-a-rest-api-in-go-with-gorilla-mux-and-postgresql
https://github.com/gorilla/mux

### Set up
```
$ go version
go version go1.16.4 darwin/amd64

# Go mod tidy and vendor
go mod tidy
go mod vendor
```

### Install Air. Air allows live reload of golang code
```
f119f4c1ff41:/workspace/training-go# go install github.com/cosmtrek/air@latest
go: downloading github.com/cosmtrek/air v1.43.0
...
go: downloading google.golang.org/protobuf v1.28.1

f119f4c1ff41:/workspace/training-go# air

  __    _   ___  
 / /\  | | | |_) 
/_/--\ |_| |_| \_ , built with Go 

watching .
!exclude tmp
!exclude vendor
building...
running...
2023/05/17 18:25:05 Server listening at localhost:8081
```

### Run
```
$ make run
go build
./toy_poc
2023/05/04 16:29:45 Server listening at localhost:8080
2023/05/04 16:29:49 Processing symbol:  ETHBTC
{"type":"spot","base_currency":"ETH","quote_currency":"BTC","status":"working","quantity_increment":"0.0001","tick_size":"0.000001","take_rate":"0.0025","make_rate":"0.001","fee_currency":"BTC","margin_trading":true,"max_initial_leverage":"10.00"}
Update quote for:  BTC
2023/05/04 16:29:49 Processing symbol:  BTCUSDC
{"type":"spot","base_currency":"BTC","quote_currency":"USDC","status":"working","quantity_increment":"0.00001","tick_size":"0.00001","take_rate":"0.0025","make_rate":"0.001","fee_currency":"USDC","margin_trading":true,"max_initial_leverage":"10.00"}
Update quote for:  USDC
```

### Test
```
# Get all symbols
$ curl localhost:8080/currency/all
[{"type":"spot","base_currency":"ETH","quote_currency":"BTC","status":"working","quantity_increment":"0.0001","tick_size":"0.000001","take_rate":"0.0025","make_rate":"0.001","fee_currency":"BTC","margin_trading":true,"max_initial_leverage":"10.00"},{"type":"spot","base_currency":"BTC","quote_currency":"USDC","status":"working","quantity_increment":"0.00001","tick_size":"0.00001","take_rate":"0.0025","make_rate":"0.001","fee_currency":"USDC","margin_trading":true,"max_initial_leverage":"10.00"}]

# Get a specific symbol
$curl localhost:8080/currency/BTCUSDC
{"type":"spot","base_currency":"BTC","quote_currency":"USDC","status":"working","quantity_increment":"0.00001","tick_size":"0.00001","take_rate":"0.0025","make_rate":"0.001","fee_currency":"USDC","margin_trading":true,"max_initial_leverage":"10.00"}

# Get a specific symbol
sampats-mbp-2:toy_poc fd98279$ curl localhost:8080/currency/ETHBTC
{"type":"spot","base_currency":"ETH","quote_currency":"BTC","status":"working","quantity_increment":"0.0001","tick_size":"0.000001","take_rate":"0.0025","make_rate":"0.001","fee_currency":"BTC","margin_trading":true,"max_initial_leverage":"10.00"}
sampats-mbp-2:toy_poc fd98279$

# Get invalid symbol
$ curl localhost:8080/currency/TEST
"Unsupported symbol: Supported Systems: [ETHBTC BTCUSDC]"
```

### Get invalid symbol
```bash
$ curl localhost:8080/currency/TEST
"Unsupported symbol: Supported Systems: [ETHBTC BTCUSDC]"
```

## MongodDB
#### After adding mongo dependency run go mod tidy and go mod vendor
```bash
6488fc3b02ce:/workspace/training-go# go mod tidy
...
go: downloading github.com/xdg-go/pbkdf2 v1.0.0
6488fc3b02ce:/workspace/training-go# go mod vendor
6488fc3b02ce:/workspace/training-go# 
```