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
    
    def loop(self, fps):
        self.move(self.x_vel, self.y_vel)
    
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)

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

def draw(window, background, bg_image, player):
    for tile in background:
        window.blit(bg_image, tile)

    player.draw(window)

    pygame.display.update()

#Handling movement and keys
def handle_move(player):
    keys = pygame.key.get_pressed()

    player.x_vel = 0 #You need this so the char wont keep moving untill u press key again
    #Moving to the left with A key
    if keys[pygame.K_a]:
        player.move_left(PLAYER_VEL)
    #Moving to the right with D key
    if keys[pygame.K_d]:
        player.move_right(PLAYER_VEL)

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png") #Can change the bg

    player = Player(100, 100, 50, 50)

    run = True
    while run:
        clock.tick(FPS) #Requlating the FPS across diff devices

        #Setting the quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        player.loop(FPS)
        handle_move(player)
        draw(window, background, bg_image, player)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)