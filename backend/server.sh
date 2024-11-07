#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    command=python3
else
    command=python
fi

while :
do
	${command} main.py
    if [ $? -ne 0 ]; then
        continue
    fi
	sleep 1
done

