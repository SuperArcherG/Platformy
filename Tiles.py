import pygame
import json


class Tiles:
    def __init__(self, data, pathToImages, screenwidth, screenheight, Uo):
        self.dat = data.read()
        self.data = json.loads(self.dat)
        self.screenwidth = screenwidth
        self.screenheight = screenheight

        self.Stone = pygame.transform.scale(pygame.image.load(
            pathToImages + "Stone.png"), ((self.screenwidth/16, self.screenheight/16)))

        self.middle = (screenwidth/2-Uo[0], screenheight/2-Uo[1])
        self.sprites = [self.Stone]

    def Show(self, surface, Px, Py, Ux, Uy, Uo):
        self.middleOffset = (self.middle[0] - self.Stone.get_size()
                             [0]/2, self.middle[1] - self.Stone.get_size()[1]/2)
        X = -Px * Ux + self.middleOffset[0]
        Y = Py * Uy + self.middleOffset[1]
        for tile in self.data['Tiles']:
            # print(tile)
            lx, ly = tile['x']*Ux, -tile['y']*Uy
            # print(tile['type'])
            surface.blit(self.sprites[tile['type']], (X+lx, Y+ly))
       # surface.blit()

    def UpdateData(self, data):
        self.dat = data.read()
        self.data = json.loads(self.dat)
