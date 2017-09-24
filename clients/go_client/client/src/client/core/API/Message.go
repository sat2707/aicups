package API

type message struct {
	mMessages []interface{}
}

func (m *message) Messages() []interface{} {
	messages := m.mMessages
	m.mMessages = []interface{}{}
	return messages
}
