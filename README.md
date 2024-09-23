# Maciassdopia
Discord backdoor creator

## In first case you need to run right file
Windows:
```setup.ps1```
Linux:
```chmod +x ./setup.sh```
```sudo ./setup.sh```

## Initializing project (windows)
I recommend using python virtual enviromend. You can create your own by running command:
```py -3 -m venv .venv```
Then you need to active your venv:
```.\.venv\Scripts\Activate.ps1```
After that type (for installing all dependencies):
```py -m pip install -r requrements.txt```
Now project is ready for the build.

## Initializing project (linux)
I recommend using python virtual enviromend. You can create your own by running command:
```python3 -m venv .venv```
If there is an error with missing venv run:
```sudo apt install python3-venv```
Then you need to active your venv:
```source .venv/bin/activate```
After that type (for installing all dependencies):
```python -m pip install -r requrements.txt```
Now project is ready for the build.

## Building project (windows)
If u want to build the project, just type:
```py .\builder.py```
Or for linux:
```python ./builder.py```

This is our new project named Maciassdopia >:)
