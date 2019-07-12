import os
import platform

sysstr = platform.system()

if sysstr == "Linux":
    os.system('virtualenv venv --python=python3')
    os.system(
        './venv/bin/pip install -r ./requirements.txt')
else:
    os.system('virtualenv venv')
    os.system(
        '.\\venv\\Scripts\\pip.exe install -r .\\requirements.txt')
