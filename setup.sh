#!/usr/bin/sh

python -m venv venv
# source venv/bin/activate  # On Linux/macOS
./venv/Scripts/activate  # On Windows

python.exe -m pip install --upgrade pip
python.exe -m pip install -r requirements.txt
