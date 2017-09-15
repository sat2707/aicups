defmodule ElixirClient.Api do
  use GenServer
  require Logger

  def start_link() do
    GenServer.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  def init(:ok) do
    Logger.info "api init"
    {:ok, %{}}
  end

  def generate_actions(json_actions) do
    Logger.info "api generate_actions"
    :gen_server.cast(__MODULE__, {:generate_actions, json_actions})
  end

  def handle_cast({:generate_actions, json_actions}, state) do
    Logger.info "api generate_actions rcv json=#{inspect json_actions}"

    # обработка входящих и генерация исходящих
    my_elevators = json_actions["my_elevators"]
    my_passengers = json_actions["my_passengers"]
    enemy_elevators = json_actions["enemy_elevators"]
    enemy_passengers = json_actions["enemy_passengers"]

    array_actions = Strategy.on_tick(my_elevators, my_passengers, enemy_elevators, enemy_passengers)

    # отправка
    ElixirClient.Client.send_actions(array_actions)
  
    {:noreply, state}
  end

end
