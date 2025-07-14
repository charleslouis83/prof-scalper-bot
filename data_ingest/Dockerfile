FROM golang:1.20-alpine
WORKDIR /app
COPY . .
RUN go build -o /app/data_ingest
CMD ["/app/data_ingest"]
