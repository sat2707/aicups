let net = require('net');
let world = process.env.WORLD_NAME || '127.0.0.1';
let port = 8000;
let solutionId = process.env.SOLUTION_ID || 1;
let client = new net.Socket();
let API = require('./core/api');
let api = new API.API();

client.connect(port, world, function() {
    client.write(JSON.stringify({'solution_id': solutionId}) + '\n');
});

let chunkReader = function (callback) {
    let chunk = "";
    return function (data) {
        chunk += data.toString();
        let dIndex = chunk.indexOf('\n');

        while (dIndex > -1) {
            try {
                let string = chunk.substring(0, dIndex);
                let json = JSON.parse(string);
                callback(json);
            } catch (err) {
                console.log(err);
            }
            chunk = chunk.substring(dIndex + 1);
            dIndex = chunk.indexOf('\n');
        }
    };
};

let began = false;

let loop = chunkReader(function (json) {
    if (began) {
        if (json.message == "down") {
            client.removeListener("data", loop);
            return
        }
        let turn = api.turn(json);
        client.write(JSON.stringify(turn) + '\n');
    } else if (json.message == "beginning") {
        began = true;
    } else {
        client.destroy();
    }
});

client.on('data', loop);
