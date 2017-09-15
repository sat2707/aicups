package core;


import core.API.API;
import org.json.simple.JSONAware;
import org.json.simple.JSONObject;
import org.json.simple.parser.ParseException;
import org.json.simple.parser.JSONParser;

import java.io.*;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;

/**
 * Created by Boris on 01.02.17.
 */
public class Client {
    private String host;
    private Integer port;
    private String solutionId;
    private JSONParser parser;
    private SocketChannel clientSocket;

    public Client(String host, Integer port, String solutionId) {
        this.host = host;
        this.port = port;
        this.solutionId = solutionId;
        this.parser = new JSONParser();
    }

    private JSONObject parseString(String jsonString) {
        try {
            return (JSONObject) parser.parse(jsonString);
        } catch (ParseException e) {
            return null;
        }
    }

    public void connect() throws IOException {
        this.clientSocket = SocketChannel.open(new InetSocketAddress(this.host, port));
        JSONObject obj = new JSONObject();
        obj.put("solution_id", solutionId);
        clientSocket.write(ByteBuffer.wrap(this.dumpMessage(obj).getBytes()));

        BufferedReader reader = new BufferedReader(new InputStreamReader(clientSocket.socket().getInputStream()));
        JSONObject message = parseString(reader.readLine());
        if (message == null) {
            System.exit(1);
        }
        if ((message.get("message")).equals("beginning")) {
            strategyLoop(reader);
        }
    }

    private void strategyLoop(BufferedReader reader) throws IOException {
        API api = new API();
        while (true) {
            JSONObject object = parseString(reader.readLine());
            if (object == null || (object.get("message") != null && object.get("message").equals("down"))) {
                break;
            }
            clientSocket.write(ByteBuffer.wrap(this.dumpMessage(api.turn(object)).getBytes()));
        }
    }

    private String dumpMessage(JSONAware object) {
        return object.toJSONString() + "\n";
    }
}
