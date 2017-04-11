#!/usr/bin/python3

import sys

import pygame

clock = pygame.time.Clock()

MAX_FPS = 60
MAP_WIDTH = 80
MAP_HEIGHT = 50
TILE_SIZE = 25
FRAME_WIDTH = 2
WIDTH = 300
HEIGHT = 300


class Tile:

    EMPTY = 0
    WALL = 1
    BULB = 2
    CROSS = 3

    lighted = False
    value = 0

    def __init__(self):
        pass

    def __init__(self, val):
        pass


class Map:
    """ map class """

    map = []
    width = 0
    height = 0

    def __init__(self):
        pass

    def __init__(self, filename):
        with open(filename) as f:
            line = f.readline()
            self.width, self.height = [int(x) for x in line.split()]
            print(str(self.width) + " " + str(self.height))
            for i in range(self.width):
                line = f.readline()
                self.map.append([Tile(int(x)) for x in line.split()])

    def draw(self, display):
        for i in range(self.width):
            for j in range(self.height):
                color = 0
                if self.map[i][j] == 0:
                    color = 255
                pygame.draw.rect(display.background, (0, 0, 0),
                                 (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(display.background, (color, color, color),
                                 (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE - FRAME_WIDTH, TILE_SIZE - FRAME_WIDTH))

    def clear(self):
        self.map = [[0 for i in range(MAP_WIDTH)] for j in range(MAP_HEIGHT)]

    def update(self):
        old = [x[:] for x in self.map]
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                neighbours = self.countNeighbours(old, i, j)
                if self.map[i][j] == 1:
                    if neighbours == 2 or neighbours == 3:
                        self.map[i][j] = 1
                    else:
                        self.map[i][j] = 0
                elif neighbours == 3:
                    self.map[i][j] = 1
                else:
                    self.map[i][j] = 0


class Display:
    def __init__(self):
        print("Initializing display")
        self.resolution = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.resolution)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255, 255, 255))
        self.background = self.background.convert()

    def blit(self):
        self.screen.blit(self.background, (0, 0))


def handleInput(map):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def init():
    print("Initializing game")
    pygame.init()
    display = Display()
    map = Map("map1")
    return map, display;


def redraw(map, display):
    map.draw(display)
    display.blit();
    pygame.display.flip()


def loop(map, display):
    global clock
    global MAX_FPS

    while True:
        delta = clock.tick(MAX_FPS)
        handleInput(map)
        redraw(map, display)


def main():
    map, display = init()
    loop(map, display)

if __name__ == "__main__":
    main()
