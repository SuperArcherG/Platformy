#!/usr/bin/env python3

import subprocess as sp
import os
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import sys
import pygame
import shutil
import json
from pygame.locals import *
from MovingBackground import BG
from Player import Player
from Floor import Floor
import platform
import urllib.request
import zipfile
from Tiles import Tiles
import subprocess
import warnings
import time
import socket
import requests
import wget


RunLocalServer = False




def is_server_up(hostname, port):
    try:
        # Create a socket object
        with socket.create_connection((hostname, port), timeout=5) as sock:
            return True
    except (socket.timeout, socket.error):
        return False

# Set the server address and port
server_address = "play.superarcherg.com"
server_port = 81

# Check if the server is up
RunLocalServer = not is_server_up(server_address, server_port)

if RunLocalServer:
        
        
    import atexit

    # Define a function to be called on exit
    def on_exit():
        print("Closing...")
        print("Deleting Lock File")
        # Function to delete the lock file
        def delete_lock_file():
            try:
                os.remove("server.lock")
                print("Lock File Deleted")
            except FileNotFoundError:
                print("Lock file not found. It might have already been deleted.")
        delete_lock_file()
        
    atexit.register(on_exit)

    from PIL import Image
    import socket
    import psutil
    import time

    def find_process_by_port(port):
        for proc in psutil.process_iter(['pid', 'connections']):
            try:
                if proc.info['connections']:
                    for conn in proc.info['connections']:
                        if conn.laddr.port == port:
                            return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return None

    def kill_process_by_port(port):
        process = find_process_by_port(port)
        if process:
            print("Killing Server")
            try:
                process.terminate()
            except psutil.NoSuchProcess:
                pass  # Process might have already terminated

            # Give some time for the process to terminate
            time.sleep(2)

            # If the process is still alive, try killing forcefully
            if process.is_running():
                print("Killing Server")
                try:
                    process.kill()
                except psutil.NoSuchProcess:
                    pass  # Process might have already terminated
        else:
            print("No Servers Running")
    # Specify the port to kill processes on
    port_to_kill = 6050

    # Kill the process running on the specified port
    kill_process_by_port(port_to_kill)



    def get_local_ip():
        try:
            # Create a socket connection to an external server (doesn't actually connect)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Use a known external server (Google's public DNS server)
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            print("ERROR IN GETTING IP")
            return None
        
    ip = str(get_local_ip()) + ":6050"
    
            
    script_path = os.getcwd()+"/RunServerLocal.py"

    try:
        print("Starting Server...")
        # Run the script in the background
        subprocess.Popen(["sudo","python3", script_path])       
        # Continue with the rest of your current script
        print("Running Local Server in the Background")
    except:
        print("SERVER START ERROR")
        
    while not os.path.exists(os.getcwd()+"/server.lock"):
        time.sleep(1)
        print("Server Ping Fail")

    print("Waiting for server to start")
    time.sleep(3)
    print("Server has started")

    ip = "http://"+str(get_local_ip()) + ":6050"
else:
    ip = "http://play.superarcherg.com:81"

DontPurge = False
SoundSystem = True
ShowIcon = True
Debug = False
LDM = False

buffer1 = 1
buffer2 = 0

pygame.init()  # initialize pygame

try:
 pygame.mixer.init()
except:
 print("ERR Audio Mixer Failed to Initialize, Check That You Have the Proper Drivers Installed")
 SoundSystem = False

#print("OS: " + os.name)
#print("System: " + platform.system())
# and platform.system() == "Darwin"
if not os.path.exists(os.getcwd() + "/assets"):
    pathToZip = os.getcwd() + "/assets.zip"
    
    url =  ip+'/assets'
    URL = url
    response = wget.download(URL, pathToZip)


            
    with zipfile.ZipFile(pathToZip, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())
    os.remove("assets.zip")

if not os.path.exists(os.getcwd() + "/tmp/"):
    os.mkdir(os.getcwd()+"/tmp/")

PATH_TO_LEVEL_DATA = os.getcwd() + '/tmp/' + '0'
LEVEL_NAME = 'No Name'
LEVEL_OWNER = 'No Name'

Icon = pygame.image.load(os.getcwd() + "/assets/images/promo/SlimeCover.png")
pygame.display.set_icon(Icon)


font = pygame.font.SysFont("Arial", 18)
resolution = 400
clock = pygame.time.Clock()
scaleModifier = 1
screenwidth, screenheight = (resolution*scaleModifier, resolution*scaleModifier)
screen = pygame.display.set_mode(
    (screenwidth, screenheight), pygame.SCALED, vsync=1)
