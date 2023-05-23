#include <cstdio>
#include <iostream>
#include <memory>
#include <router.hpp>
#include <sstream>
#include <string>
#include <vector>
#include <boost/log/core.hpp>
#include <boost/log/expressions.hpp>
#include <boost/log/trivial.hpp>

using namespace boost::urls;

namespace sravz {
    void router::init_()
    {
        // Initialize services
        mongoClient_ = std::make_shared<sravz::services::mongo::MongoClient>(std::move("mongodb://sravz:sravz@mongo:27017/sravz"));
        Aws::SDKOptions options;
        s3Client_ = std::make_shared<sravz::services::aws::s3::S3Client>("us-east-1", "sravz-data", std::move(options), sravz::services::aws::s3::S3ClientType::AWS);
        // Initialize controllers
        mongoController_ = std::make_shared<sravz::controllers::mongo::MongoController>(mongoClient_);
        awsS3Controller_ = std::make_shared<sravz::controllers::aws::AWSS3Controller>(s3Client_);
    }

    std::pair<boost::beast::http::status, std::string> router::route(boost::beast::http::verb verb, const std::string& uri, const std::string& body)
    {
        try { 
            BOOST_LOG_TRIVIAL(info) << "Request URL: " << uri;
            //result<boost::urls::url_view> r = boost::urls::parse_uri(uri);
            //url_view u = r.value();
            boost::urls::url_view uv(uri);
            auto segments = uv.segments();
            if (!segments.size())
                return { boost::beast::http::status::not_implemented, "Unsupported path" };
                // return "Path Not Supported";
            boost::json::object obj;
            std::map<std::string, std::string> params_map;
            for (auto param: uv.params()) {
                obj[param.key] = param.value;
                params_map[param.key] = param.value;
            }
            auto params_json = boost::json::serialize(obj);
            switch (verb) {
                case boost::beast::http::verb::get:
                    if (*segments.begin() == "mdb")
                    {
                        if (!uv.params().size()) {
                            // Avoid sending the complete collection
                            return { boost::beast::http::status::bad_request, "Params required for GET method" };        
                        }
                        auto it = std::next(segments.begin());
                        if (it != segments.end()) {
                            return { boost::beast::http::status::ok, mongoController_->get(*it, params_json) };
                        }                    
                    } else if (*segments.begin() == "s3") {
                        if (!uv.params().size()) {
                            // Avoid sending the complete collection
                            return { boost::beast::http::status::bad_request, "Params required for GET method" };        
                        }
                        if (!obj.contains("bucket") || !obj.contains("key") || !obj.contains("column") || !obj.contains("in_clause")) {
                            return { boost::beast::http::status::bad_request, "bucket, key, col and in_clause params required" };   
                        } 
                        BOOST_LOG_TRIVIAL(info) << "S3-Select: Bucket " << params_map["bucket"] << " Key: " << params_map["key"] << " Column: " << params_map["column"] << " in_clause: " << params_map["in_clause"];
                        return {boost::beast::http::status::ok, 
                                awsS3Controller_->get(params_map["bucket"], params_map["key"], params_map["column"], params_map["in_clause"])
                        };
                    }            
                    return { boost::beast::http::status::not_implemented, "Unsupported service" };
                    break;
                case boost::beast::http::verb::post:
                    if (*segments.begin() == "mdb")
                    {
                        auto it = std::next(segments.begin());
                        if (it != segments.end()) {
                            return { boost::beast::http::status::created, mongoController_->post(*it, body)};                      
                        }
                    }
                    return { boost::beast::http::status::not_implemented, "Unsupported service" };
                    break;
                case boost::beast::http::verb::put:
                    if (*segments.begin() == "mdb")
                    {
                        auto it = std::next(segments.begin());
                        if (it != segments.end()) {
                            boost::json::value json = boost::json::parse(body);
                            std::string filter_json = boost::json::serialize(json.at("filter").as_object());
                            std::string update_json = boost::json::serialize(json.at("update").as_object());
                            bool update_one = json.at("update_one").as_bool();
                            return { boost::beast::http::status::created, mongoController_->put(*it, filter_json, update_json, update_one)};    
                        }
                    }
                    return { boost::beast::http::status::not_implemented, "Unsupported service" };
                    break;
                case boost::beast::http::verb::delete_:
                    if (*segments.begin() == "mdb")
                    {
                        auto it = std::next(segments.begin());
                        if (it != segments.end()) {
                            boost::json::value json = boost::json::parse(body);
                            std::string filter_json = boost::json::serialize(json.at("filter").as_object());
                            bool delete_one = json.at("delete_one").as_bool();
                            return { boost::beast::http::status::ok, mongoController_->_delete(*it, filter_json, delete_one)};      
                        }
                    }
                    return { boost::beast::http::status::not_implemented, "Unsupported service" };
                    break;
                default:
                    return { boost::beast::http::status::method_not_allowed, "Unsupported method" };            
                    break;
            }
            return { boost::beast::http::status::method_not_allowed, "Unsupported method" };
        }
        catch(std::exception& ex)
        {
            return { boost::beast::http::status::internal_server_error, "Error" };
            BOOST_LOG_TRIVIAL(error) << "Router error" << ex.what();
        }
        return { boost::beast::http::status::not_implemented, "Unsupported service" };
    }
}
