import shutil
import pygame
import sys
import os
import json
from pygame.locals import *
from MovingBackground import BG
from Player import Player
from Floor import Floor
import platform
import urllib.request
import zipfile
from Tiles import Tiles


# import code
# code.interact(local=globals())
# from AppKit import NSBundle

# # NOT path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dummy.json")
# path = NSBundle.mainBundle().pathForResource_ofType_("dummy", "json")

DontPurge = False
SoundSystem = True
ShowIcon = False
Debug = True

pygame.init()  # initialize pygame

# print(os.name)
# print(platform.system())
# and platform.system() == "Darwin"
if not os.path.exists(os.getcwd() + "/assets"):
    pathToZip = os.getcwd() + "/assets.zip"
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'ARCHER_PROD/Platformy')
    opener.retrieve(
        "https://server.superarcherg.com/assets", pathToZip)
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

clock = pygame.time.Clock()
scaleModifier = 1
screenwidth, screenheight = (800*scaleModifier, 800*scaleModifier)
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


levelid = '0'


def GetLevel(id):
    levelid = str(id)
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'ARCHER_PROD/Platformy')
    opener.addheader('id', str(id))
    PATH_TO_LEVEL_DATA = os.getcwd() + '/tmp/' + str(id)
    opener.retrieve('https://server.superarcherg.com/info?id=' +
                    str(id), PATH_TO_LEVEL_DATA + '.info')
    opener.retrieve('https://server.superarcherg.com/data?id=' +
                    str(id), PATH_TO_LEVEL_DATA + '.data')
    opener.retrieve('https://server.superarcherg.com/owner?id=' +
                    str(id), PATH_TO_LEVEL_DATA + '.owner')
    text = open(PATH_TO_LEVEL_DATA+'.info', 'r')
    owner = open(PATH_TO_LEVEL_DATA+'.owner', 'r')
    jsonFile = json.loads(text.read())
    LEVEL_NAME = jsonFile['Name']
    LEVEL_OWNER = jsonFile['Creator']
    opener.retrieve('https://server.superarcherg.com/icon?id=' +
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
    Ox = Px * Ux
    Oy = Py * Uy

    time = clock.tick(framerate) / 1000.0
    x, y = pygame.mouse.get_pos()

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
        Debug = not Debug
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
    prevXY = (Px, Py)
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
    colliding = Tiles.IsColliding(Px, Py, screen, Debug)
    if colliding:
        direct = Tiles.GetDir()
        if direct == 1:
            Px = prevXY[0]
            Vx = 0
        else:
            Py = prevXY[1]
            Vy = 0
            Grounded = True
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
    pygame.display.update()
