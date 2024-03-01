# RAM Stats

Monitoring the statistics of RAM.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)


## Introduction

This is a very simple project which stores some stats (total, free, used) about your main memory every minute. Then provides an endpoint which gets n as a number and gives you the last n minutes usage stats. 

## Features

This project uses FastAPI as its core library to implement an endpoint for retrieving time series usage. 
There are two main classes for this purpose , the first one which is DataStore can be found in ram_utils file is the main way to make query over our sqlite db.
The other one is RAMStatsCollector which is responsible to collect usage statistics of RAM and report it.

The only http end-point of this project has been developed in main.py file and the project should be used by running this file. 
periodic_ram_usage async function has this purpose to get the report of ram usage and then store it on db every minute.

## Installation

You can use this project by simply installing its dependencies that can be found in requirements.txt file and then running main.py file:
Not to make settings.yml file with similar structure of settings.sample.yml file before running the project. 

```bash
# Clone the repository
git clone https://github.com/alimoosavi/RAMStats.git

# Navigate to the project directory
cd RAMStats

# Install dependencies
pip install -r requirements.txt

# Running server
python main.py
```

The other way is to just run the project using Dockerfile:
```bash 
    docker build -t ram-stats:v1.0 .
    docker run -p 8000:8000 ram-stats:v1.0
```

