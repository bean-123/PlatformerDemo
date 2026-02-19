import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Platformer") #Sets the name of the game on top of screen

BG_COLOR = (255,255,255)
WIDTH, HEIGHT = 1000, 800 #Adjust this if youre on a smaller screen
FPS = 60
PLAYER_VEL = 5 #Speed in which char moves around the screen

window = pygame.display.set_mode((WIDTH,HEIGHT)) #Creating game window

def main(window):
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS) #Requlating the FPS across diff devices

        #Setting the quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)