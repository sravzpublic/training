// reference: https://www.geeksforgeeks.org/can-constructor-private-cpp/
// reference: https://isocpp.org/

#include "fred.hpp"
#include "sample_class.hpp"
#include <iostream>
#include "main.hpp"
#include "singleton.hpp"
#include "sample_stl.hpp"
#include "static1.hpp"
#include "static2.hpp"

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
    std::cout << "Array sort test" << std::endl;
    sort_array();

    // Assignment operator test
    // Derived class assignment operator is not called until explicitly called
    std::cout << "Derived call assignment operator test" << std::endl;
    {
        SampleDerivedAssignmentOperator sdao1;
        SampleDerivedAssignmentOperator sdao2;
        sdao2 = sdao1;
    }

    // Operator overloading: atleast one type should be a class/user defined time.
    // Cannot operator overload == on char since that will not include atleast 1 user defined type
    std::cout << "Matrix usage:" << std::endl;
    {
        Matrix m(2,2);
        // std::cout << m(1,2);
    }
} 