FROM rust:slim as builder
WORKDIR /app
COPY . .
RUN cargo build --release

FROM debian:stable-slim
WORKDIR /app
COPY --from=builder /app/target/release/order_gateway /app/order_gateway
CMD ["/app/order_gateway"]
