#include <iostream>

class  StaticA
{
private:
    /* data */

public:
    StaticA(/* args */);
    ~ StaticA();
    static std::string a;    
    std::string get_a();
};

