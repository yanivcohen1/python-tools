import subprocess
import platform
import os
# result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE) # linux shell
# result = subprocess.run(['cmd', '/c', 'dir'], stdout=subprocess.PIPE) # windows cmd
# result = subprocess.run(['powershell', '/c', 'cat', 'setup.cfg'], stdout=subprocess.PIPE) # windows powershell

# for multiplatform run cmd.sh that contain #!/bin/bash ls -s"
# need in linux to "chmod u+x script.sh"
cwd = os.getcwd() # currect working dir
print(cwd)
if  platform.system() != "Windows":
    result = subprocess.run(['sh ./flaskr/cmd.sh', '/c/Temp'], stdout=subprocess.PIPE, shell=True)
else :
    result = subprocess.run(['sh', './flaskr/cmd.sh', 'C:/Temp'], stdout=subprocess.PIPE, shell=True)
print(result.stdout.decode('utf-8'))
