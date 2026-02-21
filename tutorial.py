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

#Images for sprites are only towards right, so we need to flip them to left aswell
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

#Loading all the images
def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface)) #Making the sprites larger, you can adjust the size: sprites.append(pygame.transform.scale(surface, (48, 48))), just update player at bottom

        #Defining the direction of sprites, all sprites are to the right, the once on left r flipped
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def get_heart_images():
    size = (40, 40)
    
    def make_heart(fill_color, half=False):
        surf = pygame.Surface(size, pygame.SRCALPHA)
        # Draw a simple heart using circles and a polygon
        color = fill_color
        pygame.draw.circle(surf, color, (12, 14), 10)
        pygame.draw.circle(surf, color, (28, 14), 10)
        pygame.draw.polygon(surf, color, [(2, 18), (20, 38), (38, 18)])
        if half:  # Cover right half with transparent
            pygame.draw.rect(surf, (0,0,0,0), (20, 0, 20, 40))
        return surf

    full = make_heart((220, 20, 60))
    half_h = make_heart((220, 20, 60), half=True)
    empty = make_heart((100, 100, 100))
    return full, half_h, empty

#Loading the Terrain Block from assets, can change the image on path
def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size) #Adjust this if u change image
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface) #You can adjust the size here: return pygame.transform.scale(surface, (size * 2, size * 2))

class HeightTracker:
    def __init__(self):
        self.current_height = 0
        self.all_time_best = 0  # never resets
        self.font = pygame.font.SysFont("Arial", 12, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 12, bold=True)

    def update(self, player_y, block_size):
        floor_y = HEIGHT - block_size
        self.current_height = max(0, (floor_y - player_y) // block_size)
        if self.current_height > self.all_time_best:
            self.all_time_best = self.current_height

    def reset_session(self):
        self.current_height = 0

    def draw(self, window):
        padding = 10
        
        all_time_text = self.font.render(f"Best height: {self.all_time_best} blocks", True, (255, 255, 255))
        current_text = self.small_font.render(f"Current height: {self.current_height} blocks", True, (255, 255, 255))

        x = WIDTH - max(all_time_text.get_width(), current_text.get_width()) - padding * 2

        #Position of the text
        window.blit(all_time_text, (x, 15))
        window.blit(current_text, (x, 35))

#Player/Sprite
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1 #If you want bigger gravity just increase number
    SPRITES = load_sprite_sheets("MainCharacters", "PinkMan", 32, 32, True) #Change char here
    ANIMATION_DELAY = 3 #Can change how fast/slow animation is

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
    
    #Jumping
    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0 #On the first jump the gravity goes back to 0
    
    #Directions and actions
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def make_hit(self):
        self.hit = True
        self.hit_count = 0
    
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
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0 #If we fall on a block stop moving
        self.jump_count = 0
    
    def hit_head(self):
        self.count = 0
        self.y_vel = abs(self.y_vel) * 0.5
    
    def update_sprite(self):
        sprite_sheet = "idle" #The default animation is idle
        if self.hit:
            sprite_sheet = "hit"
        if self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        if self.x_vel != 0:
            sprite_sheet = "run" #So obv if we are moving the animation is run
        
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
    
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x, offset_y,):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))

class Health:
    MAX_HEALTH = 10  #10 hits total (5 hearts x 2 halves)

    def __init__(self):
        self.health = self.MAX_HEALTH
        self.heart_full, self.heart_half, self.heart_empty = get_heart_images()

    def take_damage(self):
        self.health = max(0, self.health - 1)

    def is_dead(self):
        return self.health <= 0

    def draw(self, window):
        total_hearts = 5
        heart_width = 40
        spacing = 10
        total_width = total_hearts * heart_width + (total_hearts - 1) * spacing
        start_x = (WIDTH - total_width) // 2
        y = 20

        for i in range(total_hearts):
            heart_health = self.health - i * 2  #Each heart = 2 hit points
            if heart_health >= 2:
                img = self.heart_full
            elif heart_health == 1:
                img = self.heart_half
            else:
                img = self.heart_empty
            window.blit(img, (start_x + i * (heart_width + spacing), y))

#Objects
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

#Adding Fire object
class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"
    
    def off(self):
        self.animation_name = "off"
    
    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

