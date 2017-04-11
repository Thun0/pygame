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
    checking = False

    def __init__(self, display, filename):
        self.display = display
        with open(filename) as f:
            line = f.readline()
            self.width, self.height = [int(x) for x in line.split()]
            for i in range(self.width):
                line = f.readline()
                self.map.append([Tile(int(x)) for x in line.split()])
        self.font = pygame.font.SysFont(FONT, int(TILE_SIZE / 1.7))

    def drawValue(self, i, j):
        if self.map[i][j].value >= 0:
            color = (255, 255, 255)
            if self.checking and self.getNeighbourBulbs(i, j) != self.map[i][j].value:
                color = (230, 20, 20)
            textVal = self.font.render(str(self.map[i][j].value), True, color)
            textSize = self.font.size(str(self.map[i][j].value))
            textX = j * TILE_SIZE + TILE_SIZE / 2 - textSize[0] / 1.75
            textY = i * TILE_SIZE + TILE_SIZE / 2 - textSize[1] / 1.8
            self.display.background.blit(textVal, (textX, textY))

    def draw(self):
        for i in range(self.width):
            for j in range(self.height):
                color = (255, 255, 255)
                if self.map[i][j].type == Tile.WALL:
                    color = (0, 0, 0)
                elif self.map[i][j].value > 0:
                    color = (255, 255, 102)
                pygame.draw.rect(self.display.background, (0, 0, 0),
                                 (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(self.display.background, color,
                                 (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE - FRAME_WIDTH, TILE_SIZE - FRAME_WIDTH))
                if self.map[i][j].type == Tile.WALL:
                    self.drawValue(i, j)
                if self.map[i][j].type == Tile.CROSS:
                    self.drawCross(i, j)
                if self.map[i][j].type == Tile.BULB:
                    self.drawBulb(i, j)


    def toggleBulb(self, i, j):
        if self.map[i][j].type == Tile.WALL:
            return
        diff = 1
        if self.map[i][j].type == Tile.BULB:
            self.map[i][j].type = Tile.EMPTY
            diff = -1
        else:
            self.map[i][j].type = Tile.BULB
        idx = i
        while idx >= 0:
            if self.map[idx][j].type == Tile.WALL:
                break
            self.map[idx][j].value += diff
            idx -= 1
        idx = i+1
        while idx < self.width:
            if self.map[idx][j].type == Tile.WALL:
                break
            self.map[idx][j].value += diff
            idx += 1
        idx = j-1
        while idx >= 0:
            if self.map[i][idx].type == Tile.WALL:
                break
            self.map[i][idx].value += diff
            idx -= 1
        idx = j+1
        while idx < self.height:
            if self.map[i][idx].type == Tile.WALL:
                break
            self.map[i][idx].value += diff
            idx += 1

    def toggleCross(self, i, j):
        if self.map[i][j].type == Tile.WALL:
            return
        if self.map[i][j].type == Tile.CROSS:
            self.map[i][j].type = Tile.EMPTY
        else:
            if self.map[i][j].type == Tile.BULB:
                self.toggleBulb(i, j)
            self.map[i][j].type = Tile.CROSS

    def getIndices(self, x, y):
        tileX = int(x / TILE_SIZE)
        tileY = int(y / TILE_SIZE)
        if tileX >= self.width or tileY >= self.height:
            return -1, -1
        return tileX, tileY

    def drawCross(self, i, j):
        pygame.draw.line(self.display.background, (250, 30, 30),
                         (j * TILE_SIZE + TILE_SIZE / 4, i * TILE_SIZE + TILE_SIZE / 4),
                         (j * TILE_SIZE + TILE_SIZE * 3 / 4, i * TILE_SIZE + TILE_SIZE * 3 / 4), 2)
        pygame.draw.line(self.display.background, (250, 30, 30),
                         (j * TILE_SIZE + TILE_SIZE * 3 / 4, i * TILE_SIZE + TILE_SIZE / 4),
                         (j * TILE_SIZE + TILE_SIZE / 4, i * TILE_SIZE + TILE_SIZE * 3 / 4), 2)

    def drawBulb(self, i, j):
        color = (0, 0, 0)
        if self.checking and self.map[i][j].value > 1:
            color = (240, 30, 30)
        pygame.draw.circle(self.display.background, color,
                           (int(j * TILE_SIZE + TILE_SIZE/2), int(i * TILE_SIZE + TILE_SIZE/2)), int(TILE_SIZE/3), 2)

    # FIXME: needs implementation
    def checkSolution(self):
        pass

    # FIXME: needs implementation
    def getNeighbourBulbs(self, i, j):
        total = 0
        if i > 0 and self.map[i-1][j].type == Tile.BULB:
                total += 1
        if i < self.width-1 and self.map[i+1][j].type == Tile.BULB:
                total += 1
        if j > 0 and self.map[i][j-1].type == Tile.BULB:
                total += 1
        if j < self.height-1 and self.map[i][j+1].type == Tile.BULB:
                total += 1

        return total

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            tileY, tileX = map.getIndices(x, y)
            if tileX == -1:
                continue
            if event.button == 1:
                map.toggleBulb(tileX, tileY)
            elif event.button == 3:
                map.toggleCross(tileX, tileY)
            elif event.button == 2:
                map.checking = not map.checking


def init():
    print("Initializing game")
    pygame.init()
    display = Display()
    map = Map(display, "map1")
    return map, display


def redraw(map, display):
    map.draw()
    display.blit()
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
