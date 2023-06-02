package futures

import (
	"fmt"
	"strings"

	"github.com/gocarina/gocsv"
)

var TESTDATA = `Contract,Name,Settlement_Date,Price,Time,Change,Pct_Change
CLN23.NYM,Crude Oil,Jul 23,68.84,11:04AM EDT,-0.62,-0.89%
CLQ23.NYM,Crude Oil,Aug 23,68.97,11:03AM EDT,-0.63,-0.91%
CLX23.NYM,Crude Oil,Nov 23,68.36,11:02AM EDT,-0.58,-0.84%
CLU23.NYM,Crude Oil,Sep 23,68.88,11:04AM EDT,-0.60,-0.86%`

type FuturesChainType interface {
	GetSettlementDate() string
}

type FutureChain struct {
	Contract        string `csv:"Contract"`
	Name            string `csv:"client_name"`
	Settlement_Date string `csv:"Settlement_Date"`
	Price           string `csv:"Price"`
	Time            string `csv:"Time"`
	Change          string `csv:"Change"`
	Pct_Change      string `csv:"Pct_Change"`
}

func (fc FutureChain) GetSettlementDate() string {
	return fc.Settlement_Date
}

var FuturesChain []FutureChain

// Templated function
func Compare[T FuturesChainType](a T, b T) int {
	if a.GetSettlementDate() > b.GetSettlementDate() {
		return 1
	}
	if a.GetSettlementDate() < b.GetSettlementDate() {
		return -1
	}
	return 0
}

func PrintFutures[T []FutureChain](futuresChain T) {
	fmt.Println("Futures Chain", futuresChain)
}

// Called only once when the package is loaded
func init() {
	in := strings.NewReader(TESTDATA)
	gocsv.Unmarshal(in, &FuturesChain)
}
