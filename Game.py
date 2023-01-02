import shutil
import pygame
import sys
import os
from pygame.locals import *
from MovingBackground import BG
from Player import Player
from Floor import Floor
import platform
import urllib.request
import zipfile

# import code
# code.interact(local=globals())
from AppKit import NSBundle

# NOT path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dummy.json")
path = NSBundle.mainBundle().pathForResource_ofType_("dummy", "json")

DontPurge = True
print(os.name)
print(platform.system())
# and platform.system() == "Darwin"
if not os.path.exists(os.getcwd() + "/assets"):
    pathToZip = os.getcwd() + "/assets.zip"
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'ARCHER_PROD/Platformy')
    filename, headers = opener.retrieve(
        "https://server.superarcherg.com/assets", pathToZip)
    with zipfile.ZipFile(pathToZip, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())

pygame.init()  # initialize pygame
font = pygame.font.SysFont("Arial", 18)

clock = pygame.time.Clock()
screenwidth, screenheight = (800, 800)
screen = pygame.display.set_mode(
    (screenwidth, screenheight), flags=pygame.SCALED, vsync=0)
Ux, Uy = (screenwidth / 16, screenheight / 16)

worldSizeX = (-100, 100)
worldSizeY = (0, 100)
# Set the framerate
framerate = 60
parralax = 0.5
movementUpdate = 10

playerSpeed = 1.5
jumpForce = 2.5
xDrift = 1.1
gravity = 0.2
Grounded = True

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
Player = Player(L, R, U, D, N, screenwidth, screenheight)
Floor = Floor(screenwidth, screenheight,
              os.getcwd() + "/assets/images/tiles/Ground.png",  os.getcwd() +
              "/assets/images/tiles/DirtGround.png")
pygame.mouse.set_visible(0)
pygame.display.set_caption('Platformy')
pressedKeys = pygame.key.get_pressed()
pygame.mouse.set_visible(True)


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


# update loop
while True:
    Ox = Px * Ux
    Oy = Py * Uy

    time = clock.tick(framerate) / 1000.0
    x, y = pygame.mouse.get_pos()

    # Handle quiting of the game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if not DontPurge:
                try:
                    os.remove(os.getcwd() + "/assets.zip")
                    shutil.rmtree(os.getcwd() + "/assets")
                except (PermissionError):
                    0
            sys.exit()
    old = pressedKeys
    pressedKeys = pygame.key.get_pressed()  # checking pressed keys
    U, D, L, R = old[pygame.K_UP] != pressedKeys[pygame.K_UP] and pressedKeys[
        pygame.K_UP] != 0, pressedKeys[pygame.K_DOWN], pressedKeys[pygame.K_LEFT], pressedKeys[pygame.K_RIGHT]
    if U and Grounded:
        Vy = jumpForce
        Grounded = False
        jump.play()
    # if D:
    #     Vy = -1
    if L:
        Vx = -playerSpeed
    if R:
        Vx = playerSpeed
    Vy -= gravity

    if (abs(Vx) < 0.01):
        Vx = 0

    Px += Vx / framerate * movementUpdate
    Py += Vy / framerate * movementUpdate

    # Limits
    Px = max(min(Px, worldSizeX[1]), worldSizeX[0])
    if (max(Py, worldSizeY[0]) == 0):
        Py = 0
        Vy = 0
        if not Grounded:
            land.play()
        Grounded = True

    if not L and not R and Grounded:
        Vx = 0
    else:
        Vx = Vx / xDrift

    update_fps()

    # Draw calls
    # Set new Background Coordinates and update the screen
    Mountains.UpdateCoords(parralax, -Ox, Oy)
    Mountains.Show(screen)
    Floor.UpdateCoords(Px, Py, Ux, Uy)
    Floor.Show(screen)
    Player.Show(screen, Vx, Vy, pressedKeys[pygame.K_DOWN])
    screen.blit(update_fps(), (10, 0))
    clock.tick(60)
    pygame.display.update()
