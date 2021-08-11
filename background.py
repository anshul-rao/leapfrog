import pygame
import colorsys


class Background:
    def __init__(self):
        self.sprite = pygame.image.load('img/bg.png')
        self.pos = 0
        self.uncoloredSprite = pygame.image.load('img/bg.png')

    def setSprite(self, tint):
        spriteCopy = self.uncoloredSprite.copy()
        color = colorsys.hsv_to_rgb(tint, 1, 1)
        spriteCopy.fill((color[0] * 255, color[1] * 255, color[2] * 255), special_flags=pygame.BLEND_ADD)
        self.sprite = spriteCopy
