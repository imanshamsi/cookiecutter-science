#!/bin/sh

set -e

# run doc server
echo "--> Start MKDocs Server ..."
mkdocs serve 0.0.0.0:8080
