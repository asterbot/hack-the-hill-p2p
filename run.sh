#!/bin/bash

currentDir=$(pwd)
projectDir=$(git rev-parse --show-toplevel)
backendDir="$projectDir/backend"
frontendDir="$projectDir/frontend"

# Setting up frontend
cd "$frontendDir"

if [[ "$OSTYPE" == "linux-gnu"* ]]; then 
    gnome-terminal -- bash -c "npm run dev; exec bash" 
elif [[ "$OSTYPE" == "darwin"* ]]; then 
    osascript -e "tell app \"terminal\" to do script \"cd '$frontendDir' && npm run dev\""
fi


# Setting up backend
cd "$backendDir" 
source venv/bin/activate

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

cd "$currentDir"