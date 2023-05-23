#pragma once

#include "util.hpp"
using namespace std;

// https://docs.sravz.com/docs/tech/cpp/boost-beast-websockets/
int ws_vendor(std::string host, std::string port, std::string text, std::string endpoint, int threads);
void redis_uploader(std::string topics);
// https://docs.sravz.com/docs/tech/cpp/boost-beast-websocket-server/
int webserver(std::string address_, 
              std::string port_, 
              std::string doc_root_, 
              std::string threads_, 
              std::string topics_, 
              boost::program_options::variables_map vm_env);

// A helper function to simplify the main part.
template<class T>
ostream& operator<<(ostream& os, const vector<T>& v)
{
    copy(v.begin(), v.end(), ostream_iterator<T>(os, " "));
    return os;
}

// https://gcc.godbolt.org/z/pfJXRm
// https://en.cppreference.com/w/cpp/language/consteval
// This function might be evaluated at compile-time, if the input
// is known at compile-time. Otherwise, it is executed at run-time.
constexpr inline
unsigned long long int get_hash(char const * str, int h = 0)
{
	return (!str[h] ? 5381 : (get_hash(str, h+1)*33) ^ str[h] );
}

constexpr inline
unsigned long long int operator "" _(char const * p, size_t) { return get_hash(p); }

inline
unsigned long long int get_hash(std::string const & s) { return get_hash (s.c_str()); }
