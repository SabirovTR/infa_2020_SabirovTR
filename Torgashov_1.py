import pygame
from pygame.draw import *
from random import randint

screen_size = (length, height)  = (500, 700)


original_color_hedge = (70, 52, 52)
original_color_trees = (213, 172, 0)
original_color_spikes = (31, 21, 21)
original_color_background = (40, 161, 90)
original_color_frontground = (108, 93, 82)
test_color = (100, 100, 100)


pygame.init()

FPS = 30
screen = pygame.display.set_mode(screen_size)


rect(screen, original_color_background, (0, 0, length, height)) 
rect(screen, original_color_frontground, (0, 500, length, height))


def tree(surface, tree_color, x, y, width):

    '''
      Функция рисует ствол дерева, уходящий вверх до конца картинки("До неба")
    surface - объект pygame.Surface
    tree_color - цвет, заданный в формате, подходящем для pygame.Color
    x, y - координаты левого нижнего угла изображения
    width - ширина свола дерева
    '''
    
    rect(surface, tree_color, (x, y, width, - height))


def mushroom(surface, head_color, stipe_color, x, y, mushroom_size, points=True):

    '''
      Функция рисует гриб
    surface - объект pygame.Surface
    head_color - цвет шляпки гриба, заданный в формате, подходящем для pygame.Color
    stipe_color - цвет ножки гриба, заданный в формате, подходящем для pygame.Color
    x, y - координаты центра гриба
    mushroom_size - размер гриба
    points(bool) - точки на шляпке гриба(ставятся случайным образом на шляпке гриба)
      По умолчанию точки есть(points=True)
    '''
    
    k = mushroom_size
    ellipse(surface, stipe_color, (x + 7.5*k , y + 5*k, 5*k, 15*k))    
    ellipse(surface, head_color, (x, y, 20*k, 10*k))

    if points == True:
        for _ in range(10):
            ellipse(surface, (255, 255, 255), (x + randint(2, 16)*k, 
                                              y + randint(1, 7)*k, 2*k, k))            

def hedge(surface, body_color, spikes_color, x, y, hedge_size, mashroom_head_color=(255, 0, 0), mashroom_stipe_color=(255, 255, 255), mashroom_points=True):

    '''
      Функция рисует ежика с грибами
    surface - объект pygame.Surface
    body_color - цвет ежика, заданный в формате, подходящем для pygame.Color
    spikes_color - цвет колючек, заданный в формате, подходящем для pygame.Color
    mashroom_head_color - цвет шляпки грибов
      По умолчанию цвет шляпки - красный()
    mashroom_stipe_color - цвет ножки грибов
      По умолчанию цвет ножки - белый()
    x, y - координаты центра ежика
    hendge_size - размер гриба
    mashroom_points(bool) - точки на шляпке гриба(ставятся случайным образом на шляпке гриба)
      По умолчанию точки есть(mashroom_points=True)
    '''

    k = hedge_size

    ellipse(surface, body_color, (x+k*16, y+k*7, k*6, k*3))
    ellipse(surface, body_color, (x, y+k*7, k*6, k*3))
    ellipse(surface, body_color, (x+k*17, y+k*3, k*6, k*3))
    
    ellipse(surface, body_color, (x, y, k*20, k*10))
    ellipse(surface, body_color, (x+k*17, y+k*3, k*7, k*4))
    
    circle(surface, (0, 0, 0), (x+k*20, y+k*4), k//2)
    circle(surface, (0, 0, 0), (x+k*22, y+k*4), k//2)
    
    
    for i in range(50):
        x1, y1 = x + randint(2, 16)*k, y + randint(1, 7)*k
        polygon(surface, (0, 0, 0), [[x1, y1], [x1+2*k, y1], [x1+k, y1-4*k]], 0)
        if i == 40:
            mushroom(surface, mashroom_head_color, mashroom_stipe_color, x-k, y-k, k/3, mashroom_points)
            mushroom(surface, mashroom_head_color, mashroom_stipe_color, x+2*k, y+2*k, k/3, mashroom_points)
            mushroom(surface, mashroom_head_color, mashroom_stipe_color, x+8*k, y+3*k, k/3, mashroom_points)
            
            circle(surface, (255, 112, 77), (x+10*k, y+k), 2*k)
            circle(surface, (255, 112, 77), (x+14*k, y+k*3), 2*k)
           

#Зададим координаты ежиков, грибов и деревьев
trees = [(0, 520, 30), (100, 650, 80), (320, 580, 40), (430, 550, 30)]
hedges = [(300, 550, 7), (400, 400, 4), (100, 500, 3), (-50, 650, 5)]
mushrooms = [(450, 650, 4), (410, 660, 4), (370, 640, 4), (320, 655, 4)]

#Нарисуем картинку по заранее заданным величинам
for tr in trees:
    tree(screen, original_color_trees, *tr)

for hg in hedges:
    hedge(screen, (111, 111, 111), original_color_spikes, *hg)
    
for mush in mushrooms:
    mushroom(screen, (255, 0, 0), (255, 255, 255), *mush)
    

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
