#ifndef BASE_STRATEGY_H
#define BASE_STRATEGY_H

#include "api.h"

class BaseStrategy
{
private:
    Debug* debugPtr;

public:
    void set_debug(Debug& _debug) {
        debugPtr = &_debug;
    }

    template <typename T>
    void debug(T smth) { debugPtr->log(smth); }
};

#endif // BASE_STRATEGY_H
