#!/bin/bash

echo "";echo "Starting Imports";echo "";
python3 -m pip install -r requirements.txt
echo "";echo "Starting Program";echo "";
python3 Task1/webService.py
