#!/usr/bin/python3

import pygame
import sys

clock = pygame.time.Clock()
MAX_FPS = 60
MAP_SIZE = 30
TILE_SIZE = 40

class Map:
    """ map class """
    
    def __init__(self):
        self.map = [[0 for i in range(MAP_SIZE)] for j in range(MAP_SIZE)]
        print("Initializing map")

    def draw(self, background):
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                pygame.draw.rect(background, (0, i*8, 0),
                    (i*TILE_SIZE, j*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                print(self.map[i][j], end="")
            print("")



class Display:

    def __init__(self, background):
        print("Initializing display")
        resolution = (800, 600)    
        screen = pygame.display.set_mode(resolution)
        background = pygame.Surface(screen.get_size())
        background.fill((255, 255, 255))
        background = background.convert()
        pygame.draw.circle(background, (0,0,255), (25,25),25) 
        screen.blit(background, (0, 0))


def getKeys(event, isdown):
    if isdown:
        print("Key pressed")
    else:
        print("Key released")


def handleInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            getKeys(event, True)
        elif event.type == pygame.KEYUP:
            getKeys(event, False)


def init(map, background):
    print("Initializing game")
    pygame.init()
    display = Display(background)
    map.draw(background)


def update(delta):
    global clock
    text = "FPS: {0:.2f}".format(clock.get_fps())
    pygame.display.set_caption(text)


def redraw(map, background):
    map.draw(background)
    pygame.display.flip()


def loop(map, background):
    global clock
    global MAX_FPS
    
    print("Starting simulation")
    
    while True:
        delta = clock.tick(MAX_FPS)
        handleInput()
        update(delta)
        redraw(map, background)


def main():
    map = Map()
    background = None
    init(map, background)
    loop(map, background)


if __name__ == "__main__" :
    main()