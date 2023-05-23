/**
 * Sravz LLC
 * TODO: Handle multiple topics
 **/

#ifndef SRAVZ_REDIS_SUBSCRIBER_H
#define SRAVZ_REDIS_SUBSCRIBER_H

#include "util.hpp"

using RedisInstance = sw::redis::Redis;

class RedisSubscriber: public std::enable_shared_from_this<RedisSubscriber>
{
public:
  RedisSubscriber(std::string topics, std::shared_ptr<boost::asio::thread_pool>& io)
    : topics_(topics)
      ,redis_consumer_(RedisInstance(getRedisConnectionOptions()))
      ,redis_publisher_(RedisInstance(getRedisConnectionOptions()))
      ,io_(io)

  {
  }

  ~RedisSubscriber()
  {
    std::cout << "Subscriber closed" << std::endl;
  }

  void subscribe();

  void parse();

  void publish();

  void run();


    private:
    std::string topics_;
    RedisInstance redis_consumer_;
    RedisInstance redis_publisher_;
    std::shared_ptr<boost::asio::thread_pool> io_;
    boost::lockfree::spsc_queue<std::string, boost::lockfree::capacity<1024> > spsc_queue_parse_;
    boost::lockfree::spsc_queue<boost::json::object, boost::lockfree::capacity<1024> > spsc_queue_publish_;
    const int REDIS_BATCH_SIZE = 10;
    const int EXPONENTIAL_BACKOFF_LIMIT = 5;

    template<typename T1, typename T2>
    void get_message_with_backoff_(boost::lockfree::spsc_queue<T1, boost::lockfree::capacity<1024> > &queue, T2 &msg);

};

#endif