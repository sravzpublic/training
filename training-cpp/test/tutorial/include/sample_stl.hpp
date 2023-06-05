// Components in STL
/*
    Containers
    Algorithms
    Iterators
    Functions Objects
    Adapters
*/

#include <iostream>
#include <algorithm>

void sort_array() {
    int a[] = {5,6,7,0,1};
    std::sort(std::begin(a), std::end(a));
    std::cout << "Sorted array: ";
    for (int i : a) {
        std::cout << i << " ";
    }
    std::cout << "\n";

}