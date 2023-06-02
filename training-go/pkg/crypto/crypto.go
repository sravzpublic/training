package crypto

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/sravzpublic/training/training-go/pkg/config"
)

type InsturmentSettlementType struct {
	Type string
}

type Instrument interface {
	GetSettlementType() string
	GetType() string
}

type Crypto struct {
	InsturmentSettlementType
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

func (c *Crypto) GetType() string {
	return c.Type
}

func (c *Crypto) GetSettlementType() string {
	return c.InsturmentSettlementType.Type
}

type Future struct {
	InsturmentSettlementType
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

func (f *Future) GetType() string {
	return f.Type
}

func (f *Future) GetSettlementType() string {
	return f.InsturmentSettlementType.Type
}

// Cryptos var as a slice Crypto struct
var Cryptos map[string]Crypto
var Symbols []string

// GetCrypto gets a Crypto
func GetCrypto(w http.ResponseWriter, r *http.Request) {
	// Log request
	config.GetConfig().LogChannel <- "Request received"
	config.GetConfig().ContollerTracker <- "CryptoContoller called!!!"
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
