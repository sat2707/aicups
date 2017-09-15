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

    json = Poison.encode!(%{solution_id: "#{solution_id}"})
    msg = String.to_char_list(json)
    :gen_tcp.send(socket, msg)

    {:ok, %{options: options, socket: socket, transmitting: false}}
  end

  def handle_cast({:send_actions, json_actions}, state) do
    Logger.info "client send_actions #{inspect json_actions}"
    json = Poison.encode!(json_actions)
    msg = String.to_char_list(json)
    :gen_tcp.send(state.socket, msg)    
    {:noreply, state}
  end

  def handle_info({:tcp, _port, msg}, state) do
    json = Poison.decode!(msg)
    handle_json(state, json)
  end

  def handle_info(msg, state) do
    Logger.info "handle_info msg=#{inspect msg}"

    {:noreply, state}
  end

  defp handle_json(state, %{"message" => "beginning"} = _json) do
    Logger.info "client beginning"
    {:noreply, %{state | transmitting: true}}
  end

  defp handle_json(state, %{"message" => "down"} = _json) do
    :gen_tcp.close(state.socket)
    {:noreply, %{state | socket: nil, transmitting: false}}
  end

  # сообщение не beginning и не down
  defp handle_json(state, json) do
    Logger.info "client rcv json=#{inspect json}"
    ElixirClient.Api.generate_actions(json)
    {:noreply, state}
  end

  defp handle_json(state, _json) do
    {:noreply, state}
  end

end