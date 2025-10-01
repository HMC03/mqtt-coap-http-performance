# HTTP

## Overview
This module contains the implementation of the HTTP protocol. 
Using the http.server library from Python, we can use a one-liner command to start a server.

The client is also implemented with Python. 
We will use the requests library to make HTTP request to the server and download the file from the server.
A timer will measure the time taken to download the file and calculate the throughput after all iterations.

## Build and Compile

### Prerequisites
- Python 3.x
- requests>=2.22.0
- python-dotenv>=0.10.3
- venv>=0.21.1

### Setting up the program 

**Note: This following steps are for bash terminal.**

#### Create your virtual environment
```bash
# Make sure you are in the project root directory of the repo.
python -m venv .venv

# Activate your virtual environment
source .venv/bin/activate
```

#### Install dependencies
```bash
# Install dependencies
pip install -r requirements.txt
```

#### Start your http server
Before starting the HTTP Server, make sure you are in the **root directory** of the project. 
Also, make sure you have **activated your virtual environment**.
```bash
# Feel free to change the port number.
python -m http.server 8000 --directory ./files
```

#### Create your .env file
```bash
# Change to the http directory
cd src/http

# Create your .env file
touch .env

# Add the following lines to your .env file
# Note: Make sure it start with "http://" and end with "/".
# Note: Verify the port number is correct.
SERVER_URL={your_server_url}
```

### Running the program
Verified that the server is running by opening your browser and navigating to the server url.
```bash
# You can either use your local ip address or "localhost".
# Note: Change the port number if you changed it in the previous step.
http://localhost:8000/
```

#### Run the client
```bash
# Change to the http directory
cd src/http

# Run the program
python client.py
```

