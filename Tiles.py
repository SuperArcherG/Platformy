import pygame
import json
# from Debug import Debug


class Tiles:
    def __init__(self, data, PathToImages, screenwidth, screenheight, Uo):
        self.dat = data.read()
        self.data = json.loads(self.dat)
        self.screenwidth = screenwidth
        self.screenheight = screenheight

        self.Stone = pygame.transform.scale(pygame.image.load(
            PathToImages + "Stone.png"), ((self.screenwidth/16, self.screenheight/16)))

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
            surface.blit(self.sprites[tile['type']], (X+lx, Y+ly))
       # surface.blit()

    def UpdateData(self, data):
        self.dat = data.read()
        self.data = json.loads(self.dat)

    def IsColliding(self, Px, Py, surface, DebugEnabled):
        self.collisionPoints = [
            (-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]
        # if DebugEnabled:
        #     for i in self.collisionPoints:
        #         surface.blit(Debug.Circle, i)
        colliding = False
        for tile in self.data['Tiles']:
            # print(tile)
            lx, ly = tile['x'], tile['y']

            maxx, maxy, minx, miny = 0, 0, 0, 0

            for point in self.collisionPoints:
                maxx = max(point[0], maxx)
                minx = min(point[0], minx)
                maxy = max(point[1], maxy)
                miny = min(point[1], miny)
            c1, c2, c3, c4 = False, False, False, False
            cx1, cx2 = False, False
            for point in self.collisionPoints:
                if (Px > minx+lx-0.5):
                    c1 = True
                    cx1 = True
                if (Px < maxx+lx+0.5):
                    c2 = True
                    cx2 = True
                if (Py > miny+ly):
                    c3 = True
                if (Py < maxy+ly+0.5):
                    c4 = True
                print(str(c1) + ' ' + str(c2) + ' ' + str(c3) +
                      ' ' + str(c4) + ' ' + str(cx1) + ' ' + str(cx2))

            if (c1 and c2 and c3 and c4):
                self.colliding = True
                if cx1 and cx2:
                    self.direct = 1
                    # SnapPos
                else:
                    self.direct = 0
                return self.colliding

    def GetDir(self):
        return self.direct

    def GetPos(self):
        return self.SnapPos
