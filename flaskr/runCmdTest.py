import subprocess

# result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE) # linux shell
# result = subprocess.run(['cmd', '/c', 'dir'], stdout=subprocess.PIPE) # windows cmd
result = subprocess.run(['powershell', '/c', 'cat', 'setup.cfg'], stdout=subprocess.PIPE) # windows powershell
print(result.stdout.decode('utf-8'))