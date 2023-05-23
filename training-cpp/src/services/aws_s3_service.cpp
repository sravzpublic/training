#include <aws_s3_service.hpp>
#include <aws/core/auth/AWSCredentialsProvider.h>
#include <aws/core/Aws.h>
#include <aws/core/client/ClientConfiguration.h>
#include <aws/core/utils/memory/stl/AWSStringStream.h>
#include <aws/s3/model/Bucket.h>
#include <aws/s3/model/CSVInput.h>
#include <aws/s3/model/CSVOutput.h>
#include <aws/s3/model/DeleteObjectRequest.h>
#include <aws/s3/model/GetObjectRequest.h>
#include <aws/s3/model/InputSerialization.h>
#include <aws/s3/model/JSONInput.h>
#include <aws/s3/model/JSONOutput.h>
#include <aws/s3/model/ListObjectsRequest.h>
#include <aws/s3/model/Object.h>
#include <aws/s3/model/OutputSerialization.h>
#include <aws/s3/model/ParquetInput.h>
#include <aws/s3/model/PutObjectRequest.h>
#include <aws/s3/model/SelectObjectContentRequest.h>
#include <aws/s3/S3Client.h>
#include <boost/log/core.hpp>
#include <boost/log/expressions.hpp>
#include <boost/log/trivial.hpp>
#include <string>
#include <util.hpp>

namespace sravz {
    namespace services {
        namespace aws {
            namespace s3 {
                S3Client::S3Client(const std::string& region, const std::string& bucket, Aws::SDKOptions options, S3ClientType type)
                    :m_region(region), 
                    m_bucket(bucket), 
                    options_(options),
                    type_(type)
                {
                    Aws::Client::ClientConfiguration clientConfig;
                    switch (type)
                    {
                        case S3ClientType::CONTABO:
                        {
                            clientConfig.endpointOverride = Aws::String("usc1.contabostorage.com");
                            clientConfig.scheme = Aws::Http::Scheme::HTTPS;
                            std::string CONTABO_KEY;
                            std::string CONTABO_SECRET;
                            getenv("CONTABO_KEY", CONTABO_KEY);
                            getenv("CONTABO_SECRET", CONTABO_SECRET);
                            Aws::Auth::AWSCredentials credentialsContabo(CONTABO_KEY, CONTABO_SECRET);
                            m_s3Client =  Aws::S3::S3Client(credentialsContabo, clientConfig, Aws::Client::AWSAuthV4Signer::PayloadSigningPolicy::Never, false);
                            break;
                        }
                        case S3ClientType::AWS:
                        {
                            std::string AWS_ACCESS_KEY_ID;
                            std::string AWS_SECRET_ACCESS_KEY;
                            getenv("AWS_ACCESS_KEY_ID", AWS_ACCESS_KEY_ID);
                            getenv("AWS_SECRET_ACCESS_KEY", AWS_SECRET_ACCESS_KEY);
                            Aws::Auth::AWSCredentials credentialsAWS(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY);
                            m_s3Client =  Aws::S3::S3Client(credentialsAWS);
                            break;
                        }
                        default:
                            std::cout << "Unsupported message type" << std::endl;
                            break;
                    }
                }

                bool S3Client::putObject(const std::string& key, const std::string& value)
                {
                    Aws::S3::Model::PutObjectRequest request;
                    request.SetBucket(m_bucket);
                    request.SetKey(key);
                    // Creates a shared pointer of Aws::StringStream
                    auto stream = Aws::MakeShared<Aws::StringStream>("putObject", "");
                    *stream << value;
                    request.SetBody(stream);

                    auto outcome = m_s3Client.PutObject(request);
                    if (outcome.IsSuccess()) {
                        return true;
                    } else {
                        std::cout << "Failed with error: " << outcome.GetError() << std::endl;
                        return false;
                    }
                }

                std::string S3Client::getObject(const std::string& key)
                {
                    Aws::S3::Model::GetObjectRequest request;
                    request.SetBucket(m_bucket);
                    request.SetKey(key);

                    auto outcome = m_s3Client.GetObject(request);
                    if (outcome.IsSuccess()) {
                        // Takes ownership of the GetObjectResult
                        auto& retrievedObject = outcome.GetResultWithOwnership().GetBody();
                        std::stringstream ss;
                        ss << retrievedObject.rdbuf();
                        return ss.str();
                    } else {
                        std::cout << "Failed with error: " << outcome.GetError() << std::endl;
                        return "";
                    }
                }

