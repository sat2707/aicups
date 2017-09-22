#ifndef API_H
#define API_H

#include <string>
#include <vector>

class Elevator;

class Passenger {
public:
    int id;             // идентификатор
    double x, y;           // координаты
    double weight;
    int from_floor, dest_floor; // этаж появления и цели
    int time_to_away;
    std::string type;
    int floor;
    int elevator;    // идентификатор назначенного лифта
    int state;

    bool has_elevator() const
    {
        return elevator != -1;
    }

    int get_last_set_elevator_id() const
    {
        if (!set_elevator_ids.empty())
            return *set_elevator_ids.rbegin();
        return -1;
    }

    void set_elevator(const Elevator& elevator) const;
private:
    mutable std::vector<int> set_elevator_ids;
    friend class Client;
};

class Elevator {
public:
    int id;
    double y;
    std::vector<Passenger> passengers;
    double speed;
    int time_on_floor;
    int next_floor;
    std::string type;
    int floor;
    int state;

    int get_last_go_to_floor() const
    {
        if (!go_to_floor_floors.empty())
            return *go_to_floor_floors.rbegin();
        return -1;
    }

public:
    void go_to_floor(int floor) const;

private:
    mutable std::vector<int> go_to_floor_floors;
    friend class Client;
};

inline void Passenger::set_elevator(const Elevator &elevator) const
{
    set_elevator_ids.push_back(elevator.id);
}

inline void Elevator::go_to_floor(int floor) const
{
    go_to_floor_floors.push_back(floor);
}

#endif // API_H
