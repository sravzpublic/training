use bson::oid::ObjectId;
use chrono::DateTime;
use chrono::Utc;
use polars::series::IntoSeries;
use polars::series::Series;
use serde::ser::SerializeStruct;
use serde_derive::Deserialize;
use serde::{Serialize, Serializer};

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
    #[serde(skip, with = "bson::serde_helpers::chrono_datetime_as_bson_datetime")]
    pub date: DateTime<Utc>,
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

#[derive(Default, Debug, Clone, PartialEq, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct HistoricalQuote {
    #[serde(rename = "Date")]
    pub date: Date,
    #[serde(rename = "Volume")]
    pub volume: i64,
    #[serde(rename = "Open")]
    pub open: f64,
    #[serde(rename = "High")]
    pub high: f64,
    #[serde(rename = "Low")]
    pub low: f64,
    #[serde(rename = "Close")]
    pub close: f64,
    #[serde(rename = "AdjustedClose")]
    pub adjusted_close: f64,
}

#[derive(Default, Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Date {
    #[serde(rename = "_isoformat")]
    pub isoformat: String,
}

impl Serialize for HistoricalQuote {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let mut state = serializer.serialize_struct("HistoricalQuote", 1)?;
        state.serialize_field("Date", &self.date.isoformat)?;
        state.end()
    }
}

// Implement IntoSeries for YourStruct
// unsafe impl IntoSeries for HistoricalQuote {
//     fn into_series(self) -> Series {
//         let data_series: Series = self.date.into();
//         let volume_series: Series = self.volume.into();

//         // Concatenate the Series into a single Series
//         data_series.concat(&volume_series)
//     }
// }