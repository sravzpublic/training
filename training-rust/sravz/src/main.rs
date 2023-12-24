mod models;
mod helper;
mod mongo;
mod s3_module;
use s3_module::S3Module;
use serde_json::from_slice;
mod mongo_test;
use std::collections::HashSet;
use tokio_nsq::{NSQTopic, NSQChannel, NSQConsumerConfig, NSQConsumerConfigSources, NSQConsumerLookupConfig, NSQProducerConfig};
use gethostname::gethostname;
use mongodb::Client;
use tokio;
use std::error::Error;
use chrono::{Utc, Duration};
use crate::{helper::sha256_hash, models::{Message, HistoricalQuote}};
use log::{info, error};
use env_logger::Env;
use polars::prelude::*;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    env_logger::Builder::from_env(Env::default().default_filter_or("info")).init();
    let s3_module = S3Module::new();
    let bucket_name = "sravz-data";
    let object_key = "historical/etf_us_doo.json";
    let consumer_topic_name = "training-rust";
    let producer_topic_name = "training-node";
    let consumer_topic   = NSQTopic::new(consumer_topic_name).unwrap();
    let producer_topic = NSQTopic::new(producer_topic_name).unwrap();
    let channel = NSQChannel::new(gethostname().to_string_lossy().to_string()).unwrap();
    let client = Client::with_uri_str("mongodb://sravz:sravz@mongo:27017/sravz").await
    .expect("Unable to connect to MongoDB");  
    let mut addresses = HashSet::new();
    addresses.insert("http://nsqlookupd-1:4161".to_string());
    
    info!("Listening to nsq topic {} - channel {:?}", consumer_topic_name, gethostname());

    let mut consumer = NSQConsumerConfig::new(consumer_topic, channel)
        .set_max_in_flight(15)
        .set_sources(
            NSQConsumerConfigSources::Lookup(
                NSQConsumerLookupConfig::new().set_addresses(addresses)
            )
        )
        .build();
    
    let mut producer = NSQProducerConfig::new("nsqd-1:4150").build();

    // Download the uploaded object
    let downloaded_content = s3_module.download_object(bucket_name, object_key).await;
    match s3_module.decompress_gzip(downloaded_content) {
        Ok(decompressed_data) => {
            // info!("Decompressed data: {:?}", String::from_utf8_lossy(&decompressed_data[1..1000]));
            // Deserialize JSON data into a Vec<YourStruct>
            let vec_data: Vec<HistoricalQuote> = from_slice(&decompressed_data).expect("Failed to deserialize JSON data");

            // Create a polars DataFrame from the Vec<YourStruct>
            let df: DataFrame = DataFrame::new(vec_data).expect("Failed to create DataFrame");

            // Print the DataFrame
            println!("{:?}", df);
        }
        Err(err) => {
            info!("Error during decompression: {:?}", err);
        }
    }
    // info!("Downloaded content: {:?}", String::from_utf8_lossy(&downloaded_content));
    // TODO: Wait until a connection is initialized
    // assert_matches!(producer.consume().await.unwrap(), NSQEvent::Healthy());

    loop {
        let message = consumer.consume_filtered().await.unwrap();
        let message_body_str = std::str::from_utf8(&message.body).unwrap();        
        let hashed_string = sha256_hash(message_body_str);
        info!("Message received on NSQ = {} - SHA-256 = {}", message_body_str, hashed_string);
        let messages = mongo::find_by_key(hashed_string, &client).await.expect("Document not found");  
         
        /* If the message exists and inserted less than 24 hours back - resend the same message else reprocess the message */
        if  messages.len() > 0 && messages[0].date + Duration::days(1) < Utc::now() {
            let message = &serde_json::to_string(&messages[0]).unwrap();
            info!("Sending the existing message in mongodb {}", message);
            producer.publish(&producer_topic, message.as_bytes().to_vec()).await.unwrap();
        } else {
            info!("Processing the message");
            let result: Result<Message, serde_json::Error> = serde_json::from_str(message_body_str);        
            // Handle the result using pattern matching
            match result {
                Ok(mut _message) => {
                    let hashed_string: String = sha256_hash(message_body_str);
                    _message.date = Utc::now();
                    _message.key = hashed_string;
                    mongo::create(_message, &client).await;
                }
                Err(err) => {
                    error!("Deserialization failed: {}", err);
                }
            }   
            info!("Sending the processed message on NSQ {}", message_body_str);
            producer.publish(&producer_topic, message_body_str.as_bytes().to_vec()).await.unwrap(); 
        }
        // TODO: Wait until the message is acknowledged by NSQ
        // assert_matches!(producer.consume().await.unwrap(), NSQEvent::Ok());
        producer.consume().await.unwrap();
        message.finish().await;
    }

    // Ok(())
}