use order_gateway::Order;
use order_gateway::order_gateway::order_gateway_client::OrderGatewayClient;
use std::time::Duration;
use tokio_test::block_on;

#[test]
fn test_submit_order() {
    block_on(async {
        tokio::spawn(async {
            order_gateway::start_server("127.0.0.1:50051".parse().unwrap())
                .await
                .unwrap();
        });

        tokio::time::sleep(Duration::from_millis(100)).await;

        let mut client = OrderGatewayClient::connect("http://127.0.0.1:50051")
            .await
            .unwrap();

        let request = tonic::Request::new(Order {
            symbol: "BTCUSDT".into(),
            price: 0.0,
            quantity: 1.0,
        });

        let response = client.submit_order(request).await.unwrap();
        assert!(response.into_inner().success);
    });
}
