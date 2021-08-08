# Configuration and Dependency Checking Tools

<br/>

<p align="center">
  <img width="200" src="./static/logo.png">
</p>


<br/>
<br/>

This is the core service of our Configuration and Dependency Checking application.

## Table of Contents
1. [Location of physical api gateway] (#location-api)
2. [Developer Guide](#developer-guide)
    1. [How to run](#how-to-run)
    2. [Local Imports aren't being resolved in vscode?](#running-with-docker)
    3. [Using eslint](#using-eslint)
    4. [Deployment](#deployment)
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

#### Local Imports aren't being resolved in vscode?
If you use pylance as your python engine, you may have to add `"python.analysis.extraPaths": ["./src"]` to your settings.json inside the .vscode folder

### Deployment
The tool has been deployed onto AWS using AWS Elastic Beanstalk. To deploy, follow the steps below:

1. Run the below command in the repository's directory.
    ```    
    cd ./
    set DISABLE_ESLINT_PLUGIN=true
    npm run build
    ```

---


## Tests
We have conducted both unit and integration tests in `/src/tests`
