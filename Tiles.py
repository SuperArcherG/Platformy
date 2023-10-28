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
        self.Sand = pygame.transform.scale(pygame.image.load(
            PathToImages + "Sand.png"), ((self.screenwidth/16, self.screenheight/16)))
            
        self.middle = (screenwidth/2-Uo[0], screenheight/2-Uo[1])
        self.sprites = [self.Stone] #, self.Sand

    def Show(self, surface, Px, Py, Ux, Uy, Uo):
        self.middleOffset = (self.middle[0] - self.Stone.get_size()
                             [0]/2, self.middle[1] - self.Stone.get_size()[1]/2)
        X = -Px * Ux + self.middleOffset[0]
        Y = Py * Uy + self.middleOffset[1]
        for tile in self.data['Tiles']:
            lx, ly = self.data['Tiles'][tile]['x']*Ux, -self.data['Tiles'][tile]['y']*Uy
            surface.blit(
                self.sprites[self.data['Tiles'][tile]['type']], (X+lx, Y+ly))
        # surface.blit()

    def UpdateData(self, data):
        self.dat = data.read()
        self.data = json.loads(self.dat)
        
    def Corrected(self, Px, Py, PrevX, PrevY, DebugEnabled):
        Grounded = False
        wipx = Px
        wipy = Py
        for tile in self.data['Tiles']:
            x = self.data['Tiles'][tile]['x']
            y = self.data['Tiles'][tile]['y']
            # print(str(x) + ", " + str(y))
            a = x - 0.5 < wipx + 0.5
            b = x + 0.5 > wipx - 0.5
            c = y - 0.5 < wipy + 0.5
            d = y + 0.5 > wipy - 0.5

            a2 = x - 0.5 < PrevX + 0.5
            b2 = x + 0.5 > PrevX - 0.5
            c2 = y - 0.5 < PrevY + 0.5
            d2 = y + 0.5 > PrevY - 0.5

            if a & b & c & d:
                if a & b:
                    if a and not a2:
                        wipx = x-1
                        #if DebugEnabled:
                         #   print("PR hit TL")
                    else:
                        if b and not b2:
                            wipx = x+1
                           # if DebugEnabled:
                             #   print("PL hit TR")
                if c & d:
                    if c and not c2:
                        wipy = y-1
                        #if DebugEnabled:
                         #   print("PT hit TB")
                    else:
                        if d and not d2:
                            wipy = y+1
                            Grounded = True
                            #if DebugEnabled:
                             #   print("PB hit TT")
            
            if DebugEnabled:
                print(str(a), str(b), str(c), str(d), str(a2), str(b2), str(c2), str(d2))
        if DebugEnabled:
            print(str(wipx) + ", " + str(wipy))
        mixed = [wipx,wipy,Grounded]
        
        return(mixed)
            
