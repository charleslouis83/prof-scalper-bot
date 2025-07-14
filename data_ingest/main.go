package main

import (
	"context"
	"log"
	"os"
	"time"

	"github.com/gorilla/websocket"
	"github.com/redis/go-redis/v9"
)

// Publisher interface allows publishing messages to a channel
// This abstraction enables testing without a real Redis server.
type Publisher interface {
	Publish(ctx context.Context, channel string, message interface{}) error
}

// redisPublisher implements Publisher using go-redis.
type redisPublisher struct {
	client *redis.Client
}

func (r *redisPublisher) Publish(ctx context.Context, channel string, message interface{}) error {
	return r.client.Publish(ctx, channel, message).Err()
}

func newRedisPublisher() Publisher {
	addr := os.Getenv("REDIS_ADDR")
	if addr == "" {
		addr = "localhost:6379"
	}
	rdb := redis.NewClient(&redis.Options{Addr: addr})
	return &redisPublisher{client: rdb}
}

// runClient connects to the websocket url, sends subscription messages and
// forwards all incoming messages to the Publisher on channel "ticks".
func runClient(ctx context.Context, url string, subs []string, pub Publisher) error {
	c, _, err := websocket.DefaultDialer.Dial(url, nil)
	if err != nil {
		return err
	}
	defer c.Close()

	for _, s := range subs {
		if err := c.WriteMessage(websocket.TextMessage, []byte(s)); err != nil {
			return err
		}
	}

	for {
		_, msg, err := c.ReadMessage()
		if err != nil {
			return err
		}
		if err := pub.Publish(ctx, "ticks", msg); err != nil {
			log.Println("publish error:", err)
		}
	}
}

func main() {
	pub := newRedisPublisher()
	ctx := context.Background()

	binanceURL := os.Getenv("BINANCE_WS")
	if binanceURL == "" {
		binanceURL = "wss://stream.binance.com:9443/ws/btcusdt@trade"
	}
	bybitURL := os.Getenv("BYBIT_WS")
	if bybitURL == "" {
		bybitURL = "wss://stream.bybit.com/v5/public/spot"
	}

	go func() {
		subs := []string{"{\"op\":\"subscribe\",\"args\":[\"trade.BTCUSDT\",\"orderbook.1.BTCUSDT\"]}"}
		if err := runClient(ctx, bybitURL, subs, pub); err != nil {
			log.Println("bybit error:", err)
		}
	}()

	subs := []string{"{\"method\":\"SUBSCRIBE\",\"params\":[\"btcusdt@trade\",\"btcusdt@depth@100ms\"],\"id\":1}"}
	if err := runClient(ctx, binanceURL, subs, pub); err != nil {
		log.Println("binance error:", err)
	}

	// keep running
	for {
		time.Sleep(time.Minute)
	}
}
