# Introduction

This automation script is used to automate onboarding clients process to invite clients and IBMers in the co-execution phase through running this python script.

Alternative method is to leverage IBM Cloud GUI

## Prerequists

You will need Python 3, Your Personal Access Token of the Github repo that you stored, a new IBM internal repo, your IBM Cloud IAM API Key, your IBM Cloud Account ID

## Instructions

The steps are quite easy and straight forward:

1. You will need to create a new internal IBM repo

2. You will need to create an excel sheet in the repo you created in Step 1 and note down the excel sheet name

3. You will need to create a environment file called .env

![Sample .env setup](./environmentVariable.png?raw=true ".env")


## Run

1. Install python dependencies
   ```bash
    pip3 install -r ./requirements.txt
   ```

2. Run this project
   ```bash
    python3 csv-client.py
   ```

3. Dockerize this project
   ```bash
    docker build -t automated-onboarding .
   ```
   run in interactive mode

   ```bash
    docker run -it automated-onboarding
   ```
## Documentation Links
   