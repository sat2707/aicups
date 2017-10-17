defmodule ElixirClient.Test do
  use ExUnit.Case

  test "elevator_json" do
    elevator_map = Poison.decode!(elevator_json())

    elevator = Elevator.new(elevator_map)

    # IO.puts "elevator_json=#{inspect elevator_json}"
    # IO.puts "elevator_map=#{inspect elevator_map}"
    # IO.puts "elevator=#{inspect elevator}"
  end

  test "passenger_json" do
    passenger_map = Poison.decode!(passenger_json())

    passenger = Passenger.new(passenger_map)

    # IO.puts "passenger_json=#{inspect passenger_json}"
    # IO.puts "passenger_map=#{inspect passenger_map}"
    # IO.puts "passenger=#{inspect passenger}"
  end

  test "passengers" do
    pj = passenger_json()
    passengers_json = "[#{pj},#{pj}]"
    passengers_array = Poison.decode!(passengers_json)
    passengers = passengers_array
    |> Enum.map(&Passenger.new(&1)) 

    # IO.puts "passengers_json=#{inspect passengers_json}"
    # IO.puts "passengers_array=#{inspect passengers_array}"
    # IO.puts "passengers=#{inspect passengers}"
  end

  test "to_client" do
    {:ok, to_cli_json} = File.read("./priv/to_cli.json")

    # далее - такой же код, как будет в приеме данных от сервера
    json_actions = Poison.decode!(to_cli_json)

    my_elevators = ElixirClient.Api.parse_elevators(json_actions["my_elevators"])
    my_passengers = ElixirClient.Api.parse_passengers(json_actions["my_passengers"])
    enemy_elevators = ElixirClient.Api.parse_elevators(json_actions["enemy_elevators"])
    enemy_passengers = ElixirClient.Api.parse_passengers(json_actions["enemy_passengers"])

    array_actions = Strategy.on_tick(my_elevators, my_passengers, enemy_elevators, enemy_passengers)

    commands = ElixirClient.Api.get_state()
    IO.puts "commands = #{inspect commands}"


    # IO.puts "my_elevators = #{inspect my_elevators}"
    # IO.puts "enemy_elevators = #{inspect enemy_elevators}"
    # IO.puts "my_passengers = #{inspect my_passengers}"
    # IO.puts "enemy_passengers = #{inspect enemy_passengers}"

    # IO.puts "array_actions = #{inspect array_actions}"

  end

  test "from_client" do
    {:ok, from_cli_json} = File.read("./priv/from_cli.json")
    json_actions = Poison.decode!(from_cli_json)
    # IO.puts "from_cli_json = #{inspect from_cli_json}"
    IO.puts "json_actions = #{inspect json_actions}"
  end

  defp elevator_json() do
    """
      {
        \"id\":1,
        \"y\":2,
        \"passengers\":3,
        \"state\":4,
        \"speed\":5,
        \"floor\":6,
        \"next_floor\":7,
        \"time_on_floor\":8,
        \"type\":9
      }

    """
  end

  defp passenger_json() do
    """
      {
        \"id\":1,
        \"elevator\":2,
        \"x\":3,
        \"y\":4,
        \"state\":5,
        \"time_to_away\":6,
        \"from_floor\":7,
        \"dest_floor\":8,
        \"type\":9,
        \"floor\":10
      }
    """
  end

end
