#! /bin/sh
#
# generate_cert.sh
# Copyright (C) 2018 gaspar_d <>
#
# Distributed under terms of the MIT license.
#

usage() {
  echo "usage:   $0 <hostname> <ip>"
  echo "example: $0 jaguar.localdomain 10.0.0.0"
  echo "options:"
  echo "  - <hostname> hostnamed that will be used for CN and alt Name"
  echo "  - <ip> ip specified in alt name"
}

LHOSTNAME=$1; shift 1
LIP=$1; shift 1

if [ -z "$LHOSTNAME" ] || [ -z "$LIP" ]; then
  usage
  exit 1
fi

if [ ! -f "ia.key" ] || [ ! -f "ia.crt" ]; then
  echo "Error: Missing intermediate authority"
  exit 1
fi

sed -i .orig "s/^commonName.*$/commonName=$LHOSTNAME/" cert.cnf
sed -i .orig "s/^DNS\\.1.*$/DNS\\.1=$LHOSTNAME/"       cert.cnf
sed -i .orig "s/^IP\\.1.*$/IP\\.1=$LIP/"               cert.cnf

# Generate Certificate Request
openssl req -new -newkey rsa:2048 -keyout cert.key -out cert.csr -config cert.cnf -nodes

# Signed Certificate Request with CA
openssl x509 -req -days 3650 -in cert.csr -CA ia.crt -CAkey ia.key -CAcreateserial -out cert.crt -extfile cert.cnf -extensions v3_req

# Generate PEM from signed certificates
cat cert.key cert.crt > cert.pem
