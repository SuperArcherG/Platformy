import pygame


class Floor:

    def __init__(self, screenwidth, screenheight, Top, Bottom, Uo):

        self.screenwidth = screenwidth
        self.screenheight = screenheight

        self.top = pygame.image.load(Top)
        self.top = pygame.transform.scale(
            self.top, (self.screenwidth/4, self.screenheight/4))
        self.bottom = pygame.image.load(Bottom)
        self.bottom = pygame.transform.scale(
            self.bottom, (self.screenwidth/4, self.screenheight/4))
        self.coord1 = [0, 0]
        self.coord2 = [0, 0]
        self.coord3 = [0, 0]
        self.coord4 = [0, 0]
        self.coord5 = [0, 0]
        self.middle = (screenwidth/2-Uo[0], screenheight/2-Uo[1])
        self.offset = self.screenwidth/4

    def Show(self, surface, PlayerX, PlayerY, Ux, Uy):
        self.middleOffset = (
            self.middle[0] - self.screenheight/16, self.middle[1] - self.screenwidth/16)
        X = (-PlayerX % 4) * Ux - Ux/2
        Y = PlayerY * Uy + self.middleOffset[1]+Uy*1.5
        offsets = [-1, 0, 1, 2, 3, 4]
        heights = [0, -1]
        sprites = [self.top, self.bottom, self.bottom]
        for y in heights:
            for x in offsets:
                surface.blit(sprites[y], (X+self.offset *
                             offsets[x], Y-self.offset*heights[y]))
