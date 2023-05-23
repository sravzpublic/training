#pragma once
#include <string>
#include <vector>
#include <aws/core/Aws.h>
#include <aws/s3/S3Client.h>

namespace sravz {
    namespace services {
        namespace aws {
            namespace s3 {
                enum class S3ClientType {
                        CONTABO = 1,
                        AWS = 2
                };

                class S3Client {
                public:
                    S3Client(const std::string& region, const std::string& bucket, Aws::SDKOptions options, S3ClientType type);
                    bool putObject(const std::string& key, const std::string& value);
                    std::string getObject(const std::string& key);
                    std::vector<std::string> listObjects();
                    bool deleteObject(const std::string& key);
                    std::string s3select(const std::string& bucket, const std::string& key, const std::string& column, const std::string& value);
                    ~S3Client();
                private:
                    std::string m_region;
                    std::string m_bucket;
                    Aws::Client::ClientConfiguration m_clientConfig;
                    Aws::S3::S3Client m_s3Client;
                    Aws::SDKOptions options_;
                    S3ClientType type_;
                    // void processRecordsEvent_(const Aws::S3::Model::SelectObjectContentEventStream& eventStream);
                };
            }
        }
    }
}