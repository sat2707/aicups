using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;
using Newtonsoft.Json.Linq;
using System.IO;
using Api;

// State object for receiving data from remote device.

public class main {
	static int port = 8000;
	static StreamReader reader;
	static StreamWriter writer;

	public static void StrategyLoop () {
		api api = new api ();

		while (true)
		{
			var data = reader.ReadLine ();
			var json = JObject.Parse(data);

			var message = json.GetValue ("message");

			if (message != null && (string)message == "down") {
				break;
			}
			JArray turn = api.turn (json);
			String state = turn.ToString().Replace("\n", String.Empty);
			writer.WriteLine (state);
			writer.Flush ();
		}
	}


	public static int Main(String[] args) {
		String host = Environment.GetEnvironmentVariable ("WORLD_NAME");
		if (host == null) {
			host = "127.0.0.1";
		}

		String solutionId = Environment.GetEnvironmentVariable ("SOLUTION_ID");
		if (solutionId == null) {
			solutionId = "1";
		}

		IPHostEntry ipHostInfo = Dns.Resolve(host);
		IPAddress ipAddress = ipHostInfo.AddressList[0];
		IPEndPoint remoteEP = new IPEndPoint(ipAddress, port);

		// Create a TCP/IP socket.
		Socket client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
		client.Connect (remoteEP);
		NetworkStream myNetworkStream = new NetworkStream(client);
		reader = new StreamReader (myNetworkStream);
		writer = new StreamWriter (myNetworkStream);
		writer.AutoFlush = true;

		writer.WriteLine (String.Format("{{\"solution_id\":{0}}}", solutionId));

		var data = reader.ReadLine ();

		var json = JObject.Parse(data);
		var message = (string)json.GetValue("message");

		if (message == "beginning") {
			StrategyLoop ();
		}
			
		return 0;
	}
}
