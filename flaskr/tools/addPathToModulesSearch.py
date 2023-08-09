import sys
import os
sys.path.append( os.getcwd() ) # where setup.py is
from flaskr.lib.get_local_ip import get_local_ip

print(get_local_ip(), os.getcwd())




