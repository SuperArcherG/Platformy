import pygame
import sys
import os
from pygame.locals import *
from MovingBackground import BG
from Player import Player
from Floor import Floor

pygame.init()  # initialize pygame
font = pygame.font.SysFont("Arial", 18)

clock = pygame.time.Clock()
screenwidth, screenheight = (800, 800)
screen = pygame.display.set_mode(
    (screenwidth, screenheight), flags=pygame.SCALED, vsync=1)
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

jump = pygame.mixer.Sound(os.path.join("audio/jump.wav"))
land = pygame.mixer.Sound(os.path.join("audio/land.wav"))

# player coordinates
Px, Py = 0, 0
Vx, Vy = 0, 0
Ox, Oy = 0, 0
# Load the background image here. Make sure the file exists!

Mountains = BG(screenwidth, screenheight,
               os.path.join("images/background/BG.png"))
L, R, U, D, N = os.path.join("images/Player/L.png"), os.path.join("images/Player/R.png"), os.path.join(
    "images/Player/U.png"), os.path.join("images/Player/D.png"), os.path.join("images/Player/N.png")
Player = Player(L, R, U, D, N, screenwidth, screenheight)
Floor = Floor(screenwidth, screenheight,
              os.path.join("images/tiles/Ground.png"), os.path.join(
                  "images/tiles/DirtGround.png"))
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
    Player.Show(screen, Vx, Vy)
    screen.blit(update_fps(), (10, 0))
    clock.tick(60)
    pygame.display.update()
