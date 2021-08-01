import os
from pathlib import Path

cwd = os.getcwd()
print(cwd) # C:\Users\yaniv\OneDrive\python-flask

path = Path('./')
print(path.resolve()) # C:\Users\yaniv\OneDrive\python-flask
new_path = path.resolve() / 'flaskr' / 'currentDir.py' 
print(new_path.resolve()) # C:\Users\yaniv\OneDrive\python-flask\flaskr\currentDir.py
print(new_path.exists()) # True
print(new_path.is_dir()) # False
with new_path.open() as f: print(f.readline()) # print - import os