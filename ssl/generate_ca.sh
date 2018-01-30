#! /bin/sh
#
# generate_ca.sh
# Copyright (C) 2018 gaspar_d <>
#
# Distributed under terms of the MIT license.
#

# Generate Root CA
openssl req -new -nodes  -x509 -days 3650  -newkey rsa:2048 -keyout ca.key -out ca.crt -config ca.cnf

# Generate Intermediate CA
openssl req -nodes -new -newkey rsa:2048 -keyout  ia.key -out ia.csr -config ia.cnf
openssl x509 -req -days 3650 -in ia.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out ia.crt -extfile ia.cnf  -extensions v3_ca

# Generate PEM from signed certificates
cat ca.crt ia.crt > ca.pem 