#Background
def draw_background(window, offset_y, block_size):
    # Convert offset_y to height in blocks (offset_y is negative when climbing)
    height_blocks = -offset_y // block_size

    # Define zones as (min_height, max_height, top_color, bottom_color)
    zones = [
        (0,   20,  (135, 206, 135), (135, 206, 235)),  # ground: green to sky blue
        (20,  40,  (100, 160, 220), (135, 206, 235)),  # city: deeper blue
        (40,  60,  (80,  140, 210), (100, 160, 220)),  # clouds: lighter blue
        (60,  80,  (60,  100, 180), (80,  140, 210)),  # planes: medium blue
        (80,  100, (30,  60,  130), (60,  100, 180)),  # high sky: dark blue
        (100, 120, (10,  20,  60),  (30,  60,  130)),  # twilight: very dark
        (120, 150, (5,   5,   20),  (10,  20,  60)),   # space: near black
    ]

    # Find current zone and blend colors
    top_color = (5, 5, 20)
    bottom_color = (5, 5, 20)
    for (min_h, max_h, tc, bc) in zones:
        if min_h <= height_blocks < max_h:
            # How far through this zone are we (0.0 to 1.0)
            progress = (height_blocks - min_h) / (max_h - min_h)
            # Blend toward next zone colors
            top_color = tc
            bottom_color = bc
            break

    # Draw gradient
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)
        pygame.draw.line(window, (r, g, b), (0, y), (WIDTH, y))

# Make a Forest to lvl 0-25
#def draw_forest(window, offset_x, offset_y, height_blocks):

def draw(window, player, objects, offset_x, offset_y, health, height_tracker, stars):
    height_blocks = -offset_y // 96
    draw_background(window, offset_y, 96)
    draw_stars(window, stars, offset_y, height_blocks)
    for obj in objects:
        obj.draw(window, offset_x, offset_y)
    player.draw(window, offset_x, offset_y)
    health.draw(window)
    height_tracker.draw(window)
    pygame.display.update()

#Handling vertical collision
def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj): #Determine if two obj r colliding
            if dy > 0:
                player.rect.bottom = obj.rect.top #If your char collides w obj top
                player.landed()
            elif dy < 0:
                # Only snap to bottom if player is actually below the block
                # not just grazing the side of it
                if player.rect.centerx > obj.rect.left and player.rect.centerx < obj.rect.right:
                    player.rect.top = obj.rect.bottom + 1
                    player.hit_head()
                else:
                    continue  # ignore, it's a side graze not a real head hit!

            collided_objects.append(obj)
    
    return collided_objects

#Horizontal collision
def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
    #After collision it will revert back to where char was
    player.move(-dx, 0)
    player.update()
    return collided_object

#Handling movement and keys
def handle_move(player, objects, health):
    keys = pygame.key.get_pressed()

    player.x_vel = 0 #You need this so the char wont keep moving untill u press key again
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL* 2)

    if keys[pygame.K_a] and not collide_left: #Moving to the left with A key, only if not colliding
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and not collide_right: #Moving to the right with D key, only if not colliding
        player.move_right(PLAYER_VEL)
    
    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            if not player.hit:  # Only take damage if not in hit cooldown
                player.make_hit()
                health.take_damage()

