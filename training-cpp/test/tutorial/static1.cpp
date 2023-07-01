#include "static1.hpp"

std::string StaticB::b = "Hello world - B";

std::string StaticB::get_b() {
    // b = "Hello World - B";
    return b;
}