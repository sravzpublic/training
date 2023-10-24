use std::collections::HashSet;
use tokio_nsq::{NSQTopic, NSQChannel, NSQConsumerConfig, NSQConsumerConfigSources, NSQConsumerLookupConfig};
use gethostname::gethostname;

#[tokio::main]
async fn main() {
    let topic_name = "training-rust";
    let topic   = NSQTopic::new(topic_name).unwrap();
    let channel = NSQChannel::new(gethostname().to_string_lossy().to_string()).unwrap();
    
    let mut addresses = HashSet::new();
    addresses.insert("http://nsqlookupd-1:4161".to_string());
    
    println!("Listening to nsq topic {} - channel {:?}", topic_name, gethostname());

    let mut consumer = NSQConsumerConfig::new(topic, channel)
        .set_max_in_flight(15)
        .set_sources(
            NSQConsumerConfigSources::Lookup(
                NSQConsumerLookupConfig::new().set_addresses(addresses)
            )
        )
        .build();
    
    loop {
        let message = consumer.consume_filtered().await.unwrap();
        
        let message_body_str = std::str::from_utf8(&message.body).unwrap();
        println!("message body = {}", message_body_str);
        
        message.finish().await;
    }

}