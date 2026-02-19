import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Platformer") #Sets the name of the game on top of screen

WIDTH, HEIGHT = 1000, 800 #Adjust this if youre on a smaller screen
FPS = 60
PLAYER_VEL = 5 #Speed in which char moves around the screen

window = pygame.display.set_mode((WIDTH,HEIGHT)) #Creating game window

#Player
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
    
    #Direction
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0


    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

#Background
def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect() #The two _ will pull the information from the image
    tiles = []

    #Setting x and y axis with the tiles
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
    return tiles, image

def draw(window, background, bg_image):
    for tile in background:
        window.blit(bg_image, tile)

    pygame.display.update()

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png") #Can change the bg

    run = True
    while run:
        clock.tick(FPS) #Requlating the FPS across diff devices

        #Setting the quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        draw(window, background, bg_image)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)