#Generate automated random platforms
def generate_next_platform(block_size, current_height, screen_width_blocks, last_pos):
    positions = ["left", "middle", "right", "middle"]
    section_index = (current_height - 3) // 2  # convert height to section number
    pos = positions[section_index % len(positions)]
    new_blocks = []

    if pos == "left":
        starts = [-1, 0, 1]
        length = random.randint(2, 4)
        start = random.choice(starts)
        for j in range(length):
            new_blocks.append(Block(block_size * (start + j), HEIGHT - block_size * current_height, block_size))

    elif pos == "middle":
        center = screen_width_blocks // 2
        length = random.randint(1, 3)
        start = center - 1
        for j in range(length):
            new_blocks.append(Block(block_size * (start + j), HEIGHT - block_size * current_height, block_size))

    elif pos == "right":
        starts = [screen_width_blocks - 4, screen_width_blocks - 3]
        length = random.randint(2, 4)
        start = random.choice(starts)
        for j in range(length):
            new_blocks.append(Block(block_size * (start + j), HEIGHT - block_size * current_height, block_size))

    # Fire check
    if len(new_blocks) >= 2 and random.random() < 0.4:
        middle_block = new_blocks[len(new_blocks) // 2]
        
        # Check no block exists directly above the fire position
        fire_x = middle_block.rect.x
        fire_y = HEIGHT - block_size * current_height - block_size  # one block above
        block_above = any(
            isinstance(p, Block) and p.rect.x == fire_x and p.rect.y == fire_y
            for p in new_blocks
        )
        
        if not block_above:
            fire = Fire(fire_x, HEIGHT - block_size * current_height - 64, 16, 32)
            fire.on()
            new_blocks.append(fire)

    return new_blocks

#Stars
def draw_stars(window, stars, offset_y, height_blocks):
    if height_blocks < 80:
        return

    opacity = min(1.0, (height_blocks - 80) / 40)
    tick = pygame.time.get_ticks()

    for (x, base_y, size, twinkle) in stars:
        screen_y = base_y - (offset_y * 0.2) # 0.0 doesnt move, 0.05 barely moves and 0.1 moves faster
        screen_y = screen_y % HEIGHT # wrap around screen so stars always visible

        brightness = int(180 + 120 * math.sin(tick / 200 + twinkle * 10))
        #                       ^^^faster range        ^^^faster speed
        brightness = int(brightness * opacity)
        brightness = max(0, min(255, brightness))

        r = min(255, brightness + 20) # always push red high
        g = min(255, brightness + 55) # always push green high  
        b = int(brightness * 0.3) # blue low = yellow tint

        pygame.draw.circle(window, (r, g, b), (x, int(screen_y)), size)

def main(window, height_tracker=None):
    clock = pygame.time.Clock()
    block_size = 96

    if height_tracker is None:
        height_tracker = HeightTracker()
    else:
        height_tracker.reset_session() # only reset session, keep all time best

    player = Player(WIDTH // 2 - 25, HEIGHT - block_size - 64, 50, 50) # Starting position
    health = Health()

    # Generate stars spread across the climbing range
    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT),
          random.randint(1, 2), random.random()) for _ in range(200)]
    
    preset_platforms = [
        Block(block_size * 3, HEIGHT - block_size * 3, block_size),
        Block(block_size * 7, HEIGHT - block_size * 3, block_size),
        Block(block_size * 5, HEIGHT - block_size * 5, block_size),
        Block(block_size * 6, HEIGHT - block_size * 5, block_size),
        Block(block_size * 4, HEIGHT - block_size * 5, block_size),
        Block(block_size * 3, HEIGHT - block_size * 5, block_size),
        Block(block_size * 7, HEIGHT - block_size * 5, block_size),
        Block(block_size * 9, HEIGHT - block_size * 7, block_size),
        Block(block_size * 10, HEIGHT - block_size * 7, block_size),
        Block(block_size * 11, HEIGHT - block_size * 7, block_size),
        Block(block_size * 12, HEIGHT - block_size * 7, block_size),
        Block(block_size * 1, HEIGHT - block_size * 7, block_size),
        Block(block_size * 0, HEIGHT - block_size * 7, block_size),
        Block(block_size * -1, HEIGHT - block_size * 7, block_size),
        Block(block_size * -2, HEIGHT - block_size * 7, block_size),
        Block(block_size * 5, HEIGHT - block_size * 9, block_size),
        Block(block_size * 1, HEIGHT - block_size * 11, block_size),
        Block(block_size * 0, HEIGHT - block_size * 11, block_size),
        Block(block_size * -1, HEIGHT - block_size * 11, block_size),
        Block(block_size * 9, HEIGHT - block_size * 11, block_size),
        Block(block_size * 10, HEIGHT - block_size * 11, block_size),
        Block(block_size * 11, HEIGHT - block_size * 11, block_size),
        Block(block_size * 5, HEIGHT - block_size * 14, block_size),
        Block(block_size * 4, HEIGHT - block_size * 14, block_size),
        Block(block_size * 6, HEIGHT - block_size * 14, block_size),
        Block(block_size * 3, HEIGHT - block_size * 13, block_size),
        Block(block_size * 7, HEIGHT - block_size * 13, block_size),
        Block(block_size * -2, HEIGHT - block_size * 3, block_size),
        Block(block_size * -3, HEIGHT - block_size * 3, block_size),
        Block(block_size * -4, HEIGHT - block_size * 4, block_size),
        Block(block_size * -5, HEIGHT - block_size * 4, block_size),
        Block(block_size * 12, HEIGHT - block_size * 3, block_size),
        Block(block_size * 13, HEIGHT - block_size * 3, block_size),
        Block(block_size * 14, HEIGHT - block_size * 4, block_size),
        Block(block_size * 15, HEIGHT - block_size * 4, block_size),
    ]

    floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)]
    platforms = []
    generated_height = 16 # start generating above my designed blocks
    objects = [*floor, *preset_platforms]

    offset_x = 0
    offset_y = 0
    scroll_area_width = 200
    scroll_area_height = 200

    run = True
    while run:
        clock.tick(FPS) #Requlating the FPS across diff devices

        #Setting the quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            #Initializing jump, double jump
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        # Generate more platforms as player climbs
        player_height_blocks = (HEIGHT - player.rect.y) // block_size
        if player_height_blocks + 10 > generated_height:  # stay 10 blocks ahead
            new_platform = generate_next_platform(block_size, generated_height, WIDTH // block_size, None)
            platforms.extend(new_platform)
            objects.extend(new_platform)
            generated_height += 2        

        player.loop(FPS)
        handle_move(player, objects, health)
        height_tracker.update(player.rect.y, block_size)
        draw(window, player, objects, offset_x, offset_y, health, height_tracker, stars)

        #Defining background movement horizontal
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

        for obj in objects:
            if hasattr(obj, 'loop'):
                obj.loop()
        
        if health.is_dead():
            main(window, height_tracker)
            return
        
        # Vertical scrolling
        if ((player.rect.bottom - offset_y >= HEIGHT - scroll_area_height) and player.y_vel > 0) or (
            (player.rect.top - offset_y <= scroll_area_height) and player.y_vel < 0):
            offset_y += player.y_vel

        #Verical wont go below the floor
        offset_y = min(offset_y, 0)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)