#pragma once
// Service includes
#include <mongo_service.hpp>
#include <aws_s3_service.hpp>
// Controller includes
#include <mongo_controller.hpp>
#include <aws_s3_controller.hpp>
#include <boost/beast/http.hpp>
#include <boost/json.hpp>
#include <boost/url.hpp>


namespace sravz {
    class router
    {
        public:
            router()
            {
                init_();
            }
            std::pair<boost::beast::http::status, std::string> route(boost::beast::http::verb method, const std::string& uri, const std::string& body);
        private:
            void init_();
            // Services
            std::shared_ptr<sravz::services::mongo::MongoClient> mongoClient_;
            std::shared_ptr<sravz::services::aws::s3::S3Client> s3Client_;
            // Controllers
            std::shared_ptr<sravz::controllers::mongo::MongoController> mongoController_;
            std::shared_ptr<sravz::controllers::aws::AWSS3Controller> awsS3Controller_;
    };
}

