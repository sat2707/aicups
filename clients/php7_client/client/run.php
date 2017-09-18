<?php

require_once('core/api.php');

$host = array_key_exists('WORLD_NAME', $_ENV) ? $_ENV['WORLD_NAME'] : "127.0.0.1";
$port = 8000;

/**
 * Client class
 */
class Client {
    
    /**
     *
     * @var integer
     */
    public $solutionId;

    /**
     * 
     * @param integer $solutionId
     */
    function __construct($solutionId) {
        $this->solutionId = $solutionId;
        $this->sock = NULL;
    }

    /**
     * Creates socket and starts strategy loop
     * @param string $host
     * @param integer $port
     */
    public function connect($host, $port) {
        $adress = $host . ":" . $port;
        $this->sock = stream_socket_client("tcp://" . $adress, $errno, $errstr, $flags = STREAM_CLIENT_ASYNC_CONNECT | STREAM_CLIENT_CONNECT);
        stream_set_blocking($this->sock, false);

        if (!$this->sock) {
            echo "$errstr ($errno)\n";
        } else {
            $msg = array("solution_id" => $this->solutionId);
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
                $this->strategyLoop();
            }
        }
    }

    /**
     * Convert message from array to 
     * @param array $message
     * @return string
     */
    private static function dumpMessage($message) {

        $result = json_encode($message) . "\n";
        return $result;
    }

    /**
     * Main loop
     */
    private function strategyLoop() {
        $api = new Api();
        $data = '';
        $read = [$this->sock];
        $write = NULL;
        $except = NULL;

        while (1) {
            $result = stream_select($read, $write, $except, 1000);
            try {
                $buffer = fgets($this->sock);
                $data = $data . $buffer;

                $jsonData = json_decode($data);
                if (!empty($jsonData)) {
                    if (array_key_exists('message', $jsonData) && $jsonData->message == 'down') {
                        break;
                    }
                    $turn = $api->turn($jsonData);
                    $this->sendMessage($turn);
                    $data = '';
                }
            } catch (Exception $e) {
                echo $e . '\n';
                break;
            }
        }
        fclose($this->sock);
    }

    /**
     * Convert and send message array to socket
     * @param array $message
     * @return integer
     */
    public function sendMessage($message) {
        $msg = $this->dumpMessage($message);
        return fwrite($this->sock, $msg);
    }

}

$solutionId = array_key_exists('SOLUTION_ID', $_ENV) ? $_ENV['SOLUTION_ID'] : 1;
$client = new Client($solutionId);
$client->connect($host, $port);
