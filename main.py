import pygame
import sys
import input_box
import console
import random
import os

pygame.init()

screen=pygame.display.set_mode((640, 680))
pygame.display.set_caption(f"Gui Shell Emulator")
console_layer = pygame.Surface((640, 680))

bg_col=(50, 50, 100)
gray=(200, 200, 200)

def kill():
    pygame.quit()
    sys.exit()

def main():
    clock = pygame.time.Clock()
    console_output = console.ConsoleOutput(25, 18, 90, 600, 575)
    inputbox = input_box.InputBox(10, 50, 615, 30, 25)

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

            inputbox.handle_event(event)

        screen.fill(bg_col)
        inputbox.draw(screen)
        console_output.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    kill()

if __name__ == '__main__':
    main()