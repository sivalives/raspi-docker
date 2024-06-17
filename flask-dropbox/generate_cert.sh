#!/bin/bash

CERT_DIR="/app/certs"
KEY_FILE="$CERT_DIR/key.pem"
CERT_FILE="$CERT_DIR/cert.pem"

# Create certs directory if it doesn't exist
mkdir -p $CERT_DIR

# Generate self-signed SSL certificate
openssl req -x509 -nodes -newkey rsa:4096 -keyout $KEY_FILE -out $CERT_FILE -days 365 -subj "/CN=example.com"