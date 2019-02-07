#!/bin/bash
display_usage() {
    echo -e "\nUsage:\ntest.01.sh -n <number-of-runs> <hostname:port>"
}

if [  $# -le 1 ] 
	then 
		display_usage
		exit 1
	fi

if [[ ( $# == "--help") ||  $# == "-h" ]] 
	then 
		display_usage
		exit 0
	fi 

echo -e "Sending to" http://$3/api/v1.0/documents/convert $2 times

time for i in $(seq 1 $2);
do
    find ../examples -name '*' -type f -exec curl -F file=@{} http://$3/api/v1.0/documents/convert \;
done