pygame.display.set_caption("Level Select")
Ux, Uy = (screenwidth / 16, screenheight / 16)
Uo = (-Ux/2, +Uy/2)
Uo = (0, 0)
worldSizeX = (-100, 100)
worldSizeY = (0, 100)
# Set the framerate
framerate = 60
parralax = 1/3
movementUpdate = 10

playerSpeed = 1.5
jumpForce = 2.5
# xDrift = 1.1
xDrift = 10
gravity = 0.2
Grounded = True

if SoundSystem:
    jump = pygame.mixer.Sound(os.getcwd() + "/assets/audio/jump.wav")
    land = pygame.mixer.Sound(os.getcwd() + "/assets/audio/land.wav")

# player coordinates
Px, Py = 0, 0
Vx, Vy = 0, 0
Ox, Oy = 0, 0
# Load the background image here. Make sure the file exists!

Mountains = BG(screenwidth, screenheight, os.getcwd() +
               "/assets/images/background/BG.png")
L, R, U, D, N = os.getcwd() + "/assets/images/Player/L.png", os.getcwd() + "/assets/images/Player/R.png",  os.getcwd() + \
    "/assets/images/Player/U.png", os.getcwd() + "/assets/images/Player/D.png", os.getcwd() + \
    "/assets/images/Player/N.png"
Player = Player(L, R, U, D, N, screenwidth, screenheight, Uo)
Floor = Floor(screenwidth, screenheight,
              os.getcwd() + "/assets/images/tiles/Ground.png",  os.getcwd() +
              "/assets/images/tiles/DirtGround.png", Uo)
TileData = open(os.getcwd()+"/assets/placeholder/0.data", 'r')
Tiles = Tiles(TileData, os.getcwd() + "/assets/images/tiles/",
              screenheight, screenheight, Uo)
pygame.mouse.set_visible(0)
pygame.display.set_caption('Platformy')
pressedKeys = pygame.key.get_pressed()
pygame.mouse.set_visible(True)

img2 = pygame.image.load(
            os.getcwd() + "/tmp.png")


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


def DrawCollissionSquare(x, y):
    # Player Bounding Box
    pygame.draw.line(color="red", surface=screen, start_pos=(
        x-Ux/2, screenheight/2-Uy/2), end_pos=(x+Ux/2, screenheight/2-Uy/2), width=1)
    pygame.draw.line(color="red", surface=screen, start_pos=(
        x-Ux/2, screenheight/2+Uy/2), end_pos=(x+Ux/2, screenheight/2+Uy/2), width=1)
    pygame.draw.line(color="red", surface=screen, start_pos=(
        x-Ux/2, screenheight/2-Uy/2), end_pos=(x-Ux/2, screenheight/2+Uy/2), width=1)
    pygame.draw.line(color="red", surface=screen, start_pos=(
        x+Ux/2, screenheight/2-Uy/2), end_pos=(x+Ux/2, screenheight/2+Uy/2), width=1)
    

levelid = '0'


def GetLevel(id):
    
    PATH_TO_LEVEL_DATA = os.getcwd() + '/tmp/' + str(id)
    
    levelid = str(id)

    with open(PATH_TO_LEVEL_DATA+".info", mode="wb") as file:
        url =  ip + '/info?id=' + str(id)
        response = requests.get(url, stream=True)
        for chunk in response.iter_content(chunk_size=10 * 1024):
            file.write(chunk)
            
    with open(PATH_TO_LEVEL_DATA+".data", mode="wb") as file:
        url =  ip + '/data?id=' + str(id)
        response = requests.get(url, stream=True)
        for chunk in response.iter_content(chunk_size=10 * 1024):
            file.write(chunk)
            
    with open(PATH_TO_LEVEL_DATA+".owner", mode="wb") as file:
        url =  ip + '/owner?id=' + str(id)
        response = requests.get(url, stream=True)
        for chunk in response.iter_content(chunk_size=10 * 1024):
            file.write(chunk)

    with open(PATH_TO_LEVEL_DATA+".jpeg", mode="wb") as file:
        url =  ip+'/icon?id=' + str(id)
        response = requests.get(url, stream=True)
        for chunk in response.iter_content(chunk_size=10 * 1024):
            file.write(chunk)
    
    text = open(PATH_TO_LEVEL_DATA+'.info', 'r')
    owner = open(PATH_TO_LEVEL_DATA+'.owner', 'r')
    jsonFile = json.loads(text.read())
    LEVEL_NAME = jsonFile['Name']
    LEVEL_OWNER = jsonFile['Creator']

            
    pygame.display.set_caption(
        LEVEL_NAME + " by " + LEVEL_OWNER + " Uploaded by " + owner.read() + ' ID:' + levelid)
        
    img2 = pygame.image.load(
        PATH_TO_LEVEL_DATA + ".jpeg")
        
    pygame.display.set_icon(img2)
    Tiles.UpdateData(open(PATH_TO_LEVEL_DATA + '.data', 'r'))
    return levelid

