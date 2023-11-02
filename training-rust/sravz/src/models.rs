use bson::oid::ObjectId;
use chrono::DateTime;
use chrono::Utc;
use serde_derive::Deserialize;
use serde_derive::Serialize;

#[derive(Default, Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Message {
    #[serde(rename = "_id", skip_serializing_if = "Option::is_none")]
    pub id: Option<ObjectId>,
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
    // #[serde(with = "bson::serde_helpers::chrono_datetime_as_bson_datetime")]
    // pub date: DateTime<Utc>,
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
