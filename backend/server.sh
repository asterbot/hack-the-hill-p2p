#!/bin/bash

while :
do
	python main.py
    if [ $? -ne 0 ]; then
        continue
    fi
	sleep 1
done

