import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 120
screen_size = (screen_x, screen_y) = (1200, 900)
screen = pygame.display.set_mode(screen_size)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

balls = []

class BALL(object):
    
    def __init__(self, size, x, y, vx, vy, color):
        self.size = size
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def screen(self):
        circle(screen, self.color, (self.x, self.y), self.size)

def new_ball():
    temp_ball = BALL(randint(10, 100),
                     randint(100, 1100),
                     randint(100, 800),
                     randint(-5, 5),
                     randint(-5, 5),
                     COLORS[randint(0, 5)])
    good_place = False
    while not good_place:
        good_place = True
        for ball in balls:
            distance = int(((temp_ball.x - ball.x)**2 + (temp_ball.y - ball.y)**2)**0.5 - ball.size)
            temp_ball.size = min(distance, temp_ball.size)
            if temp_ball.size <= 10:
                temp_ball.x = randint(100, 1100)
                temp_ball.y = randint(100, 800)
                good_place = False
                break
    balls.append(BALL(temp_ball.size, temp_ball.x, temp_ball.y, temp_ball.vx, temp_ball.vy, temp_ball.color))


pygame.display.update()
clock = pygame.time.Clock()
score = 0
finished = False

new_ball()
new_ball()
new_ball()
new_ball()
new_ball()
new_ball()
new_ball()
new_ball()
new_ball()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            event.x, event.y = event.pos
            for ball in balls:
                if (ball.x - event.x)**2 + (ball.y - event.y)**2 < ball.size**2:
                    score += 1
                    balls.remove(ball)
                    new_ball()
    for ball in balls:
        ball.move()
        ball.screen()
        if min(ball.x, abs(ball.x - screen_x)) <= ball.size:
            ball.vx = -ball.vx
            ball.x += 2 * ball.vx 
        if min(ball.y, abs(ball.y - screen_y)) <= ball.size:
            ball.vy = -ball.vy
            ball.y += 2 * ball.vy
        for other_ball in balls:
            if ball != other_ball:
                if (ball.x - other_ball.x)**2 + (ball.y - other_ball.y)**2 <= (ball.size + other_ball.size)**2:
                    temp_vx = ball.vx
                    temp_vy = ball.vy
                    ball.vx = other_ball.vx
                    ball.vy = other_ball.vy
                    other_ball.vx = temp_vx
                    other_ball.vy = temp_vy
                    ball.move()
                    other_ball.move()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
