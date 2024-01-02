mod models;
mod helper;
mod mongo;
mod s3_module;
mod router;
mod mongo_test;
mod leveraged_funds;
use std::collections::HashSet;
use tokio_nsq::{NSQTopic, 
    NSQChannel, 
    NSQConsumerConfig, 
    NSQConsumerConfigSources, 
    NSQConsumerLookupConfig, 
    NSQProducerConfig};
use gethostname::gethostname;
use mongodb::Client;
use tokio;
use std::error::Error;
use chrono::{Utc, Duration};
use crate::{helper::sha256_hash, models::Message, router::Router};
use log::{info, error};
use env_logger::Env;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    env_logger::Builder::from_env(Env::default().default_filter_or("info")).init();
    let consumer_topic_name = "training-rust";
    let producer_topic_name = "training-node";
    let consumer_topic   = NSQTopic::new(consumer_topic_name).expect("Failed to create consumer topic");
    let producer_topic = NSQTopic::new(producer_topic_name).expect("Failed to create producer topic");
    let channel = NSQChannel::new(gethostname().to_string_lossy().to_string()).expect("Failed to create NSQ channel");
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
    let router = Router::new();
    loop {
        let message = consumer.consume_filtered().await.expect("Failed to consume NSQ message");
        let message_body_str = std::str::from_utf8(&message.body).expect("Failed to get JSON string from NSQ Message");        
        let hashed_string = &sha256_hash(message_body_str);
        info!("Message received on NSQ = {} - SHA-256 = {}", message_body_str, hashed_string);
        let messages = mongo::find_by_key(hashed_string.to_string(), &client).await.expect("Document not found");  
         
        /* If the message exists and inserted less than 24 hours back - resend the same message else reprocess the message */
        if  messages.len() > 0 && messages[0].date + Duration::days(1) < Utc::now() {
            let message = &serde_json::to_string(&messages[0]).expect("Failed to convert NSQ message to JSON string");
            info!("Sending the existing message in mongodb {}", message);
            producer.publish(&producer_topic, message.as_bytes().to_vec()).await.expect("Failed to publish NSQ message");
        } else {
            info!("Processing the message...");
            let result: Result<Message, serde_json::Error> = serde_json::from_str(message_body_str);        
            // Handle the result using pattern matching
            match result {
                Ok(mut _message) => {
                    let router_result = router.process_message(_message).await;
                    match router_result {
                        Ok(mut processed_message) => {
                            // let hashed_string: String = sha256_hash(message_body_str);
                            processed_message.date = Utc::now();
                            processed_message.key = hashed_string.to_string();
                            mongo::create(processed_message.clone(), &client).await;
                            let message_body_str = &serde_json::to_string(&processed_message).expect("Failed to convert message to JSON string");
                            info!("Sending the processed message on NSQ {}", message_body_str);
                            producer.publish(&producer_topic, message_body_str.as_bytes().to_vec()).await.expect("Failed to publish NSQ message"); 
                            continue;
                        }
                        Err(err) => {
                            error!("Router message processing error: {}", err);
                            //message_body_str = &serde_json::to_string(*err).expect("Failed to convert message to JSON string");
                        }
                    }
                }
                Err(err) => {
                    error!("Deserialization failed: {}", err);
                }
            }   
            info!("Unable to process message {}", message_body_str);
            producer.publish(&producer_topic, message_body_str.as_bytes().to_vec()).await.expect("Failed to publish NSQ message"); 
        }
        // TODO: Wait until the message is acknowledged by NSQ
        // assert_matches!(producer.consume().await.unwrap(), NSQEvent::Ok());
        // producer.consume().await.expect("Failed to consume NSQ message");
        // message.finish().await;
    }

    // Ok(())
}