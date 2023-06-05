// https://isocpp.org/wiki/faq/freestore-mgmt
class FredPtr;
class Fred {
public:
  Fred() : count_(0) /*...*/ { }  // All ctors set count_ to 0 !
  // ...
private:
  friend class FredPtr;     // A friend class
  unsigned count_;
  // count_ must be initialized to 0 by all constructors
  // count_ is the number of FredPtr objects that point at this
};
