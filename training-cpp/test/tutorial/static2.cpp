#include "static2.hpp"
// #include "static1.hpp"

std::string StaticA::a = "Hello world - a";

std::string StaticA::get_a() {
    return a; // + StaticB().get_b();
}