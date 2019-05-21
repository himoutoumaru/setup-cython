import os
import platform

os.system('virtualenv --python=python3 venv')
sysstr = platform.system()
if sysstr == "Linux":
    os.system('./venv/bin/pip -r requirements.txt')
else:
    os.system('./venv/Scripts/pip.exe -r requirements.txt')
