#include "fred.hpp"

class FredPtr {
public:
  Fred* operator-> () { return p_; }
  Fred& operator* ()  { return *p_; }
  FredPtr(Fred* p)    : p_(p) { ++p_->count_; }  // p must not be null
 ~FredPtr()           { if (--p_->count_ == 0) delete p_; }
  FredPtr(const FredPtr& p) : p_(p.p_) { ++p_->count_; }
  FredPtr& operator= (const FredPtr& p)
        { // DO NOT CHANGE THE ORDER OF THESE STATEMENTS!
          // (This order properly handles self-assignment)
          // (This order also properly handles recursion, e.g., if a Fred contains FredPtrs)
          Fred* const old = p_;
          p_ = p.p_;
          ++p_->count_;
          if (--old->count_ == 0) delete old;
          return *this;
        }
private:
  Fred* p_;    // p_ is never NULL
};