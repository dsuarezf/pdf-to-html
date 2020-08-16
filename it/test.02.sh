#!/bin/bash

display_usage() {
    echo -e "\nUsage:\n`basename $0` -f <folder> -n <number-of-processes> <hostname:port>"
}

if [[ "$1" == "--help" ||  "$1" == "-h" ]]
	then
		display_usage
		exit 0
	fi

if [ $# -le 4 ]
	then
		display_usage
		exit 1
	fi

echo -e "Sending to" http://$5/api/v1.0/documents/convert $4 processes

time (
  for i in $(seq 1 $4);
  do
	find $2 -name '*' -type f -exec curl -F file=@{} http://$5/api/v1.0/documents/convert \; &
  done
  wait
)