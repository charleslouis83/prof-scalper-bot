use tonic::{Request, Response, Status, transport::Server};

pub mod order_gateway {
    tonic::include_proto!("ordergateway");
}

use order_gateway::order_gateway_server::{OrderGateway, OrderGatewayServer};
pub use order_gateway::{Ack, CancelRequest, Order, Position, PositionQuery};

#[derive(Default)]
pub struct OrderGatewayService;

#[tonic::async_trait]
impl OrderGateway for OrderGatewayService {
    async fn submit_order(&self, _request: Request<Order>) -> Result<Response<Ack>, Status> {
        Ok(Response::new(Ack {
            success: true,
            message: "order submitted".into(),
        }))
    }

    async fn cancel_order(
        &self,
        _request: Request<CancelRequest>,
    ) -> Result<Response<Ack>, Status> {
        Ok(Response::new(Ack {
            success: true,
            message: "order cancelled".into(),
        }))
    }

    async fn query_position(
        &self,
        request: Request<PositionQuery>,
    ) -> Result<Response<Position>, Status> {
        let symbol = request.into_inner().symbol;
        Ok(Response::new(Position {
            symbol,
            quantity: 0.0,
        }))
    }
}

pub async fn start_server(addr: std::net::SocketAddr) -> Result<(), Box<dyn std::error::Error>> {
    let svc = OrderGatewayService::default();
    Server::builder()
        .add_service(OrderGatewayServer::new(svc))
        .serve(addr)
        .await?;
    Ok(())
}
