#!/usr/bin/python3

import sys

import pygame

TILE_SIZE = 25
FRAME_WIDTH = 1
WIDTH = 300
HEIGHT = 300
FONT = "notomono"

class Tile:

    EMPTY = 0
    WALL = 1
    BULB = 2
    CROSS = 3

    type = EMPTY
    lighted = False
    value = 0

    def __init__(self):
        pass

    def __init__(self, val):
        if val != 0:
            self.type = self.WALL
            self.value = val-2


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
            for i in range(self.width):
                line = f.readline()
                self.map.append([Tile(int(x)) for x in line.split()])
        self.font = pygame.font.SysFont(FONT, int(TILE_SIZE / 1.7))

    def draw(self, display):
        for i in range(self.width):
            for j in range(self.height):
                color = 0
                if self.map[i][j].type == Tile.EMPTY:
                    color = 255
                pygame.draw.rect(display.background, (0, 0, 0),
                                 (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(display.background, (color, color, color),
                                 (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE - FRAME_WIDTH, TILE_SIZE - FRAME_WIDTH))
                if self.map[i][j].type == Tile.WALL and self.map[i][j].value >= 0:
                    #self.font.set_bold(True)
                    textVal = self.font.render(str(self.map[i][j].value), True, (255, 255, 255))
                    textSize = self.font.size(str(self.map[i][j].value))
                    textX = j * TILE_SIZE + TILE_SIZE / 2 - textSize[0] / 1.75
                    textY = i * TILE_SIZE + TILE_SIZE / 2 - textSize[1] / 1.8
                    display.background.blit(textVal, (textX, textY))

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
    while True:
        handleInput(map)
        redraw(map, display)


def main():
    map, display = init()
    loop(map, display)

if __name__ == "__main__":
    main()
