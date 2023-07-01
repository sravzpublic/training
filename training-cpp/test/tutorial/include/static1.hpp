#include <iostream>

class StaticB
{
private:
    /* data */    
public:
    StaticB(/* args */);
    ~StaticB();
    static std::string b;
    std::string get_b();
};
