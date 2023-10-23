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



RunLocalServer = True

if RunLocalServer:
    from PIL import Image
    import socket
    def get_local_ip():
        try:
            # Create a socket connection to an external server (doesn't actually connect)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Use a known external server (Google's public DNS server)
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            print(f"An error occurred while getting the local IP: {e}")
            return None
        
    ip = str(get_local_ip()) + ":6050"
else:
    ip = "https://server.superarcherg.com:80"
DontPurge = True
SoundSystem = True
ShowIcon = True
Debug = True
buffer = 1
ip = 'http://192.168.0.126:6050'
pygame.init()  # initialize pygame

# print(os.name)
# print(platform.system())
# and platform.system() == "Darwin"
if not os.path.exists(os.getcwd() + "/assets"):
    pathToZip = os.getcwd() + "/assets.zip"
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'ARCHER_PROD/Platformy')
    opener.retrieve(ip + '/assets', pathToZip)
    with zipfile.ZipFile(pathToZip, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())
    os.remove(os.getcwd() + "/assets.zip")

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
    levelid = str(id)
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'ARCHER_PROD/Platformy')
    opener.addheader('id', str(id))
    PATH_TO_LEVEL_DATA = os.getcwd() + '/tmp/' + str(id)
    opener.retrieve(ip + '/info?id=' +
                    str(id), PATH_TO_LEVEL_DATA + '.info')
    opener.retrieve(ip + '/data?id=' +
                    str(id), PATH_TO_LEVEL_DATA + '.data')
    opener.retrieve(ip + '/owner?id=' +
                    str(id), PATH_TO_LEVEL_DATA + '.owner')
    text = open(PATH_TO_LEVEL_DATA+'.info', 'r')
    owner = open(PATH_TO_LEVEL_DATA+'.owner', 'r')
    jsonFile = json.loads(text.read())
    LEVEL_NAME = jsonFile['Name']
    LEVEL_OWNER = jsonFile['Creator']
    opener.retrieve(ip + '/icon?id=' +
                    str(id), PATH_TO_LEVEL_DATA + '.jpeg')
    pygame.display.set_caption(
        LEVEL_NAME + " by " + LEVEL_OWNER + " Uploaded by " + owner.read() + ' ID:' + levelid)
    img2 = pygame.image.load(
        PATH_TO_LEVEL_DATA + ".jpeg")
    pygame.display.set_icon(img2)
    Tiles.UpdateData(open(PATH_TO_LEVEL_DATA + '.data', 'r'))
    return levelid


levelid = GetLevel(1)
PATH_TO_LEVEL_DATA = os.getcwd() + '/tmp/' + levelid

# update loop
while True:
    prevXY = (Px, Py)

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
        buffer += 1
        if buffer == 2:
         Debug = not Debug
         buffer = 0

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
    Mountains.UpdateCoords(parralax, -Ox, Oy)
    Mountains.Show(screen)
    Floor.Show(screen, Px, Py, Ux, Uy)
    Tiles.Show(screen, Px, Py, Ux, Uy, Uo)
    screen.blit(update_fps(), (10, 0))
    t1,t2=prevXY
    colliding = Tiles.IsColliding(Px, Py, t1, t2, screen, Debug)
    if colliding:
        Py = prevXY[1]
        Px = prevXY[0]
        Vy = 0
        Vx = 0
        Grounded = True
    # REWRITE
    Player.Show(screen, Vx, Vy, pressedKeys[pygame.K_DOWN])
    if levelid != '0' and ShowIcon:
        img2 = pygame.image.load(
            PATH_TO_LEVEL_DATA + ".jpeg")
        scale = 2
        img2 = pygame.transform.scale(img2, (16*scale, 16*scale))
        img2 = pygame.transform.scale(img2, (Ux*scale, Uy*scale))
        img2.set_alpha(128)
        screen.blit(img2, (screenwidth-Ux*scale, 0))
    clock.tick(60)

    if Debug:
        DrawCollissionSquare(screenwidth/2, screenheight/2)

    pygame.display.update()
