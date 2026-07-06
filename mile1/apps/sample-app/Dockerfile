FROM golang:1.23-alpine AS builder
WORKDIR /app
COPY src/ .
RUN go build -o sample-app main.go

FROM alpine:3.20
WORKDIR /app
COPY --from=builder /app/sample-app .
EXPOSE 8080
CMD ["./sample-app"]