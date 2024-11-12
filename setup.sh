#!bin/bash

projectDir=$(git rev-parse --show-toplevel)
frontendDir="$projectDir/frontend"
backendDir="$projectDir/backend"
currentDir=$(pwd)

cd "$frontendDir" 
npm i

cd "$backendDir" 
python3.9 -m venv venv 
source venv/bin/activate 
pip install -r requirements.txt
mkdir sources
mkdir uploads

cd "$currentDir"
