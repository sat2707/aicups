#include <iostream>
#include <algorithm>
#include <exception>
#include <vector>
#include <memory>

#include "csimplesocket/ActiveSocket.h"
#include "json.hpp"
#include "core/api.h"
#include "core/strategy.h"

using json = nlohmann::json;

const int PACKET_SIZE = 8096;

namespace
{
template<typename JSON>
void fill_passenger(Passenger &passenger, const JSON &jpassenger)
{
    passenger.id = jpassenger["id"];
    passenger.x = jpassenger["x"];
    passenger.y = jpassenger["y"];
    passenger.weight = jpassenger["weight"];
    passenger.from_floor = jpassenger["from_floor"];
    passenger.dest_floor = jpassenger["dest_floor"];
    passenger.time_to_away = jpassenger["time_to_away"];
    passenger.type = jpassenger["type"];
    passenger.floor = jpassenger["floor"];
    if (jpassenger["elevator"].is_null())
        passenger.elevator = - 1;
    else
        passenger.elevator = jpassenger["elevator"];
    passenger.state = jpassenger["state"];
}

template<typename JSON>
void fill_elevator(Elevator &elevator, const JSON &jelevator)
{
    elevator.id = jelevator["id"];
    elevator.y = jelevator["y"];
    elevator.speed = jelevator["speed"];
    elevator.time_on_floor = jelevator["time_on_floor"];
    elevator.next_floor = jelevator["next_floor"];
    elevator.type = jelevator["type"];
    elevator.floor = jelevator["floor"];
    elevator.state = jelevator["state"];

    for (auto && jpassenger : jelevator["passengers"])
    {
        elevator.passengers.emplace_back();
        ::fill_passenger(*elevator.passengers.rbegin(), jpassenger);
    }
}
}

class Client
{
public:

    Client(const std::string &host, int port, const std::string &solution_id)
        : host(host), port(port), solution_id(solution_id)
    {
        client.Initialize();
        client.DisableNagleAlgoritm();
    }

    ~Client()
    {
        client.Close();
    }

    bool open()
    {
        bool result = client.Open(host.c_str(), port);
        if (result)
        {
            json obj = {{"solution_id", solution_id}};
            std::string message = obj.dump() + "\n";
            send(message.c_str(), message.length());
        }
        return result;
    }

    int run()
    {
        std::string line;
        while(1)
        {
            int numBytes = client.Receive(PACKET_SIZE);
            if (numBytes <= 0)
            {
                std::cout << "Input closed" << std::endl;
                if (!line.empty())
                {
                    if (!doCommand(line))
                        return 0;
                }
                return -2;
            }

            uint8 * data = client.GetData();
            uint8 * data_end = data + numBytes;
            uint8 * endOfLine;
            while ((endOfLine = std::find(data, data_end, '\n')) < data_end)
            {
                line.append(data, endOfLine);
                if (!doCommand(line))
                    return 0;
                line.clear();
                data = endOfLine + 1;
            }

            line.append(data, data_end);
        }

        return 0;
    }

    bool doCommand(const std::string &line)
    {
        try
        {
            auto cmd = json::parse(line);

            if (cmd.count("message") && cmd["message"] == std::string("down"))
            {
                std::cout << "Down" << std::endl;
                return false;
            }

            if (!started)
            {
                if (cmd["message"] != std::string("beginning"))
                {
                    std::cerr << "Unknown command " << line << std::endl;
                    exit(-3);
                }

                started = true;
                strategy.reset(new Strategy());
                return true;
            }

            std::vector<Elevator> my_elevators;
            std::vector<Elevator> enemy_elevators;
            std::vector<Passenger> my_passengers;
            std::vector<Passenger> enemy_passengers;

            for (auto && jelevator : cmd["my_elevators"])
            {
                my_elevators.emplace_back();
                ::fill_elevator(*my_elevators.rbegin(), jelevator);
            }

            for (auto && jelevator : cmd["enemy_elevators"])
            {
                enemy_elevators.emplace_back();
                ::fill_elevator(*enemy_elevators.rbegin(), jelevator);
            }

            for (auto && jpassenger : cmd["my_passengers"])
            {
                my_passengers.emplace_back();
                ::fill_passenger(*my_passengers.rbegin(), jpassenger);
            }

            for (auto && jpassenger : cmd["enemy_passengers"])
            {
                enemy_passengers.emplace_back();
                ::fill_passenger(*enemy_passengers.rbegin(), jpassenger);
            }

            strategy->logs.clear();
            strategy->on_tick(my_elevators, my_passengers, enemy_elevators, enemy_passengers);

            messages = json::array();
            for (Elevator &elevator : my_elevators)
            {
                go_to_floor_commands(elevator);
            }

            for (Passenger &passenger : my_passengers)
            {
                set_elevator_to_passenger_commands(passenger);
            }

            for (Passenger &passenger : enemy_passengers)
            {
                set_elevator_to_passenger_commands(passenger);
            }

            log_commands(*strategy);

            std::string message = messages.dump() + "\n";
            send(message.c_str(), message.length());
            return true;
        }
        catch (...)
        {
            std::cerr << "Error while processing command " << line << std::endl;
            throw;
        }

        return false;
    }

private:
    CActiveSocket client;
    std::string host;
    int port;
    std::string solution_id;
    bool started = false;
    std::unique_ptr<Strategy> strategy;
    json messages;

    void go_to_floor_commands(Elevator &elevator)
    {
        for (int floor : elevator.go_to_floor_floors)
        {
            json obj = {
                {"command", "go_to_floor"},
                {   "args", {
                        {"elevator_id", elevator.id},
                        {"floor", floor}
                    }
                }
            };
            messages.push_back(obj);
        }
    }

    void set_elevator_to_passenger_commands(Passenger &passenger)
    {
        for (int set_elevator_id : passenger.set_elevator_ids)
        {
            json obj = {
                {"command", "set_elevator_to_passenger"},
                {   "args", {
                        {"passenger_id", passenger.id},
                        {"elevator_id", set_elevator_id}
                    }
                }
            };
            messages.push_back(obj);
        }
    }

    void log_commands(BaseStrategy &base_strategy)
    {
        for (std::pair<bool, std::stringstream> &log : base_strategy.logs)
        {
            json obj = {
                {"command", log.first ? "exception" : "log"},
                {   "args", {
                        {"text", log.second.str()}
                    }
                }
            };
            messages.push_back(obj);
        }
    }

    void send(const char *bytes, size_t byteCount) {
        unsigned int offset = 0;
        int sentByteCount;

        while (offset < byteCount && (sentByteCount = client.Send(reinterpret_cast<const uint8*>(bytes + offset), byteCount - offset)) > 0) {
            offset += sentByteCount;
        }

        if (offset != byteCount) {
            exit(10013);
        }
    }
};

int main()
{
    std::string host = "127.0.0.1";
    std::string solution_id = "-1";
    int port = 8000;
    const char* env_value;

    if ((env_value = std::getenv("WORLD_NAME")))
    {
        host = env_value;
    }
    if ((env_value = std::getenv("SOLUTION_ID")))
    {
        solution_id = env_value;
    }

    Client client(host, port, solution_id);
    if (!client.open())
    {
        std::cerr << "Error opening connection" << std::endl;
        return -1;
    }

    return client.run();
}
