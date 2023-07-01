package options

type Option struct {
	ContractName         string  `json:"contractName"`
	ContractSize         string  `json:"contractSize"`
	ContractPeriod       string  `json:"contractPeriod"`
	Currency             string  `json:"currency"`
	Type                 string  `json:"type"`
	InTheMoney           string  `json:"inTheMoney"`
	LastTradeDateTime    string  `json:"lastTradeDateTime"`
	ExpirationDate       string  `json:"expirationDate"`
	Strike               float64 `json:"strike"`
	LastPrice            int     `json:"lastPrice"`
	Bid                  int     `json:"bid"`
	Ask                  float64 `json:"ask"`
	Change               int     `json:"change"`
	ChangePercent        int     `json:"changePercent"`
	Volume               int     `json:"volume"`
	OpenInterest         int     `json:"openInterest"`
	ImpliedVolatility    int     `json:"impliedVolatility"`
	Delta                int     `json:"delta"`
	Gamma                int     `json:"gamma"`
	Theta                int     `json:"theta"`
	Vega                 int     `json:"vega"`
	Rho                  int     `json:"rho"`
	Theoretical          int     `json:"theoretical"`
	IntrinsicValue       float64 `json:"intrinsicValue"`
	TimeValue            int     `json:"timeValue"`
	UpdatedAt            string  `json:"updatedAt"`
	DaysBeforeExpiration int     `json:"daysBeforeExpiration"`
}
