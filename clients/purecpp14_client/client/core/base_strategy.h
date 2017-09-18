#ifndef BASE_STRATEGY_H
#define BASE_STRATEGY_H

#include <vector>
#include <string>
#include <sstream>
#include <utility>

class BaseStrategy
{
private:
    std::vector<std::pair<bool/*is exception*/, std::string>> logs;
    friend class Client;
public:
    template <typename T>
    void log(T &&smth)
    {
        std::stringstream oss;
        oss << smth;
        logs.push_back(std::make_pair(false, oss.str()));
    }

    template <typename T>
    void exception(T &&smth)
    {
        std::stringstream oss;
        oss << smth;
        logs.push_back(std::make_pair(true, oss.str()));
    }
};

#endif // BASE_STRATEGY_H
