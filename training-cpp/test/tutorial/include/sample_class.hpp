#include <iostream>
#include <cstring>

using namespace std;


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
    static const std::string s; //  = "Hello World";
    static const int i = 0;
  private:
    Shape(int len, int breadth) {
        len_ = len;
        breadth_ = breadth;
    }
    int len_;
    int breadth_;
};

// Consturct on first use idiom to prevent static initialization faisco

// Explicit keyword on constructor
struct ExplicitA
{
    ExplicitA(int) { }      // converting constructor
    ExplicitA(int, int) { } // converting constructor (C++11)
    operator bool() const { return true; }
};
 
struct ExplicitB
{
    explicit ExplicitB(int) { }
    explicit ExplicitB(int, int) { }
    explicit operator bool() const { return true; }
};

// Enable explicit constructor for classes with pointer data
struct ExplicitConstructor {

};

// class Handle {
// private:
//     std::string name;
//     ExplicitConstructor* p;
// public:
//     Handle(string n)
//         :name(n), p(0) { /* acquire X called "name" and let p point to it */ }
//     ~Handle() { delete p; /* release X called "name" */ }
//     // ...
// };
// void f(const string& hh)
// {
//     Handle h1(hh);
//     Handle h2 = h1; // leads to disaster!
//     // ...
// }

// Derived clases with custom assignment operator
class SampleBaseAssignmentOperator {
  public:
    SampleBaseAssignmentOperator()
    { 
      std::cout << "Constructing base" << std::endl; 
    }    
    SampleBaseAssignmentOperator& operator= (SampleBaseAssignmentOperator& sb) {
        std::cout << "Sample Base Assignment Operator called" << std::endl;
        return *this;
    } 
    virtual ~SampleBaseAssignmentOperator()
    { 
      std::cout<< "Destructing base" << std::endl; 
    }    
};
 
class SampleDerivedAssignmentOperator: public SampleBaseAssignmentOperator {
  public:
    SampleDerivedAssignmentOperator()    
     { 
        std::cout << "Constructing derived" << std::endl; 
     }
    SampleDerivedAssignmentOperator& operator= (SampleDerivedAssignmentOperator& sb) {
        std::cout << "SampleDerived Assignment Operator called" << std::endl;
        // SampleBaseAssignmentOperator::operator= (sb);
        return *this;
    } 
    ~SampleDerivedAssignmentOperator()
    { 
        std::cout << "Destructing derived" << std::endl; 
    }
};

// Create an array backed matrix with () operator overloaded to access an element
// class Matrix {
//   public:
//     Matrix(int rows, int cols);
//     int operator() (int row, int col);      
//     ~Matrix();    
//   private:
//     int rows_;
//     int cols_;
//     int *data_;
// };

class BadIndex : public std::exception {
    public:
    BadIndex(std::string msg) : message(msg) {}
    std::string what () {
            return message;
    }
    private:
    std::string message;    
};

class Matrix {
public:
  Matrix(unsigned rows, unsigned cols);
  double& operator() (unsigned row, unsigned col);        // Subscript operators often come in pairs
  double  operator() (unsigned row, unsigned col) const;  // Subscript operators often come in pairs
  // ...
 ~Matrix();                              // Destructor
  Matrix(const Matrix& m);               // Copy constructor
  Matrix& operator= (const Matrix& m);   // Assignment operator
  // ...
private:
  unsigned rows_, cols_;
  double* data_;
};

inline
Matrix::Matrix(unsigned rows, unsigned cols)
  : rows_ (rows)
  , cols_ (cols)
//, data_ ← initialized below after the if...throw statement
{
  if (rows == 0 || cols == 0)
    throw BadIndex("Matrix constructor has 0 size");
  data_ = new double[rows * cols];
}
inline
Matrix::~Matrix()
{
  delete[] data_;
}
inline
double& Matrix::operator() (unsigned row, unsigned col)
{
  if (row >= rows_ || col >= cols_)
    throw BadIndex("Matrix subscript out of bounds");
  return data_[cols_*row + col];
}
inline
double Matrix::operator() (unsigned row, unsigned col) const
{
  if (row >= rows_ || col >= cols_)
    throw BadIndex("const Matrix subscript out of bounds");
  return data_[cols_*row + col];
}

// Create a linked list
