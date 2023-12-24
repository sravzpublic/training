use rusoto_core::{Region, ByteStream};
use rusoto_s3::{CreateBucketRequest, DeleteObjectRequest, GetObjectRequest, ListObjectsV2Request, PutObjectRequest, S3, S3Client};
use std::{io::{Read, self}, env};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use flate2::read::GzDecoder;

pub struct S3Module {
    client: S3Client,
}

impl S3Module {
    pub fn new() -> Self {
        let custom_endpoint = "usc1.contabostorage.com";
        let access_key = env::var("CONTABO_KEY").expect("CONTABO_KEY not found in environment variables");
        let secret_key = env::var("CONTABO_SECRET").expect("CONTABO_SECRET not found in environment variables");
        let client = S3Client::new_with(
            rusoto_core::request::HttpClient::new().expect("Failed to create HTTP client"),
            rusoto_core::credential::StaticProvider::new_minimal(access_key, secret_key),
            Region::Custom {
                name: "custom".to_owned(),
                endpoint: custom_endpoint.to_owned(),
            },
        );

        Self { client }
    }

    pub async fn create_bucket(&self, bucket_name: &str) {
        // Create a new bucket
        let create_bucket_request = CreateBucketRequest {
            bucket: bucket_name.to_string(),
            ..Default::default()
        };

        self.client.create_bucket(create_bucket_request).await.expect("Failed to create bucket");
    }

    pub async fn list_objects(&self, bucket_name: &str) {
        // List objects in the bucket
        let list_objects_request = ListObjectsV2Request {
            bucket: bucket_name.to_string(),
            ..Default::default()
        };

        let result = self.client.list_objects_v2(list_objects_request).await.expect("Failed to list objects");

        println!("Objects in the bucket:");
        for obj in result.contents.unwrap_or_default() {
            println!("{}", obj.key.unwrap_or_default());
        }
    }

    // pub async fn upload_object(&self, bucket_name: &str, object_key: &str, content: &[u8]) {
    //     // Upload an object to the bucket
    //     let put_object_request = PutObjectRequest {
    //         bucket: bucket_name.to_string(),
    //         key: object_key.to_string(),
    //         body: Some(ByteStream::new(content)),
    //         ..Default::default()
    //     };

    //     self.client.put_object(put_object_request).await.expect("Failed to upload object");
    // }

    pub fn decompress_gzip(&self, compressed_data: Vec<u8>) -> Result<Vec<u8>, io::Error> {
        // Create a GzDecoder and feed the compressed data into it
        let mut decoder = GzDecoder::new(compressed_data.as_slice());
    
        // Read the decompressed data into a Vec<u8>
        let mut decompressed_data = Vec::new();
        decoder.read_to_end(&mut decompressed_data)?;
    
        Ok(decompressed_data)
    }

    pub async fn download_object(&self, bucket_name: &str, object_key: &str) -> Vec<u8> {
        // Download an object from the bucket
        let get_object_request = GetObjectRequest {
            bucket: bucket_name.to_string(),
            key: object_key.to_string(),
            ..Default::default()
        };

        let response = self.client.get_object(get_object_request).await.expect("Failed to download object");
        let body = response.body.expect("Object body not found");

        let mut bytes = Vec::new();
        body.into_async_read().read_to_end(&mut bytes).await.expect("Failed to read object body");

        bytes
    }

    pub async fn delete_object(&self, bucket_name: &str, object_key: &str) {
        // Delete an object from the bucket
        let delete_object_request = DeleteObjectRequest {
            bucket: bucket_name.to_string(),
            key: object_key.to_string(),
            ..Default::default()
        };

        self.client.delete_object(delete_object_request).await.expect("Failed to delete object");
    }
}
