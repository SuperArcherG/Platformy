import pygame


class BG:

    def __init__(self, screenwidth, screenheight, imagefile):

        self.screenwidth = screenwidth
        self.screenheight = screenheight

        self.img = pygame.image.load(imagefile)
        self.img = pygame.transform.scale(
            self.img, (self.screenwidth, self.screenheight))
        self.coord = [0, 0]
        self.coord2 = [-screenwidth, 0]
        self.coord3 = [0, -screenheight]
        self.coord4 = [-screenwidth, -screenheight]

    def Show(self, surface):

        surface.blit(self.img, self.coord)
        surface.blit(self.img, self.coord2)
        surface.blit(self.img, self.coord3)
        surface.blit(self.img, self.coord4)

    def UpdateCoords(self, parralax, PlayerX, PlayerY):

        NewX = parralax * PlayerX
        NewY = parralax * PlayerY

        self.coord[0] = NewX % self.screenwidth
        self.coord2[0] = (NewX % self.screenwidth) - self.screenwidth
        self.coord3[0] = NewX % self.screenwidth
        self.coord4[0] = (NewX % self.screenwidth) - self.screenwidth
        self.coord[1] = NewY % self.screenheight
        self.coord2[1] = (NewY % self.screenheight)
        self.coord3[1] = NewY % self.screenheight - self.screenheight
        self.coord4[1] = (NewY % self.screenheight) - self.screenheight
