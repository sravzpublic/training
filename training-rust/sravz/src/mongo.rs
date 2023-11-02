use futures::TryStreamExt;
use mongodb::Client;
use mongodb::bson::doc;
use serde_json;

use crate::models::{Message, PI};

pub async fn create(_create: Message, _mdb: &Client){
    let db = _mdb.database("sravz");
    let _col = db.collection::<Message>("nsq_message_cache");
    _col.insert_one(_create, None).await.expect("Unable to insert message");
}

pub async fn find(_create: Message, _mdb: &Client) -> Result<Vec<Message>, Box<dyn std::error::Error>>  {
    let db = _mdb.database("sravz");
    let _col = db.collection::<Message>("nsq_message_cache");
    let messages: Vec<Message> = _col.find(doc! { "key": _create.key }, None).await
        .expect("Unable to get Cursor")
        .try_collect().await
        .expect("Unable to collect from items Cursor");
    println!("messages: {:?}", messages);
    Ok(messages)
}

pub async fn find_by_key(key: String, _mdb: &Client) -> Result<Vec<Message>, Box<dyn std::error::Error>>  {
    let db = _mdb.database("sravz");
    let _col = db.collection::<Message>("nsq_message_cache");
    let messages: Vec<Message> = _col.find(doc! { "key": key }, None).await
        .expect("Unable to get Cursor")
        .try_collect().await
        .expect("Unable to collect from items Cursor");
    println!("messages: {:?}", messages);
    Ok(messages)
}

async fn update_many(_create: Message, _mdb: &Client){
    let client = Client::with_uri_str("mongodb://mongo:root@localhost:27017").await
    .expect("Unable to connect to MongoDB");
    let db = client.database("sravz");
    let _col = db.collection::<Message>("nsq_message_cache");
    _col.update_many(
        doc! { "key": "8631c843c43d7d746de2b80ca4db2cdc" },
        doc! { "$set": { "date": "ISODate(\"2023-10-24T13:47:13.550+0000\")" } },
        None,
    ).await.expect("Unable to update messages");
}

async fn delete_many(_create: Message, _mdb: &Client){
    let client = Client::with_uri_str("mongodb://mongo:root@localhost:27017").await
    .expect("Unable to connect to MongoDB");
    let db = client.database("sravz");
    let _col = db.collection::<Message>("nsq_message_cache");
    _col.delete_many(
        doc! { "key": "8631c843c43d7d746de2b80ca4db2cdc" },
        None,
    ).await.expect("Unable to delete messages");
    let messages: Vec<Message> = _col.find(doc! { "key": "8631c843c43d7d746de2b80ca4db2cdc" }, None).await
        .expect("Unable to get Cursor")
        .try_collect().await
        .expect("Unable to collect items from Cursor");
    println!("messages: {:?}", messages);
}

