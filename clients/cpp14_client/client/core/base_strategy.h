#ifndef BASE_STRATEGY_H
#define BASE_STRATEGY_H

#include <vector>
#include <string>
#include <sstream>
#include <utility>

class BaseStrategy
{
private:
    std::vector<std::pair<bool/*is exception*/, std::stringstream>> logs;
    friend class Client;
public:

    std::stringstream &log()
    {
        logs.push_back(std::make_pair(false, std::stringstream()));
        return logs.rbegin()->second;
    }

    std::stringstream & exception()
    {
        logs.push_back(std::make_pair(true, std::stringstream()));
        return logs.rbegin()->second;
    }
};

#endif // BASE_STRATEGY_H
