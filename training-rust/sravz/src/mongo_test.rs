use crate::{mongo, models::Message};
use mongodb::Client;
use tokio::test;

// src/lib.rs
#[tokio::test]
async fn test_mongo_create() {
    let client = Client::with_uri_str("mongodb://sravz:sravz@mongo:27017/sravz").await
    .expect("Unable to connect to MongoDB");  
    // Utc.ymd(2020, 2, 7).and_hms(0, 0, 0)
    // "date" : "2023-10-27T15:45:00Z",
    let json_str = r#"{
        "id" : 21.1,
        "p_i" : {
            "args" : [
                "idx_us_ndx"
            ],
            "kwargs" : {
                "device" : "mobile",
                "upload_to_aws" : true
            }
        },
        "t_o" : "production_backend-node8c6b43063463",
        "cid" : "VTTT7Qu_jaQn-IhAAAGP",
        "cache_message" : true,
        "stopic" : "pca",
        "ts" : 1698155232.5238342,
        "fun_n" : "get_correlation_analysis_tear_sheet_user_asset",
        "e" : "Error",
        "key" : "8631c843c43d7d746de2b80ca4db2cdc",
        "exception_message" : "Traceback (most recent call last):\n  File \"/home/airflow/src/services/kafka_helpers/message_contracts.py\", line 381, in get_output_message\n    data = MessageContracts.MESSAGEID_FUNCTION_MAP.get(\n  File \"/home/airflow/.local/lib/python3.8/site-packages/decorator.py\", line 232, in fun\n    return caller(func, *(extras + args), **kw)\n  File \"/home/airflow/src/util/helper.py\", line 187, in save_data_to_contabo\n    args_,kwargs = func(*args, **kwargs)\n  File \"/home/airflow/src/analytics/portfolio.py\", line 361, in get_correlation_analysis_tear_sheet_user_asset\n    df = pe.get_df_from_s3(sravz_id)\n  File \"/home/airflow/src/services/price_queries.py\", line 149, in get_df_from_s3\n    data_df = pd.read_csv(io.BytesIO(historical_price))\nTypeError: a bytes-like object is required, not 'list'\n"
    }"#;
    let result: Result<Message, serde_json::Error> = serde_json::from_str(json_str);        
    // Handle the result using pattern matching
    match result {
        Ok(_message) => {
            mongo::create(_message, &client).await;
        }
        Err(err) => {
            eprintln!("Deserialization failed: {}", err);
        }
    }    
}

#[tokio::test]
async fn test_mongo_find() {
    let client = Client::with_uri_str("mongodb://sravz:sravz@mongo:27017/sravz").await
    .expect("Unable to connect to MongoDB");  
    // Utc.ymd(2020, 2, 7).and_hms(0, 0, 0)
    // "date" : "2023-10-27T15:45:00Z",
    let json_str = r#"{
        "id" : 21.1,
        "p_i" : {
            "args" : [
                "idx_us_ndx"
            ],
            "kwargs" : {
                "device" : "mobile",
                "upload_to_aws" : true
            }
        },
        "t_o" : "production_backend-node8c6b43063463",
        "cid" : "VTTT7Qu_jaQn-IhAAAGP",
        "cache_message" : true,
        "stopic" : "pca",
        "ts" : 1698155232.5238342,
        "fun_n" : "get_correlation_analysis_tear_sheet_user_asset",
        "e" : "Error",
        "key" : "8631c843c43d7d746de2b80ca4db2cdc",
        "exception_message" : "Traceback (most recent call last):\n  File \"/home/airflow/src/services/kafka_helpers/message_contracts.py\", line 381, in get_output_message\n    data = MessageContracts.MESSAGEID_FUNCTION_MAP.get(\n  File \"/home/airflow/.local/lib/python3.8/site-packages/decorator.py\", line 232, in fun\n    return caller(func, *(extras + args), **kw)\n  File \"/home/airflow/src/util/helper.py\", line 187, in save_data_to_contabo\n    args_,kwargs = func(*args, **kwargs)\n  File \"/home/airflow/src/analytics/portfolio.py\", line 361, in get_correlation_analysis_tear_sheet_user_asset\n    df = pe.get_df_from_s3(sravz_id)\n  File \"/home/airflow/src/services/price_queries.py\", line 149, in get_df_from_s3\n    data_df = pd.read_csv(io.BytesIO(historical_price))\nTypeError: a bytes-like object is required, not 'list'\n"
    }"#;
    let result: Result<Message, serde_json::Error> = serde_json::from_str(json_str);        
    // Handle the result using pattern matching
    match result {
        Ok(_message) => {
            let messages = mongo::find(_message, &client).await.expect("Document not found");
            assert!(messages.len() > 0, "1 or more messages should be found.");
        }
        Err(err) => {
            eprintln!("Deserialization failed: {}", err);
        }
    }    
}