levelid = GetLevel(1)

PATH_TO_LEVEL_DATA = os.getcwd() + '/tmp/' + levelid

prevXY = (0, 0)


# update loop
while True:

    Ox = Px * Ux
    Oy = Py * Uy

    time = clock.tick(framerate) / 1000.0
    MouseX, MouseY = pygame.mouse.get_pos()

    # Handle quiting of the game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shutil.rmtree(os.getcwd()+"/tmp")
            if not DontPurge:
                try:
                    shutil.rmtree(os.getcwd() + "/assets")
                except (PermissionError):
                    0
            sys.exit()
    old = pressedKeys
    pressedKeys = pygame.key.get_pressed()  # checking pressed keys
    if (pressedKeys[pygame.K_0]):
        Px, Py, Vx, Vy = 0, 3, 0, 0
    if (pressedKeys[pygame.K_r]):
        levelid = GetLevel(1)
    if (old[pygame.K_F3] != pressedKeys[pygame.K_F3]):
        buffer1 += 1
        if buffer1 == 2:
         Debug = not Debug
         buffer1 = 0
    if (old[pygame.K_F4] != pressedKeys[pygame.K_F4]):
        buffer2 += 1
        if buffer2 == 2:
         LDM = not LDM
         buffer2 = 0
    U, D, L, R = old[pygame.K_UP] != pressedKeys[pygame.K_UP] and pressedKeys[
        pygame.K_UP] != 0, pressedKeys[pygame.K_DOWN], pressedKeys[pygame.K_LEFT], pressedKeys[pygame.K_RIGHT]
    if U and Grounded:
        Vy = jumpForce
        Grounded = False
        if SoundSystem:
            jump.play()
    if L:
        Vx = -playerSpeed
    if R:
        Vx = playerSpeed
    Vy -= gravity

    if (abs(Vx) < 0.01):
        Vx = 0

    Px += Vx / framerate * movementUpdate
    Py += Vy / framerate * movementUpdate    # Limits
    Px = max(min(Px, worldSizeX[1]), worldSizeX[0])
    if (max(Py, worldSizeY[0]) == 0):
        Py = 0
        Vy = 0
        if not Grounded and SoundSystem:
            land.play()
        Grounded = True
    if not L and not R and Grounded:
        Vx = 0
    else:
        Vx = Vx / xDrift
    currXY = (Px, Py)
    
    update_fps()

    # Draw calls
    # Set new Background Coordinates and update the screen
    screen.fill((0, 0, 0))
    
    t1,t2=prevXY
    colliding = Tiles.IsColliding(Px, Py, t1, t2, Debug)
    
    if colliding:
        if not Grounded and SoundSystem:
            land.play()
        Grounded = True

    
    ppx = 0
    ppy = 0
    
    Cx = Tiles.correctedX(Px, Py, t1, t2, Debug)
    Cy = Tiles.correctedY(Px, Py, t1, t2, Debug)
    #Cy = Py
    
    if Cx != Px:
        Px = Cx
        ppx = prevXY[0]
        Vx = 0
    else:
        ppx = Px
        
    if Cy != Py:
        Py = Cy
        ppy = prevXY[1]
        Vy = 0
    else:
        ppy = Py   
    
    prevXY = (ppx, ppy)

    if not LDM:
        Mountains.UpdateCoords(parralax, -Ox, Oy)
        Mountains.Show(screen)
        Floor.Show(screen, Px, Py, Ux, Uy)
    else:
        screen.blit(font.render("LDM Enabled", 1, pygame.Color("coral")),(10, 0))
        pygame.draw.line(color="green", surface=screen, start_pos=(0,screenheight/2+Uy/2+Py*Uy), end_pos=(screenwidth, screenheight/2+Uy/2+Py*Uy), width=1)

    Tiles.Show(screen, Px, Py, Ux, Uy, Uo)
    Player.Show(screen, Vx, Vy, pressedKeys[pygame.K_DOWN])
    
    if levelid != '0' and ShowIcon and not LDM:
        scale = 2
        screen.blit(img2, (screenwidth-Ux*scale, 0))
    
    clock.tick(60)

    if Debug:
        DrawCollissionSquare(screenwidth/2, screenheight/2)
        screen.blit(update_fps(), (10, 0))
        pygame.draw.line(color="red", surface=screen, start_pos=(0,screenheight/2+Uy/2+Py*Uy), end_pos=(screenwidth, screenheight/2+Uy/2+Py*Uy), width=1)

    pygame.display.update()
