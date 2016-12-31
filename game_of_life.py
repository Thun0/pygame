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

    def draw(self, display):
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                pygame.draw.rect(display.background, (0, i*8, 0),
                    (i*TILE_SIZE, j*TILE_SIZE, TILE_SIZE, TILE_SIZE))



class Display:

    def __init__(self):
        print("Initializing display")
        self.resolution = (800, 600)
        self.screen = pygame.display.set_mode(self.resolution)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255, 255, 255))
        self.background = self.background.convert()

    def blit(self):
        self.screen.blit(self.background, (0, 0))


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


def init():
    print("Initializing game")
    pygame.init()
    display = Display()
    map = Map()
    return map, display;


def update(delta):
    global clock
    text = "FPS: {0:.2f}".format(clock.get_fps())
    pygame.display.set_caption(text)


def redraw(map, display):
    map.draw(display)
    display.blit();
    pygame.display.flip()


def loop(map, display):
    global clock
    global MAX_FPS
    
    print("Starting simulation")
    
    while True:
        delta = clock.tick(MAX_FPS)
        handleInput()
        update(delta)
        redraw(map, display)


def main():
    map, display = init()
    loop(map, display)


if __name__ == "__main__" :
    main()