                std::vector<std::string> S3Client::listObjects()
                {
                    Aws::S3::Model::ListObjectsRequest request;
                    request.SetBucket(m_bucket);

                    std::vector<std::string> objectKeys;
                    auto outcome = m_s3Client.ListObjects(request);
                    if (outcome.IsSuccess()) {
                        auto objects = outcome.GetResult().GetContents();
                        for (const auto& object : objects) {
                            objectKeys.push_back(object.GetKey());
                        }
                    } else {
                        std::cout << "Failed with error: " << outcome.GetError() << std::endl;
                    }
                    return objectKeys;
                }

                bool S3Client::deleteObject(const std::string& key)
                {
                    Aws::S3::Model::DeleteObjectRequest request;
                    request.SetBucket(m_bucket);
                    request.SetKey(key);

                    auto outcome = m_s3Client.DeleteObject(request);
                    if (outcome.IsSuccess()) {
                        return true;
                    } else {
                        std::cout << "Failed with error: " << outcome.GetError() << std::endl;
                        return false;
                    }
                }

                std::string S3Client::s3select(const std::string& bucket, const std::string& key, const std::string& column, const std::string& in_clause)
                {
                    Aws::S3::Model::SelectObjectContentRequest request;
                    request.SetBucket(bucket);
                    request.SetKey(key);
                    request.SetExpressionType(Aws::S3::Model::ExpressionType::SQL);
                    std::ostringstream buffer;
                    buffer << "[";

                    if (!in_clause.empty()) {
                        std::vector<std::string> params;
                        std::stringstream ss(in_clause);
                        std::string param;
                        while (std::getline(ss, param, ',')) {
                            params.push_back(param);
                        }
                        std::string inClause = "(";
                        for (auto it = params.begin(); it != params.end(); ++it)
                        {
                            inClause += "'" + *it + "'";
                            if (it != params.end() - 1)
                                inClause += ",";
                        }
                        inClause += ")";
                        BOOST_LOG_TRIVIAL(info) << "Select statement: SELECT * FROM S3Object WHERE " << column << " IN " << inClause;
                        request.SetExpression("SELECT * FROM S3Object WHERE " + column + " IN " + inClause);
                    } else {
                        request.SetExpression("SELECT * FROM S3Object");
                    }


                    // Set the input and output serialization formats for Parquet
                    Aws::S3::Model::InputSerialization input_serialization;
                    input_serialization.SetParquet(Aws::S3::Model::ParquetInput());
                    Aws::S3::Model::OutputSerialization output_serialization;
                    Aws::S3::Model::JSONOutput jsonOutput;
                    jsonOutput.SetRecordDelimiter(",");
                    output_serialization.SetJSON(jsonOutput);
                    request.SetInputSerialization(input_serialization);
                    request.SetOutputSerialization(output_serialization);

                    Aws::S3::Model::SelectObjectContentHandler handler;
                    handler.SetRecordsEventCallback([&](const Aws::S3::Model::RecordsEvent& recordsEvent)
                    {
                        auto recordsVector = recordsEvent.GetPayload();
                        Aws::String records(recordsVector.begin(), recordsVector.end());
                        buffer << records.c_str();
                    });
                    handler.SetStatsEventCallback([&](const Aws::S3::Model::StatsEvent& statsEvent)
                    {

                    });

                    // Register a callback function to handle the S3 Select events
                    request.SetEventStreamHandler(handler);

                    // Issue the S3 Select request
                    auto outcome = m_s3Client.SelectObjectContent(request);
                    if (outcome.IsSuccess())
                    {
                        std::cout << "S3 Select request succeeded" << std::endl;
                    }
                    else
                    {
                        std::cout << "S3 Select request failed: " << outcome.GetError().GetMessage() << std::endl;
                    }
                    auto outputString = buffer.str();
                    if (!outputString.empty() && outputString.back() == ',') {
                        outputString.pop_back();
                    }
                    outputString += "]";
                    return outputString;
                }

                S3Client::~S3Client()
                {
                    // Aws::ShutdownAPI(options_);
                }
            }
        }
    }
}


