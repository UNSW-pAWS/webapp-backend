# Webapp Backend

> This is the backend for our Dependency Scrubbing Web App

## Steps to set up environment

1. `sudo apt-get install python3-venv` (if needed)
2. `python3 -m venv [environment-name]`
3. `. [environment-name]/bin/activate`
4. If using vscode, ensure the correct interpretor is set
5. `python -m pip install --upgrade pip`
6. `pip install -r requirements.txt`
7. navigate to /src
8. run `python -m flask run`

Note: .gitignore will ensure your .vscode and venv folders do not get accidentally committed

#### Local Imports aren't being resolved in vscode?
If you use pylance as your python engine, you may have to add `"python.analysis.extraPaths": ["./src"]` to your settings.json inside the .vscode folder
