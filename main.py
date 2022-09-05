import math
import sys
import pygame

import os
os.environ["SDL_VIDEODRIVER"]="x11"

from vector import Vector

pygame.init()

# window stuff
screen_size = width, height = 800, 300
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# background image scrolling
bg = pygame.image.load("assets/background.jpg").convert()
tiles = math.ceil(width / bg.get_width()) + 1
scroll = 0

# player stuff
speed = 2
velocity = Vector()
position = Vector()
size = 10, 20
player = pygame.Rect(400, 0, *size)
left = right = up = down = can_jump = False

# for debug text
font = pygame.font.SysFont("consolas", 30)

while 1:  # game loop
    delta = clock.tick(60)
    time_scale = delta / 5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == 97:  # a
                left = True
            elif event.key == 100:  # d
                right = True
            elif event.key == 115:  # s
                down = True
            elif event.key == 119:  # w
                up = True
        elif event.type == pygame.KEYUP:
            if event.key == 97:  # a
                left = False
            elif event.key == 100:  # d
                right = False
            elif event.key == 115:  # s
                down = False
            elif event.key == 119:  # w
                up = False


    # movement
    velocity.x = 0
    if left:
        velocity.x -= speed
    if right:
        velocity.x += speed
    if up and can_jump:
        velocity.y = -9
        can_jump = False
    velocity.y += 0.7  # gravity
    position.x += velocity.x
    position.y += velocity.y
    scroll = -(position.x % bg.get_width())
    player.move_ip(0, velocity.y * time_scale)

    # don't let the player fall forever
    if player.y > 200:
        player.y = position.y = 200
        velocity.y = 0
        can_jump = True

    # draw the background
    screen.fill((200, 200, 200))
    for i in range(tiles):
        screen.blit(bg, (bg.get_width()*i + scroll, 0))
    pygame.draw.rect(screen, (0, 0, 0), player)

    # debug text?
    pos_text = font.render(f"x: {position.x} y: {position.y}", False, (0, 0, 0), None)
    screen.blit(pos_text, (10, 10))

    pygame.display.flip()