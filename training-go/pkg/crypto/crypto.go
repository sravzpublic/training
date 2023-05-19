package crypto

import (
	"encoding/json"
	"fmt"
	"net/http"
	"training-go/pkg/config"

	"github.com/gorilla/mux"
)

type Crypto struct {
	Type               string `json:"type"`
	BaseCurrency       string `json:"base_currency"`
	QuoteCurrency      string `json:"quote_currency"`
	Status             string `json:"status"`
	QuantityIncrement  string `json:"quantity_increment"`
	TickSize           string `json:"tick_size"`
	TakeRate           string `json:"take_rate"`
	MakeRate           string `json:"make_rate"`
	FeeCurrency        string `json:"fee_currency"`
	MarginTrading      bool   `json:"margin_trading"`
	MaxInitialLeverage string `json:"max_initial_leverage"`
	DateTime           string `json:"datetime"`
}

// Cryptos var as a slice Crypto struct
var Cryptos map[string]Crypto
var Symbols []string

// GetCrypto gets a Crypto
func GetCrypto(w http.ResponseWriter, r *http.Request) {
	// Log request
	config.GetConfig().LogChannel <- "Request received"

	// https://api.hitbtc.com/api/3/public/symbol/BTCUSDC
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r) // Gets params

	if params["symbol"] == "all" {
		v := make([]Crypto, 0, len(Cryptos))

		for _, value := range Cryptos {
			v = append(v, value)
		}

		json.NewEncoder(w).Encode(v)
		return
	}

	for key, item := range Cryptos {
		if key == params["symbol"] {
			json.NewEncoder(w).Encode(item)
			return
		}
	}
	json.NewEncoder(w).Encode(fmt.Sprintf("Unsupported symbol: Supported Systems: %v", Symbols))
}