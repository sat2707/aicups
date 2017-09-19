package API

import "fmt"

type Debug struct {
	message
}

func (d *Debug) Log(object interface{}) {
	cmd := make(map[string]interface{})
	cmd["text"] = fmt.Sprint(object)

	message := make(map[string]interface{})
	message["command"] = "log"
	message["args"] = cmd

	d.mMessages = append(d.mMessages, message)
}

func (d *Debug) Exception(object interface{}) {
	cmd := make(map[string]interface{})
	cmd["text"] = fmt.Sprint(object)

	message := make(map[string]interface{})
	message["command"] = "exception"
	message["args"] = cmd

	d.mMessages = append(d.mMessages, message)
}

func NewDebug() *Debug {
	return &Debug{}
}
