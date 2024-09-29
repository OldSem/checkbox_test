#!/bin/bash

# Check arguments
if [ -z "$1" ]; then
    ENV_FILE="./.env"
    echo "Path to .env did not send, use default: $ENV_FILE"
else
    ENV_FILE=$1
fi

# Make sure, that certain file exists
if [ -f "$ENV_FILE" ]; then
    # Read variables from .env file
    export $(grep -v '^#' "$ENV_FILE" | xargs)
    #echo $(grep -v '^#' "$ENV_FILE" | xargs)
    echo $(grep -v '^#' "$ENV_FILE" | xargs).
    # Display variables from .env file
    #echo "Reading variables:"
    #echo $ENV_FILE
    #cat $ENV_FILE | grep -v '^#'
else
    echo "Error: file $ENV_FILE not found!"
    exit 1
fi
