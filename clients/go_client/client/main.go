package main

import (
	"encoding/json"
	"github.com/pomkac/aicups/clients/go_client/client/core/API"
	"fmt"
	"net"
	"bufio"
	"sync"
	"log"
	"os"
)

func main() {

	host := os.Getenv("WORLD_NAME")

	if host == "" {
		host = "127.0.0.1"
	}

	solutionId := os.Getenv("SOLUTION_ID")

	if solutionId == "" {
		solutionId = "-1"
	}

	loop(host, 8000, solutionId)
}

func getMessage(reader *bufio.Reader, jsonObject *interface{}) error{
	message, err := reader.ReadBytes('\n')

	if err != nil {
		return err
	}

	err = json.Unmarshal(message, &jsonObject)

	if err != nil || jsonObject == nil {
		log.Fatalf("JSON parse error: %s", err)
		return err
	}

	return nil
}

func loop(host string, port int, solutionId string) {
	var jsonPool = sync.Pool{}

	conn, err := net.Dial("tcp", fmt.Sprintf("%s:%d", host, port))

	if err != nil {
		log.Fatalf("Socket error: %s", err)
		return
	}

	defer conn.Close()

	reader := bufio.NewReader(conn)

	_, err = fmt.Fprintf(conn, `{"solution_id":"%s"}` + "\n", solutionId)

	if err != nil {
		log.Fatal("Can not send solution_id")
		return
	}

	api := API.NewAPI(&Strategy{})

	for {

		jsonObject := jsonPool.Get()

		if err := getMessage(reader , &jsonObject); err != nil{
			log.Fatalf("JSON parse error: %s", err)
			break
		}

		if cmd, ok := jsonObject.(map[string]interface{})["message"]; ok {
			if cmd.(string) == "down" {
				log.Println("Parsed down")
				break
			}
			if err := getMessage(reader , &jsonObject); err != nil{
				log.Fatalf("JSON parse error: %s", err)
				break
			}
		}

		jsonArray := api.Turn(jsonObject.(map[string]interface{}))

		res, _ := json.Marshal(jsonArray)

		conn.Write(res)
		conn.Write([]byte("\n"))

		jsonPool.Put(jsonObject)
	}
}
