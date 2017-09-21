package core.API;

import org.json.simple.JSONObject;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Boris on 01.02.17.
 */
public class Debug implements MessagesInterface {
    private List<JSONObject> messages;

    public Debug(){
        messages = new ArrayList<>();
    }

    public void log(Object object) {
        JSONObject jo = new JSONObject();
        jo.put("command", "log");
        JSONObject args = new JSONObject();
        args.put("text", object.toString());
        jo.put("args", args);
        this.messages.add(jo);
    }

    public void exception(Object object) {
        JSONObject jo = new JSONObject();
        jo.put("command", "exception");
        JSONObject args = new JSONObject();
        args.put("text", object.toString());
        jo.put("args", args);
        this.messages.add(jo);
    }

    public List<JSONObject> getMessages() {
        List<JSONObject> _messages = this.messages;
        this.messages = new ArrayList<>();
        return _messages;
    }
}
