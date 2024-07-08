use crate::{models::Message, s3_module::S3Module};
use std::io::Cursor;
use log::info;
use polars::prelude::*;
use std::error::Error;

pub struct LeveragedFunds{
    s3_module : S3Module
}

impl LeveragedFunds {

    pub fn new() -> Self {
        // TODO: Check proper dependency injection
        let s3_module = S3Module::new();
        LeveragedFunds { s3_module }
    }

    pub async fn leverage_funds_nasdaq100(&self, message: Message) -> Result<Message, Box<dyn Error>>  {
        let bucket_name = "sravz-data";
        let object_key = "historical/etf_us_qqq.json";
        // Download the uploaded object
        let downloaded_content = self.s3_module.download_object(bucket_name, object_key).await;
        match self.s3_module.decompress_gzip(downloaded_content) {
            Ok(decompressed_data) => {
                let cursor = Cursor::new(decompressed_data);
                let df = JsonReader::new(cursor)
                            .finish()
                            .unwrap();
                let mut df = df.unnest(["Date"]).unwrap();
                let df = df.rename("_isoformat", "Date").unwrap();
                let mut df = df
                .clone()
                .lazy()
                .select([
                    col("Date").dt().to_string("%Y-%m-%dTHH:mm:ss"),
                    col("DateTime").str().to_datetime(
                        Some(TimeUnit::Microseconds),
                        None,
                        StrptimeOptions::default(),
                        lit("raise"),
                    ),
                ])
                .collect()?;
                let _ = df.drop_in_place("Date");
                let df = df.rename("DateTime", "Date").unwrap();
                println!("{:?}", df);
            }
            Err(err) => {
                info!("Error during decompression: {:?}", err);
            }
        }

        return Ok(message);
    }

}
