#!/bin/bash

echo "This sets a cluster up with a PEM as a base64 secret, which goes along with scripts/dcos-pem.sh"
echo "Getting cert from host (make sure this is ONLY IP / hostname - not http://.. ): $1"
openssl s_client -showcerts -connect $1:443 </dev/null 2>/dev/null|openssl x509 -outform PEM > ./dcos.pem
openssl base64 -in dcos.pem -out dcos.pem.64 


