mod models;
mod helper;
mod mongo;
mod mongo_test;
use std::collections::HashSet;
use tokio_nsq::{NSQTopic, NSQChannel, NSQConsumerConfig, NSQConsumerConfigSources, NSQConsumerLookupConfig, NSQProducerConfig};
use gethostname::gethostname;
use mongodb::Client;
use std::env;
use tokio;
use std::error::Error;

use crate::{helper::sha256_hash, models::Message};

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
// async fn main() {    
    let consumer_topic_name = "training-rust";
    let producer_topic_name = "training-node";
    let consumer_topic   = NSQTopic::new(consumer_topic_name).unwrap();
    let producer_topic = NSQTopic::new(producer_topic_name).unwrap();
    let channel = NSQChannel::new(gethostname().to_string_lossy().to_string()).unwrap();
    let client = Client::with_uri_str("mongodb://sravz:sravz@mongo:27017/sravz").await
    .expect("Unable to connect to MongoDB");  
    // Utc.ymd(2020, 2, 7).and_hms(0, 0, 0)
    // "date" : "2023-10-27T15:45:00Z",
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

    // TODO: Wait until a connection is initialized
    // assert_matches!(producer.consume().await.unwrap(), NSQEvent::Healthy());

    loop {
        let message = consumer.consume_filtered().await.unwrap();
        let message_body_str = std::str::from_utf8(&message.body).unwrap();        
        let hashed_string = sha256_hash(message_body_str);
        println!("message body = {}", message_body_str);
        println!("message body SHA-256: {}", hashed_string);
        let messages = mongo::find_by_key(hashed_string, &client).await.expect("Document not found");  
         
        if  messages.len() > 0 {
            let message = &serde_json::to_string(&messages[0]).unwrap();
            producer.publish(&producer_topic, message.as_bytes().to_vec()).await.unwrap();
        } else {
            let result: Result<Message, serde_json::Error> = serde_json::from_str(message_body_str);        
            // Handle the result using pattern matching
            match result {
                Ok(mut _message) => {
                    let hashed_string = sha256_hash(message_body_str);
                    _message.key = hashed_string;
                    mongo::create(_message, &client).await;
                }
                Err(err) => {
                    eprintln!("Deserialization failed: {}", err);
                }
            }   
            producer.publish(&producer_topic, message_body_str.as_bytes().to_vec()).await.unwrap(); 
        }
        // TODO: Wait until the message is acknowledged by NSQ
        // assert_matches!(producer.consume().await.unwrap(), NSQEvent::Ok());
        producer.consume().await.unwrap();
        message.finish().await;
    }

    // Ok(())
}