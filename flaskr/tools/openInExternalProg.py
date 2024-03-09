import subprocess
from tkinter import filedialog

fileName = filedialog.askopenfilename()
subprocess.run(['cmd', '/c', "C:\ProgramFiles\HxD\HxD.exe", fileName], stdout=subprocess.PIPE, shell=True)
