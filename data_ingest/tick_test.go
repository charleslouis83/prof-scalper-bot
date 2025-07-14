package main

import (
	"context"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/gorilla/websocket"
)

// mockPublisher records published messages for assertions.
type mockPublisher struct {
	msgs []string
}

func (m *mockPublisher) Publish(ctx context.Context, channel string, message interface{}) error {
	switch v := message.(type) {
	case string:
		m.msgs = append(m.msgs, v)
	case []byte:
		m.msgs = append(m.msgs, string(v))
	default:
		return nil
	}
	return nil
}

func startWSServer(t *testing.T, messages []string) *httptest.Server {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		upgrader := websocket.Upgrader{}
		c, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			t.Fatal(err)
		}
		for _, msg := range messages {
			if err := c.WriteMessage(websocket.TextMessage, []byte(msg)); err != nil {
				t.Fatal(err)
			}
		}
		time.Sleep(100 * time.Millisecond)
	}))
	return server
}

func TestRunClientPublishesTicks(t *testing.T) {
	msgs := []string{`{"type":"trade"}`, `{"type":"depth"}`}
	srv := startWSServer(t, msgs)
	defer srv.Close()

	wsURL := "ws" + srv.URL[4:]
	mp := &mockPublisher{}
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	go runClient(ctx, wsURL, nil, mp)
	time.Sleep(200 * time.Millisecond)

	if len(mp.msgs) != len(msgs) {
		t.Fatalf("expected %d messages, got %d", len(msgs), len(mp.msgs))
	}
	for i, m := range msgs {
		if mp.msgs[i] != m {
			t.Errorf("message %d mismatch: got %s want %s", i, mp.msgs[i], m)
		}
	}
}
