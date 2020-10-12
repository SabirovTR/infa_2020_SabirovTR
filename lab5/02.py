import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 10
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def new_ball():
    '''рисует новый шарик '''
    global x, y, vx, vy, r
    x = randint(100, 1100)
    y = randint(100, 900)
    vx = randint(10, 100)
    vy = randint(10, 100)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)

pygame.display.update()
clock = pygame.time.Clock()
finished = False
flag = False
hit_flag = True
endure_counter = 2
miss_counter = 0
score = 0

while not finished:
    if (hit_flag)or(miss_counter > endure_counter):
        new_ball()
        pygame.display.update()
        screen.fill(BLACK)
        hit_flag = False
        miss_counter = 0
    else:
        miss_counter += 0.1
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x0, y0 = event.pos
                if (x - x0)**2 + (y - y0)**2 < r**2:
                    score += 1
                    miss_counter = 0
                    hit_flag = True

pygame.quit()

print(score)
