#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]
then
  echo "Specify a username and hostname or IP. For example:"
  echo "  ./get_config.sh admin 10.0.0.1"
  exit 1
fi

echo -n "$1 password: " 1>&2
read -s PASSWORD
export PASSWORD
echo "" 1>&2

python get_config.py $1 $2 | tr -d "\r" | tail -n +2 | head -n -2
