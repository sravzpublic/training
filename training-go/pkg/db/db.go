package db

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"sync"
	"time"

	"github.com/sravzpublic/training/training-go/pkg/config"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/mongo/readpref"
)

type DBData struct {
	Table1 string `json:"table1"`
	Table2 string `json:"table2"`
	Table3 string `json:"table3"`
}

func GetData(w http.ResponseWriter, r *http.Request) {
	config.GetConfig().ContollerTracker <- "DBContoller called!!!"
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

func init() {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	client, err := mongo.Connect(ctx, options.Client().ApplyURI("mongodb://sravz:sravz@mongo:27017/sravz"))
	if err != nil {
		log.Println("Cannot connect to mongodb at mongodb://sravz:sravz@mongo:27017/sravz")
	}
	_ = client.Ping(ctx, readpref.Primary())
	log.Println("Pinged MongoDB")
	defer func() {
		if err = client.Disconnect(ctx); err != nil {
			panic(err)
		}
	}()
	collection := client.Database("testing").Collection("numbers")
	ctx, cancel = context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	res, err := collection.InsertOne(ctx, bson.D{{Key: "name", Value: "pi"},
		{Key: "value", Value: 3.14159}})
	if err == nil {
		id := res.InsertedID
		log.Println("Inserted document ID", id)
	}

}
