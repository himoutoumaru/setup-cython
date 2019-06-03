import os
import platform

os.system('virtualenv venv')
sysstr = platform.system()

if sysstr == "Linux":
    os.system(
        './venv/bin/pip install -r ./requirements.txt')
else:
    os.system(
        '.\\venv\\Scripts\\pip.exe install -r .\\requirements.txt')
