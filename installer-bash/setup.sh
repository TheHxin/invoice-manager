#! /bin/bash

root = $(pwd)

echo "Fetching back-end"
mkdir ./back-end
cd ./back-end
git clone https://github.com/TheHxin/invoice-manager.git

echo "Setting back-end up"
python3 -m venv .venv && source .venv/bin/activate
pip install -r req.txt

echo "Starting back-end"
cd source
uvicorn main:app --port 38532


cd root

echo "Fetching front-end"
mkdir ./front-end
cd ./front-end
git clone https://github.com/TheHxin/invoice-manager-front.git
