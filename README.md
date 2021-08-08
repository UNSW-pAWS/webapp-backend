# Configuration and Dependency Checking Tools

<br/>

<p align="center">
  <img width="200" src="./static/logo.png">
</p>


<br/>
<br/>

This is the core service of our Configuration and Dependency Checking application.

## Table of Contents
1. [Location of physical api gateway] (#Location-of-physical-api-gateway)
2. [Developer Guide](#developer-guide)
    1. [How to run](#how-to-run)
    2. [Local Imports aren't being resolved in vscode?](#running-with-docker)
    3. [Deployment](#deployment)
3. [User Guide](#user-guide)

## Location of physical api gateway
The following is where our live api gatway is located
```https://paws-backend.link/```

## Developer Guide

### How to run:
1. `sudo apt-get install python3-venv` (if needed)
2. `python3 -m venv [environment-name]`
3. `. [environment-name]/bin/activate` or `[environment-name]\Scripts\activate` (Windows)
4. If using vscode, ensure the correct interpretor is set
5. `python -m pip install --upgrade pip`
6. `pip install -r requirements.txt`
7. Navigate to `/src` and run `python -m flask run`

Note: .gitignore will ensure your .vscode and venv folders do not get accidentally committed

### Local Imports aren't being resolved in vscode?
If you use pylance as your python engine, you may have to add `"python.analysis.extraPaths": ["./src"]` to your settings.json inside the .vscode folder

### Deployment
The tool has been deployed onto AWS using AWS Elastic Beanstalk. To deploy, follow the steps below:

1. In your virtual env, install the EB CLI and verify that it is installed correctly.
    ```    
    pip install awsebcli --upgrade
    eb --version
    ```
2. Get your API Key and Secret from your AWS console and update your credentials in `~/.aws/config`.
3. Follow the commands mentioned below, replacing the region with your selected region. 
    ```    
    eb init -p python-3.6 flask-tutorial — region ap-southeast-2
    eb init
    eb create flask-env
    eb open
    ```   
4. Now your flask application has been deployed! To terminate follow the commands below: 
    ```    
    eb terminate flask-env
    ```

---


## Tests
We have conducted both unit and integration tests in `/src/tests`
