//
// SRAVZ LLC
//

#ifndef SRAVZ_WEB_PUBLISHER_HPP
#define SRAVZ_WEB_PUBLISHER_HPP

#include <util.hpp>
#include <sravz.hpp>
#include "shared_state.hpp"
#include "websocket_session.hpp"
#include "symbol.hpp"

class publisher : public boost::enable_shared_from_this<publisher>
{
    // RedisInstance redis_consumer_;
    net::io_context& ioc_publisher_;
    boost::shared_ptr<shared_state> state_;
public:
    explicit
    publisher(net::io_context& ioc_publisher, boost::shared_ptr<shared_state> const& state);
    void publish ();
};

#endif
