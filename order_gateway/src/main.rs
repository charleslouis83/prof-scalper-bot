use order_gateway::start_server;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "0.0.0.0:50051".parse()?;
    println!("OrderGateway listening on {}", addr);
    start_server(addr).await
}
