defmodule Strategy do
  # модуль стратегии - генсервер. на случай, если в стратегии
  # захочется хранить какое-то состояние между тиками
  use GenServer
  require Logger

  # Коды состояний лифтов ELEVATOR_STATE
  @timeout_check
  @waiting 0
  @moving  1
  @opening 2
  @filling 3 # забирает и/или высаживает пассажиров
  @closing 4

  # Коды состояний пассажиров PASSENGER_STATE
  @waiting_for_elevator 1 # ждет лифт
  @moving_to_elevator   2 # идет к лифту
  @returning            3 # возвращается обратно, если лифт уехал
  @moving_to_floor      4 # идет по лестнице
  @using_elevator       5 # едет в лифте
  @exiting              6 # выходит из лифта

  def on_tick(my_elevators, my_passengers, enemy_elevators, enemy_passengers) do
    Enum.map(my_elevators, fn(el) ->
                             Elevator.go_to_floor(el, 1)
                           end)
    hd(my_passengers)
    |> Passenger.set_elevator(hd(my_elevators))
  end

  def start_link() do
    GenServer.start_link(__MODULE__, %{}, name: __MODULE__)
  end

  def init(state) do
    Logger.info "Strategy init state=#{inspect state}"
    {:ok, state}
  end
end
