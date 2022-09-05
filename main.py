import math
import sys
import pygame

from vector import Vector


BACKGROUND_IMAGE_PATH = "assets/background.jpg"
pygame.init()

# window stuff
screen_size = width, height = 800, 300
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

# background image scrolling
bg = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
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
        velocity.y = -4
        can_jump = False
    velocity.y += 0.25  # gravity

    # track the player position
    position.x += velocity.x * time_scale
    position.y += velocity.y * time_scale

    # determine the background position
    scroll -= velocity.x * time_scale
    if abs(scroll) > bg.get_width():
        scroll %= bg.get_width()

    # for now player stays in the middle of the screen
    player.move_ip(0, velocity.y * time_scale)
    player.x = 400
    player.y = int(position.y)

    # don't let the player fall forever
    if position.y > 200:
        player.y = position.y = 200
        velocity.y = 0
        can_jump = True

    # draw the background
    screen.fill((200, 200, 200))
    for i in range(-1, tiles):
        screen.blit(bg, (bg.get_width()*i + scroll, -140))
    pygame.draw.rect(screen, (0, 0, 0), player)

    # debug text?
    pos_text = font.render(f"x: {position.x: 8.2f} y: {position.y:.2f}", False, (0, 0, 0), None)
    screen.blit(pos_text, (10, 10))

    pygame.display.flip()