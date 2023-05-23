# Makefile
SHELL := /bin/bash
.PHONY: default
default: run
REDIS_PLUS_PLUS_MODULES_DIR=../redis-plus-plus-modules
BOOST_1_81_0_DIR=/workspace/backend-cpp/boost_1_81_0/
INCLUDE_DIR=../include
INCLUDE_SERVICES_DIR=../include/services
INCLUDE_CONTROLLERS_DIR=../include/controllers
INCLUDE_ROUTER_DIR=../include/router
CPP_JWT_INCLUDE_DIR=/workspace/backend-cpp/cpp-jwt/include/
ENV_VAR_FILE=../.env
include $(ENV_VAR_FILE)
export $(shell sed 's/=.*//' $(ENV_VAR_FILE))

cd-backend-cpp-dir:
	cd ${BACKEND-CPP-DIR}

build-docker-image:
	docker build --tag public.ecr.aws/b8h3z2a1/sravz/backend-cpp:$(BACKEND_CPP_IMAGE_Version) .

sravz_service_db:
	g++ --std=c++17 -I$(INCLUDE_SERVICES_DIR) -I$(BOOST_1_81_0_DIR) -I/usr/local/include/mongocxx/v_noabi -I/usr/local/include/bsoncxx/v_noabi -L$(BOOST_1_81_0_DIR)/stage/lib -L/usr/local/lib ./main_mongo_db.cpp ../src/services/mongo_service.cpp -o ../dist/test/main_mongo_db -lmongocxx -lbsoncxx -lboost_json

sravz_service_aws_s3:
	g++ --std=c++17 -Wno-deprecated-declarations -DBOOST_LOG_DYN_LINK -I$(INCLUDE_DIR) -I$(INCLUDE_SERVICES_DIR) -I /usr/local/include/aws/include -L /usr/local/lib/ ./main_aws_s3.cpp ../src/services/aws_s3_service.cpp ../src/util.cpp -o ../dist/test/main_aws_s3 -laws-cpp-sdk-core -laws-cpp-sdk-s3 -lboost_log -lcrypto -lssl

sravz_router:
	g++ --std=c++17 -I$(INCLUDE_SERVICES_DIR) -I$(INCLUDE_CONTROLLERS_DIR) \
	-I$(INCLUDE_ROUTER_DIR) -I$(BOOST_1_81_0_DIR) -I/usr/local/include/mongocxx/v_noabi \
	-I/usr/local/include/bsoncxx/v_noabi -L/usr/local/lib \
	./main_router.cpp ../src/services/mongo_service.cpp ../src/router/router.cpp ../src/controllers/mongo_controller.cpp \
	-o ../dist/test/router -lmongocxx -lbsoncxx -lboost_json -lboost_url

run_service_db: sravz_service_db
	LD_LIBRARY_PATH=/usr/local/lib:$(BOOST_1_81_0_DIR)/stage/lib ../dist/test/main_mongo_db

run_service_aws_s3: sravz_service_aws_s3
	LD_LIBRARY_PATH=/usr/local/lib:$(BOOST_1_81_0_DIR)/stage/lib ../dist/test/main_aws_s3

run_router: sravz_router
	LD_LIBRARY_PATH=/usr/local/lib ../dist/test/router