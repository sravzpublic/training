use std::collections::HashSet;
use tokio_nsq::{NSQTopic, NSQChannel, NSQConsumerConfig, NSQConsumerConfigSources, NSQConsumerLookupConfig, NSQProducerConfig};
use gethostname::gethostname;
use mongodb::{Client, options::{ClientOptions, ResolverConfig}};
use std::env;
use tokio;
extern crate crypto;
extern crate digest;
extern crate sha2;
use digest::Digest;
use sha2::Sha256;
use std::error::Error;
use serde_derive::Deserialize;
use serde_derive::Serialize;

#[derive(Default, Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Root {
    #[serde(rename = "_id")]
    pub id: String,
    #[serde(rename = "id")]
    pub id2: f64,
    #[serde(rename = "p_i")]
    pub p_i: PI,
    #[serde(rename = "t_o")]
    pub t_o: String,
    pub cid: String,
    #[serde(rename = "cache_message")]
    pub cache_message: bool,
    pub stopic: String,
    pub ts: f64,
    #[serde(rename = "fun_n")]
    pub fun_n: String,
    pub e: String,
    pub date: String,
    pub key: String,
    #[serde(rename = "exception_message")]
    pub exception_message: String,
}

#[derive(Default, Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct PI {
    pub args: Vec<String>,
    pub kwargs: Kwargs,
}

#[derive(Default, Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Kwargs {
    pub device: String,
    #[serde(rename = "upload_to_aws")]
    pub upload_to_aws: bool,
}


fn sha256_hash(input: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(input);

    let result = hasher.finalize();
    
    // Convert the result to a hexadecimal string
    let hash_string = result.iter()
        .map(|byte| format!("{:02x}", byte))
        .collect::<String>();

    hash_string
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
// async fn main() {    
    let consumer_topic_name = "training-rust";
    let producer_topic_name = "training-node";
    let consumer_topic   = NSQTopic::new(consumer_topic_name).unwrap();
    let producer_topic = NSQTopic::new(producer_topic_name).unwrap();
    let channel = NSQChannel::new(gethostname().to_string_lossy().to_string()).unwrap();
    
    // Load the MongoDB connection string from an environment variable:
    let client_uri =
    env::var("MONGOLAB_URI").expect("You must set the MONGOLAB_URI environment var!");

    // A Client is needed to connect to MongoDB:
    // An extra line of code to work around a DNS issue on Windows:
    let options =
    ClientOptions::parse_with_resolver_config(&client_uri, ResolverConfig::cloudflare())
        .await?;
    let client = Client::with_options(options)?;

    // Print the databases in our MongoDB cluster:
    println!("Databases:");
    for name in client.list_database_names(None, None).await? {
    println!("- {}", name);
    }    

    let mut addresses = HashSet::new();
    addresses.insert("http://nsqlookupd-1:4161".to_string());
    
    println!("Listening to nsq topic {} - channel {:?}", consumer_topic_name, gethostname());

    let mut consumer = NSQConsumerConfig::new(consumer_topic, channel)
        .set_max_in_flight(15)
        .set_sources(
            NSQConsumerConfigSources::Lookup(
                NSQConsumerLookupConfig::new().set_addresses(addresses)
            )
        )
        .build();
    
    let mut producer = NSQProducerConfig::new("nsqd-1:4150").build();

    // Wait until a connection is initialized
    // assert_matches!(producer.consume().await.unwrap(), NSQEvent::Healthy());

    loop {
        let message = consumer.consume_filtered().await.unwrap();
        
        let message_body_str = std::str::from_utf8(&message.body).unwrap();        
        let hashed_string = sha256_hash(message_body_str);
        println!("message body = {}", message_body_str);
        println!("message body SHA-256: {}", hashed_string);
        
        /*
        {
            "_id" : ObjectId("6537cae1c6426dda1f34b0b5"),
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
            "date" : ISODate("2023-10-24T13:47:13.550+0000"),
            "key" : "8631c843c43d7d746de2b80ca4db2cdc",
            "exception_message" : "Traceback (most recent call last):\n  File \"/home/airflow/src/services/kafka_helpers/message_contracts.py\", line 381, in get_output_message\n    data = MessageContracts.MESSAGEID_FUNCTION_MAP.get(\n  File \"/home/airflow/.local/lib/python3.8/site-packages/decorator.py\", line 232, in fun\n    return caller(func, *(extras + args), **kw)\n  File \"/home/airflow/src/util/helper.py\", line 187, in save_data_to_contabo\n    args_,kwargs = func(*args, **kwargs)\n  File \"/home/airflow/src/analytics/portfolio.py\", line 361, in get_correlation_analysis_tear_sheet_user_asset\n    df = pe.get_df_from_s3(sravz_id)\n  File \"/home/airflow/src/services/price_queries.py\", line 149, in get_df_from_s3\n    data_df = pd.read_csv(io.BytesIO(historical_price))\nTypeError: a bytes-like object is required, not 'list'\n"
        }

        */
        producer.publish(&producer_topic, message_body_str.as_bytes().to_vec()).await.unwrap();
        // Wait until the message is acknowledged by NSQ
        // assert_matches!(producer.consume().await.unwrap(), NSQEvent::Ok());
        producer.consume().await.unwrap();
        message.finish().await;
    }

    // Ok(())
}