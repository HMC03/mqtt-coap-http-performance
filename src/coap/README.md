## CoAP Server

## Setup

* Change the directory of COAP, if it hasn't already been cloned:

```bash
cd src/coap
```

* Create a new isolated python environment:

```bash
# Note: Preferably, you would be in your project root directory.
python -m venv .venv
```

* Activate the virtual environment so the installed libraries apply only inside it:

```bash
source .venv/bin/activate
```

* Install the aiocoap library inside the virtual environment to enable CoAP protocol functionality:

```bash
pip install aiocoap
```

* Run the CoAP server python script that listens for and responds to CoAP requests:

```bash
# Note: Change to the coap directory
cd src/coap

# Run the server script
python3 coap_server.py
```

## CoAP Client

## Setup

* Run the CoAP client script to request files from the server and log transfer times and throughputs:

```bash
# Note: Make sure you are still in the coap directory
python3 coap_client_logging.py
```

## CoAP Results

* Run the analysis script:

```bash
# Note: Again, make sure your virtual environment is activated and you are in the coap directory.
python3 coap_analyze_results.py
```









