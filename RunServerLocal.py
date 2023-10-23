import os
import git

direct = os.getcwd() + "/Platformy-Server/"
if not os.path.exists(os.getcwd() + "/Platformy-Server"):
    print("Server Not Installed")
    print("Installing...")
    git.Git(direct).clone("https://github.com/SuperArcherG/Platformy-Server.git")
else:
    print("Server Already Installed!")
    
import subprocess

script_path = "/home/archer/Desktop/Github Desktop/Platformy/Platformy-Server/server.py"

try:
    subprocess.run(["python3", script_path])
except Exception as e:
    print(f"An error occurred: {e}")