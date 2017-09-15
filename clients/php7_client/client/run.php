<?php
    require('core/api.php');

    $host = array_key_exists('WORLD_NAME', $_ENV) ? $_ENV['WORLD_NAME'] : "127.0.0.1";
    $port = 8000;

    class Client {
        function __construct($solution_id) {
            $this->solution_id = $solution_id;
            $this->sock = NULL;
        }

        public function connect($host, $port) {
            $adress =  $host.":".$port;
            $this->sock = stream_socket_client("tcp://".$adress, $errno, $errstr,
                $flags=STREAM_CLIENT_ASYNC_CONNECT|STREAM_CLIENT_CONNECT);
            stream_set_blocking($this->sock, false);

            if (!$this->sock) {
                echo "$errstr ($errno)\n";
            } else {
                $msg = array("solution_id" => $this->solution_id);
                $this->send_message($msg);

                $read = array($this->sock);
                $write = NULL;
                $except = NULL;
                $result = stream_select($read, $write, $except, 1000);
                if (!$result) {
                    fclose($this->sock);
                    return;
                }

                $data = json_decode(fgets($this->sock));
                if (array_key_exists('message', $data) && $data->message == 'beginning') {
                    $this->strategy_loop();
                }
            }
        }

        private static function dump_message($message) {

            $result = json_encode($message)."\n";
            // echo $result;
            return $result;
        }

        private function strategy_loop() {
            $api = new Api();
            $data = '';
            $read = array($this->sock);
            $write = NULL;
            $except = NULL;

            while (1) {
                $result = stream_select($read, $write, $except, 1000);
                try {
                    $buffer = fgets($this->sock);
                    $data = $data.$buffer;

                    $jsonData = json_decode($data);
                    if (!empty($jsonData)) {
                        if (array_key_exists('message', $jsonData) && $jsonData->message == 'down') {
                            break;
                        }
                        $turn = $api->turn($jsonData);
                        $this->send_message($turn);
                        $data = '';
                    }
                } catch (Exception $e) {
                    echo $e.'\n';
                    break;
                }
            }
            fclose($this->sock);
        }


        public function send_message($message) {
            $msg = $this->dump_message($message);
            return fwrite($this->sock, $msg);
        }
    }

    $solution_id = array_key_exists('SOLUTION_ID', $_ENV) ? $_ENV['SOLUTION_ID'] : 1;
    $client = new Client($solution_id);
    $client->connect($host, $port);
?>
