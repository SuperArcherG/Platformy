import pygame


class Player():
    def __init__(self, L, R, U, D, N, screenwidth, screenheight, Uo):
        self.L = pygame.image.load(L)
        self.R = pygame.image.load(R)
        self.U = pygame.image.load(U)
        self.D = pygame.image.load(D)
        self.N = pygame.image.load(N)
        self.screenwidth = screenwidth
        self.screenheight = screenheight
        self.middle = (screenwidth/2-Uo[0], screenheight/2-Uo[1])

    def Show(self, surface, Vx, Vy, pressedDown):
        directionSprite = self.N
        if (Vx > 0 and abs(Vx) >= -Vy):
            directionSprite = self.R
        else:
            if (Vx < 0 and abs(Vx) >= -Vy):
                directionSprite = self.L
            else:
                if (Vy > 0):
                    directionSprite = self.U
                else:
                    if (Vy < 0):
                        directionSprite = self.D
                    else:
                        if (pressedDown):
                            directionSprite = self.D
                        else:
                            directionSprite = self.N

        sprite = pygame.transform.scale(
            directionSprite, (self.screenwidth/16, self.screenheight/16))
        middleOffset = (self.middle[0] - sprite.get_size()
                        [0]/2, self.middle[1] - sprite.get_size()[1]/2)
        surface.blit(sprite, middleOffset)
