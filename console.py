import pygame
import sys

text_list=[]

class ConsoleOutput:
    def __init__(self, font_size, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.Font(None, font_size)
        self.line_height = self.font.get_height()

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        if len(text_list)>28:
            text_list.pop(0)

        for i in range(len(text_list)):
            img = self.font.render(text_list[i], True, (255, 255, 255))
            screen.blit(img, (30, 100+20*i))