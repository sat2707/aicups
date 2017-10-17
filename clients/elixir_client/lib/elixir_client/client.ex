defmodule ElixirClient.Client do
  use GenServer
  require Logger

  def start_link(options) do
    GenServer.start_link(__MODULE__, options, name: __MODULE__)
  end

  def send_actions(json_actions) do
    :gen_server.cast(__MODULE__, {:send_actions, json_actions})
  end

  # Server Callbacks

  def init({host, port, solution_id} = options) do
    Logger.info "client init #{inspect options}"

    {:ok, socket} = :gen_tcp.connect(String.to_char_list(host),
                                     port, [:binary, {:packet, :line}, {:active, true}])

    json = Poison.encode!(%{solution_id: solution_id}) <> "\n"
    msg = String.to_char_list(json)
    :gen_tcp.send(socket, msg)

    {:ok, %{options: options, socket: socket, transmitting: false, sdata: ""}}
  end

  def handle_cast({:send_actions, json_actions}, state) do
    # Logger.info "client send_actions #{inspect json_actions}"
    json = Poison.encode!(json_actions) <> "\n"
    msg = String.to_char_list(json)
    :gen_tcp.send(state.socket, msg)    
    {:noreply, state}
  end

  def handle_info({:tcp, _port, msg}, state) do
    rcvd = state.sdata <> msg

    case String.contains?(rcvd, "\n") do
      true ->
        array_of_json = String.split(rcvd, "\n")
        # Logger.debug ">>>> array_of_json=#{inspect array_of_json}"
        # spawn(__MODULE__, :parse_jsons, [array_of_json])
        parse_jsons(array_of_json)

        {:noreply, %{state | sdata: List.last(array_of_json) }}
      _else ->
        {:noreply, %{state | sdata: rcvd }}
    end   
  end

  def handle_info({:data_to_decode, data}, state) do
    # Logger.info "handle_info data_to_decode data=#{inspect data}"
    json = Poison.decode!(data)
    handle_json(state, json)
    # {:noreply, state}
  end

  def handle_info(_msg, state) do
    # Logger.info "handle_info msg=#{inspect msg}"

    {:noreply, state}
  end

  def parse_jsons([""]) do
    ""
  end
  def parse_jsons([not_ended_tail]) do
    not_ended_tail
  end
  def parse_jsons([head | tail]) do
    send(self(), {:data_to_decode, head})
    parse_jsons(tail)
  end

  defp handle_json(state, %{"message" => "beginning"} = _json) do
    Logger.info "client beginning"
    {:noreply, %{state | transmitting: true}}
  end

  defp handle_json(state, %{"message" => "down"} = _json) do
    Logger.info "client down"
    :gen_tcp.close(state.socket)
    {:noreply, %{state | socket: nil, transmitting: false}}
  end

  # сообщение не beginning и не down
  defp handle_json(state, json) do
    # Logger.info "client rcv json=#{inspect json}"
    ElixirClient.Api.generate_actions(json)
    {:noreply, state}
  end

end