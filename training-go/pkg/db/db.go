package db

import (
	"encoding/json"
	"log"
	"net/http"
	"sync"
)

type DBData struct {
	Table1 string `json:"table1"`
	Table2 string `json:"table2"`
	Table3 string `json:"table3"`
}

func GetData(w http.ResponseWriter, r *http.Request) {
	var wg sync.WaitGroup
	var dbData DBData
	for i := 1; i <= 3; i++ {
		wg.Add(1)
		i := i
		go func() {
			defer wg.Done()
			if i == 1 {
				dbData.Table1 = "Table1 Data Filled"
			}
			if i == 2 {
				dbData.Table2 = "Table2 Data Filled"
			}
			if i == 3 {
				dbData.Table3 = "Table3 Data Filled"
			}
		}()
	}
	wg.Wait()
	log.Println("Returing in dbData: ", dbData)
	json.NewEncoder(w).Encode(dbData)

}

func IntMin(a, b int) int {
	if a < b {
		return a
	}
	return b
}
