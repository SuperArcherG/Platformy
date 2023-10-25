#!/usr/bin/env python3

import os
import git
import shutil



STABLE = True
if not STABLE:
    print("Release is not marked as STABLE...")
    print("Deleting current version and reinstalling...")
    folder_to_delete = os.path.join(os.getcwd(), "Platformy-Server")
    shutil.rmtree(folder_to_delete, ignore_errors=True)
    print("Uninstalled Successfully! \n")

direct = os.getcwd() + "/Platformy-Server/"
if not os.path.exists(os.getcwd() + "/Platformy-Server"):
    print("Server Not Installed!")
    print("Installing...")
    git.Git(direct).clone("https://github.com/SuperArcherG/Platformy-Server.git")
    print("Installed Successfully! \n")
else:
    print("Server Already Installed! \n")

def create_lock_file():
    with open("server.lock", "w") as lock_file:
        lock_file.write("Server is running")

create_lock_file()

print("Running Server")

import subprocess

script_path = os.getcwd() + "/Platformy-Server/server.py"

try:
    subprocess.run(["python3", script_path])
except Exception as e:
    print("An error occurred")
