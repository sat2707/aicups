defmodule Elevator do
  defstruct id: nil, y: nil, passengers: nil, state: nil,
            speed: nil, floor: nil, next_floor: nil,
            time_on_floor: nil, type: nil
  
  use ExConstructor
  # goToFloor
  def go_to_floor(elevator, floor) do
    cmd_map = %{command: "go_to_floor",
                args: %{
                  elevator_id: elevator.id,
                  floor: floor
                }}
    ElixirClient.Api.add_command(cmd_map)
  end
end

defmodule Passenger do
  defstruct id: nil, elevator: nil, x: nil, y: nil, state: nil,
            time_to_away: nil, from_floor: nil,
            dest_floor: nil, type: nil, floor: nil

  use ExConstructor
  def has_elevator(passenger) do
    passenger.elevator != nil
  end

  def set_elevator(passenger, elevator) do
    cmd_map = %{command: "set_elevator_to_passenger",
                args: %{
                  elevator_id: elevator.id,
                  passenger_id: passenger.id
                }}
    ElixirClient.Api.add_command(cmd_map)
  end
end


defmodule ElixirClient.Api do
  use GenServer
  require Logger

  def start_link() do
    GenServer.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  def init(:ok) do
    # Logger.info "api init"
    {:ok, %{commands: []}}
  end

  def generate_actions(json_actions) do
    # Logger.info "api generate_actions"
    :gen_server.cast(__MODULE__, {:generate_actions, json_actions})
  end

  def add_command(command) do
    # Logger.info "api generate_actions"
    :gen_server.cast(__MODULE__, {:add_command, command})
  end

  def get_state() do
    # Logger.info "api generate_actions"
    :gen_server.call(__MODULE__, :get_state)
  end

  def handle_cast({:generate_actions, json_actions}, state) do
    # Logger.info "api generate_actions rcv json=#{inspect json_actions}"

    # обработка входящих и генерация исходящих
    my_elevators = ElixirClient.Api.parse_elevators(json_actions["my_elevators"])
    my_passengers = ElixirClient.Api.parse_passengers(json_actions["my_passengers"])
    enemy_elevators = ElixirClient.Api.parse_elevators(json_actions["enemy_elevators"])
    enemy_passengers = ElixirClient.Api.parse_passengers(json_actions["enemy_passengers"])

    Strategy.on_tick(my_elevators, my_passengers, enemy_elevators, enemy_passengers)

    array_actions = Enum.reverse(state.commands)

    # отправка
    ElixirClient.Client.send_actions(array_actions)
  
    {:noreply, %{state | commands: [] }}
  end

  def handle_cast({:add_command, command}, state) do
    # Logger.info "api generate_actions rcv json=#{inspect json_actions}"
 
    {:noreply, %{state | commands: [command] ++ state.commands}}
  end

  def handle_call(:get_state, _from, state) do
    {:reply, Enum.reverse(state.commands), state}
  end

  def parse_elevators(data) do
    Enum.map(data, fn(el) ->
                     new_el = Elevator.new(el)
                     %{new_el | passengers: parse_passengers(new_el.passengers)}
                   end)
  end

  def parse_passengers(data), do: Enum.map(data, &Passenger.new(&1))

end
