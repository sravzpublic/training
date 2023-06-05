#include <iostream>
#include <cstring>

class Sample {
    public:
        Sample(int i, std::string s): i_(i) {
            s_ = new char[s.size() + 1];
            strcpy(s_, s.data());    
            std::cout << "Consturctor called for: " << i << std::endl;
            std::cout << "String s_ initialized to: " << s_ << std::endl;
        };
        Sample(const Sample &s);        
        ~Sample();        
    private:
        int i_;
        char* s_;
        int size_;        
};

// Derived clases
class SampleBase {
  public:
    SampleBase()    
    { std::cout << "Constructing base" << std::endl; }
    virtual ~SampleBase()
    { std::cout<< "Destructing base" << std::endl; }    
};
 
class SampleDerived: public SampleBase {
  public:
    SampleDerived()    
     { std::cout << "Constructing derived" << std::endl; }
    ~SampleDerived()
       { std::cout << "Destructing derived" << std::endl; }
};

// Friend class
class SampleBase1 {
  private:
    SampleBase1() { 
        std::cout << "Constructing SampleBase1" << std::endl; 
    }
    friend class SampleBase2;

};
 
class SampleBase2 {
  public:
    SampleBase2() { 
        SampleBase1 sb;
        std::cout << "Constructing SampleBase2" << std::endl; 
    }
};

// Named constructor idiom. 
// Overcome limitation where asme parameter list cannot be used for constructors
class Shape {
  public:
    static Shape square(int len, int breadth);
    static Shape rectangle(int len, int breadth);
  private:
    Shape(int len, int breadth) {
        len_ = len;
        breadth_ = breadth;
    }
    int len_;
    int breadth_;
};

