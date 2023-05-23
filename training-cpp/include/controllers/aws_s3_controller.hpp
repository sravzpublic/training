#pragma once
#include <aws_s3_service.hpp>
#include <memory>
#include <aws/core/Aws.h>

namespace sravz {
    namespace controllers {
        namespace aws {
            class AWSS3Controller
            {
                public:
                    AWSS3Controller(std::shared_ptr<sravz::services::aws::s3::S3Client> &s3Client)
                        : s3Client_(s3Client)
                    {
                    }
                    std::string get(const std::string& bucket, const std::string& key, const std::string& column, const std::string& in_clause);
                private:
                    std::shared_ptr<sravz::services::aws::s3::S3Client> s3Client_;
                    Aws::SDKOptions awsOptions_;
            };
        }
    }
}