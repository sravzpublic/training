// reference: https://www.geeksforgeeks.org/can-constructor-private-cpp/
// reference: https://isocpp.org/

#include "fred.hpp"
#include "sample_class.hpp"
#include <iostream>
#include "main.hpp"
#include "singleton.hpp"
#include "sample_stl.hpp"

using namespace std;

int main() {    
    // Shared pointer with reference counting
    std::cout << "Executing Tuturial" << std::endl;
    std::string s = "Hello World";
    // Test Sample class
    {
        std:: cout << "Sample class testing" << std::endl;
        Sample s1(1, s);
        Sample s2 = s1;
    }
    // Base class virtual destructor
    {
        std:: cout << "Virutal destructor testing" << std::endl;
        // If base class destructor is not virtual only base class destructor is called
        // Make base class destructor virtual and try again
        SampleBase *b = new SampleDerived();
        delete b;
    }
    // Private destructors
    // Private destructor works if an object is not created
    {


    }
    // Private constructors
    {
        std:: cout << "Private constructor testing" << std::endl;
        SampleBase2 sb2;
    }    
    // Singleton test
    {
        std::cout << "Singleton Test";
        singleton_test();
        Singleton* singleton = Singleton::GetInstance("BAR");
        // delete singleton; // Need not delete a singleton as it will be used the entire program life.
    }
    // Named constructor idiom
    {
        Shape squre = Shape::square(1,2);
        Shape rectangle = Shape::rectangle(1,2);
    }
    // STL Usage
    // Sort array
    sort_array();
} 