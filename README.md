# Fault-Tolerant Key/Value Service


## Project Structure

```bash
bin #A folder to put your scripts (.bat for Windows or .sh for macOS and Linux)
images #A folder where to put the screenshots that you generate.
kv #A folder where to implement the key/value service
└── kvstorage.py #A Python script to implement an instance of the Key/Value Service. TO COMPLETE
└── kvstorage_http.py #A Python script to implement an HTTP server to interact with an instance of the Key/Value Service. TO COMPLETE
```

## Initialization

The Python Library PySyncObj (https://readthedocs.org/projects/pysyncobj/) will be used through the Assignment.

The library can be installed with:
```bash
pip install pysyncobj
```

Note: Python 3 should be used for this Assignment. If your command python is not for Python 3, please update it (or use python3 instead).

## Task 1: Discovering Raft

The website https://raft.github.io/ shows an interactive visualization of how Raft works for
a group of 5 servers, supporting a simple database with only one type of transaction.

Answer the questions about it in your Report.

## Task 2: Implementation of a Fault-Tolerant Key/Value Service with Raft

In this task, you should complete the Python scripts kvstorage.py and kvstorage_http.py, in the kv folder.

kvstorage.py is an implementation of a Raft server, implementing a key/value store. 

kvstorage_http.py is an HTTP server that enables interactions with a Raft server from kvstorage.py.

The script kvstorage_http.py takes the following parameters:

- The port for the HTTP server (e.g., 8080).
- The address of the Raft node (e.g., 127.0.0.1:6000)
- The next parameters are the addresses of the other Raft nodes (e.g., 127.0.0.1:6001)

To start the servers, use the scripts provided in the bin folder. These scripts should be run from the bin folder in different terminals.


On Windows

```bash
.\create_server0.bat #And the other numbers
```

On macOS and Linux
```bash


```bash
chmod +x create_server0.sh #And the other numbers
./create_server0.sh #And the other numbers
```

The API description for the HTTP servers is provided in api_description.yml

You can perform a PUT operation to the key/value service for key "a" with: 

POST https://localhost:8080/keys/a HTTP/1.1
Content-Type: application/json

{"type": "PUT",
"value": ["cat", "dog"]
}

You can perform an APPEND operation to the key/value service for key "a" with: 

POST https://localhost:8080/keys/a HTTP/1.1
Content-Type: application/json

{"type": "APPEND",
"value": "mouse"
}

You can perform a GET operation to the key/value service for key "a" with:

GET https://localhost:8080/keys/a HTTP/1.1

You can retrieve the status of node 0 with:

GET https://localhost:8080/admin/status HTTP/1.1

Complete Task 2 in the Report


# Task 3: Evaluation of the Key/Value Service

Complete Task 3 in the Report.

# Task 4: Questions on Raft

Answer the questions in the Report.