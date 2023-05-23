#include <util.hpp>

// Gets env variable
bool getenv(const char *name, std::string &env)
{
    const char *ret = getenv(name);
    if (ret) {
        env = std::string(ret);
    } else {
        std::cout << "Env variable: " << name << " not set!!!";
    }
    return !!ret;
}

// Returns redis connection options to be used in redis connection creation
sw::redis::ConnectionOptions getRedisConnectionOptions() {
    std::string REDIS_HOST;
    std::string REDIS_PORT;
    std::string REDIS_PASSWORD;
    sw::redis::ConnectionOptions opts;
    if (getenv("REDIS_HOST", REDIS_HOST))
        opts.host = REDIS_HOST;
    if (getenv("REDIS_PORT", REDIS_PORT))
        opts.port = std::stoi(REDIS_PORT);
    if (getenv("REDIS_PASSWORD", REDIS_PASSWORD))
        opts.password = REDIS_PASSWORD;
    opts.socket_timeout = std::chrono::milliseconds(200);
    return opts;
}
