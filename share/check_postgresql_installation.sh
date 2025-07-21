#!/bin/bash

# PostgreSQL'in yüklü olduğundan emin olun
if !command -v psql &> /dev/null
then
    echo "PostgreSQL kurulu değil. Lütfen PostgreSQL'i kurun ve tekrar deneyin. - from: $0"
    exit 1
else 
    echo "PostgreSQL Sistemde Yüklü. - from: $0"
    exit 0

fi