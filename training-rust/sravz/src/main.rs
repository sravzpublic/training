use std::collections::HashSet;

use tokio_nsq::{NSQTopic, NSQChannel, NSQConsumerConfig, NSQConsumerConfigSources, NSQConsumerLookupConfig};

fn main() {
    let topic   = NSQTopic::new("names").unwrap();
    let channel = NSQChannel::new("first").unwrap();
    
    let mut addresses = HashSet::new();
    addresses.insert("http://nsqlookupd-1:4161".to_string());
    
    let mut consumer = NSQConsumerConfig::new(topic, channel)
        .set_max_in_flight(15)
        .set_sources(
            NSQConsumerConfigSources::Lookup(
                NSQConsumerLookupConfig::new().set_addresses(addresses)
            )
        )
        .build();
    
    let mut message = consumer.consume_filtered().await.unwrap();
    
    let message_body_str = std::str::from_utf8(&message.body).unwrap();
    println!("message body = {}", message_body_str);
    
    message.finish();
}
