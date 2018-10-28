#!/bin/bash
display_usage() {
    echo -e "\nUsage:\ntest.01.sh <hostname:port>"
}

if [  $# -le 0 ] 
	then 
		display_usage
		exit 1
	fi

if [[ ( $# == "--help") ||  $# == "-h" ]] 
	then 
		display_usage
		exit 0
	fi 

time for i in {1..10};
do
    find ../examples -name '*' -type f -exec curl -F file=@{} http://$1/api/v1.0/documents/convert \;
done