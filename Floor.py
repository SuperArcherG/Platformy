import pygame


class Floor:

    def __init__(self, screenwidth, screenheight, Top, Bottom):

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
        self.middle = (screenwidth/2, screenheight/2)

    def Show(self, surface):
        surface.blit(self.top, self.coord1)
        surface.blit(self.top, self.coord2)
        surface.blit(self.top, self.coord3)
        surface.blit(self.top, self.coord4)
        surface.blit(self.top, self.coord5)
        surface.blit(self.bottom, self.coord11)
        surface.blit(self.bottom, self.coord21)
        surface.blit(self.bottom, self.coord31)
        surface.blit(self.bottom, self.coord41)
        surface.blit(self.bottom, self.coord51)

    def UpdateCoords(self, PlayerX, PlayerY, Ux, Uy):
        X = (-PlayerX % 4) * Ux
        Y = PlayerY * Uy + self.middle[1]
        offset = self.top.get_width()
        self.coord1 = (X, Y)
        self.coord2 = (X + offset, Y)
        self.coord3 = (X + 2 * offset, Y)
        self.coord4 = (X + 3 * offset, Y)
        self.coord5 = (X - offset, Y)
        self.coord11 = (X, Y + offset)
        self.coord21 = (X + offset, Y + offset)
        self.coord31 = (X + 2 * offset, Y + offset)
        self.coord41 = (X + 3 * offset, Y + offset)
        self.coord51 = (X - offset, Y + offset)
