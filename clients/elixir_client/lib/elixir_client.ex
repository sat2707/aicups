defmodule ElixirClient do
  use Application
  import Supervisor.Spec

  def start(_type, _args) do

    host  = case System.get_env()["WORLD_NAME"] do
      nil -> fatal_error("env WORLD_NAME not set")
      world_name -> world_name
    end

    solution_id  = case System.get_env()["SOLUTION_ID"] do
      nil -> fatal_error("env SOLUTION_ID not set")
      str_solution_id -> 
        {solution_id, _} = Integer.parse(str_solution_id)
        solution_id
    end

    IO.puts "Host: #{host}"
    ip = case :inet.gethostbyname(String.to_char_list(host)) do
      {:ok, {:hostent, _, [], :inet, 4, ip_list}} ->
        ip_list
        |> hd()
        |> :inet_parse.ntoa()
        |> to_string()
      {:error, :nxdomain} ->
        fatal_error("Can't determine host")
    end
    
    port = 8000

    IO.puts "IPv4 address: #{inspect ip}"
    IO.puts "Port: #{inspect port}"
    IO.puts "SOLUTION_ID: #{inspect solution_id}"

    childrens = [
      # Plug.Adapters.Cowboy.child_spec(:http, ElixirClient.Router, [], port: port),
      worker(ElixirClient.Api, []),
      worker(ElixirClient.Client, [{host, port, solution_id}])
    ]

    Supervisor.start_link(childrens, strategy: :one_for_one)
  end

  defp fatal_error(message) do
      IO.puts(message)
      throw(message)
  end
end
