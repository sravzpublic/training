use std::collections::HashSet;
use tokio_nsq::{NSQTopic, NSQChannel, NSQConsumerConfig, NSQConsumerConfigSources, NSQConsumerLookupConfig, NSQProducerConfig};
use gethostname::gethostname;

#[tokio::main]
async fn main() {
    let consumer_topic_name = "training-rust";
    let producer_topic_name = "training-node";
    let consumer_topic   = NSQTopic::new(consumer_topic_name).unwrap();
    let producer_topic = NSQTopic::new(producer_topic_name).unwrap();
    let channel = NSQChannel::new(gethostname().to_string_lossy().to_string()).unwrap();
    

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
        println!("message body = {}", message_body_str);
        producer.publish(&producer_topic, message_body_str.as_bytes().to_vec()).await.unwrap();
        // Wait until the message is acknowledged by NSQ
        // assert_matches!(producer.consume().await.unwrap(), NSQEvent::Ok());
        producer.consume().await.unwrap();
        message.finish().await;
    }

}