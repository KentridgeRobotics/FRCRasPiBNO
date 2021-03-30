#!/usr/bin/env bash

VIRTUAL_ENV_DIR=".bno-tables-env"

if [[ ! -d "$VIRTUAL_ENV_DIR" ]]; then
    
    echo "Could not find virtual environment, setting up..."
    if ! command -v virtualenv > /dev/null; then
       echo "ERROR: Could not find virtualenv, please ensure it is installed."
       printf "\tsudo apt-get install python3-virtualenv\n"
       exit 1
    fi

    virtualenv -p /usr/bin/python3 "$VIRTUAL_ENV_DIR"

    # Activate environment
    source "$VIRTUAL_ENV_DIR"/bin/activate
    pip install -r requirements.txt
else
    echo "Virtual environment already found. Nothing to do."
fi


