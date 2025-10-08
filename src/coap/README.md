\## CoAP Server

\## Setup

* Change working directory where the CoAP files are saved:

```

cd C:\\Users\\archi\\Downloads\\DataFiles

```

* Create a new isolated python environment:

```

python -m venv coap\_env

```

* Activate the virtual environment so the installed libraries apply only inside it:

```

coap\_env\\Scripts\\activate

```

* Install the aiocoap library inside the virtual environment to enable CoAP protocol functionality:

```

pip install aiocoap

```

* Run the CoAP server python script that listens for and responds to CoAP requests:

```

C:\\Users\\archi\\Downloads\\DataFiles\\coap\_server.py

```

\## CoAP Client

\## Setup

* Move into the project folder where CoAP files are stored:

```

cd C:\\Users\\archi\\Downloads\\DataFiles

```

* Activate the virtual Python environment to use the installed aiocoap library:

```

coap\_env\\Scripts\\activate

```

* Run the CoAP client script to request files from the server and log transfer times and throughputs:

```

python coap\_client\_logging.py

```



\## CoAP Results

\## Setup

* Open project folder containing all CoAP files:

```

cd C:\\Users\\archi\\Downloads\\DataFiles

```

* Activate the virtual environment:

```

coap\_env\\Scripts\\activate

```

* Run the analysis script:

```

python coap\_analyze\_results.py

```









