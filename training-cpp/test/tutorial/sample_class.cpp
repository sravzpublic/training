#include "sample_class.hpp"
#include <iostream>
#include <cstring>

// Copy constructor definition
Sample::Sample(const Sample &s) {
    std::cout << "Copy consturctor called" << std::endl;
    i_ = s.i_;
    size_ = strlen(s.s_);
    this->s_ = new char[s.size_ + 1];
    strcpy(this->s_, s.s_);    
}

// Destructor declaration is needed when we use pointers, file handlers etc
Sample::~Sample() {
    delete[] s_;
    std::cout << "Destructor called!" << std::endl;    
}

// Named constructor idiom
Shape Shape::square(int len, int breadth) {
    return Shape(len, breadth);
}

Shape Shape::rectangle(int len, int breadth) {
    return Shape(len, breadth);
}

std::string const Shape::s = "Hello world"; // Non int, non compile time const initialization

// inline Matrix::Matrix(int rows, int cols):rows_(rows),cols_(cols) {
//     data_ = new int[rows_*cols_];
// }

// inline Matrix::~Matrix() {
//     delete[] data_;
// }


// inline int Matrix::operator()(int rows, int cols) {
//     return data_[rows*cols+cols];
// }

