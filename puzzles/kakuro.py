#!/usr/bin/python3

import sys

import pygame

TILE_SIZE = 50
FRAME_WIDTH = 1
WIDTH = 600
HEIGHT = 600
FONT = "ubuntu"
drawPossibilities = True


class Tile:
    EMPTY = 0
    WALL = 1
    SUM_DOWN = 2
    SUM_RIGHT = 3
    SUM_BOTH = 4

    type = EMPTY
    sumRight = -1
    sumDown = -1
    value = -1
    possible = [True for i in range(10)]
    active = False

    def __init__(self, val):
        self.possible[0] = False
        if val == 1:
            self.type = self.WALL
        elif val == 2:
            self.type = self.SUM_DOWN
        elif val == 3:
            self.type = self.SUM_RIGHT
        elif val == 4:
            self.type = self.SUM_BOTH

    def getPossibilitiesCount(self):
        sum = 0
        for possible in self.possible:
            if possible:
                sum += 1
        return sum

    def getPossibilities(self):
        possibilities = []
        for i in range(1, 10):
            if self.possible[i]:
                possibilities.append(i)
        return possibilities

    def isPossible(self, val):
        return self.possible[val]

class Map:
    map = []
    downTiles = []
    rightTiles = []
    width = 0
    height = 0
    active = (-1, -1)

    def __init__(self, display, filename):
        self.display = display
        with open(filename) as f:
            line = f.readline()
            self.width, self.height = [int(x) for x in line.split()]
            for i in range(self.width):
                line = f.readline()
                self.map.append([Tile(int(x)) for x in line.split()])
                for j in range(self.height):
                    if self.map[-1][j].type == Tile.SUM_DOWN or self.map[-1][j].type == Tile.SUM_BOTH:
                        self.downTiles.append(self.map[-1][j])
                    if self.map[-1][j].type == Tile.SUM_RIGHT or self.map[-1][j].type == Tile.SUM_BOTH:
                        self.rightTiles.append(self.map[-1][j])
            # down sums
            line = f.readline()
            idx = 0
            for value in line.split():
                self.downTiles[idx].sumDown = value;
                idx += 1
            # right sums
            line = f.readline()
            idx = 0
            for value in line.split():
                self.rightTiles[idx].sumRight = value;
                idx += 1

        self.sumFont = pygame.font.SysFont(FONT, int(TILE_SIZE / 2))
        self.possibilitiesFont = pygame.font.SysFont(FONT, int(TILE_SIZE / 3.5))
        self.valueFont = pygame.font.SysFont(FONT, int(TILE_SIZE / 1.5))

    def drawPossibility(self, i, j, val):
        color = (0, 0, 0)
        textVal = self.possibilitiesFont.render(str(val), True, color)
        offsetX = 0
        offsetY = 0
        if 4 <= val <= 6:
            offsetY = TILE_SIZE / 3
        if 7 <= val <= 9:
            offsetY = TILE_SIZE * 2 / 3
        if val == 2 or val == 5 or val == 8:
            offsetX = TILE_SIZE / 3
        if val == 3 or val == 6 or val == 9:
            offsetX = TILE_SIZE * 2 / 3
        textX = j * TILE_SIZE + offsetX + TILE_SIZE*0.07
        textY = i * TILE_SIZE + offsetY
        self.display.background.blit(textVal, (textX, textY))

    def drawSum(self, i, j):
        if self.map[i][j].sumRight != -1:
            color = (0, 0, 0)
            textVal = self.sumFont.render(str(self.map[i][j].sumRight), True, color)
            textSize = self.sumFont.size(str(self.map[i][j].sumRight))
            textX = j * TILE_SIZE + TILE_SIZE * 3 / 4 - textSize[0] / 1.75
            textY = i * TILE_SIZE + TILE_SIZE / 4 - textSize[1] / 1.8
            self.display.background.blit(textVal, (textX, textY))
        if self.map[i][j].sumDown != -1:
            color = (0, 0, 0)
            textVal = self.sumFont.render(str(self.map[i][j].sumDown), True, color)
            textSize = self.sumFont.size(str(self.map[i][j].sumDown))
            textX = j * TILE_SIZE
            textY = i * TILE_SIZE + TILE_SIZE * 3 / 4 - textSize[1] / 1.8
            self.display.background.blit(textVal, (textX, textY))

    def getIndices(self, x, y):
        tileX = int(x / TILE_SIZE)
        tileY = int(y / TILE_SIZE)
        if tileX >= self.width or tileY >= self.height:
            return -1, -1
        return tileX, tileY

    def draw(self):
        for i in range(self.width):
            for j in range(self.height):
                color = (255, 255, 255)
                if self.map[i][j].type != Tile.EMPTY:
                    color = (150, 150, 150)
                if self.map[i][j].active:
                    frame = FRAME_WIDTH+1
                    pygame.draw.rect(self.display.background, (250, 50, 50),
                                     (j * TILE_SIZE - frame, i * TILE_SIZE - frame, TILE_SIZE+frame, TILE_SIZE+frame))
                    pygame.draw.rect(self.display.background, color,
                                     (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE - frame, TILE_SIZE - frame))
                else:
                    pygame.draw.rect(self.display.background, (0, 0, 0),
                                     (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.display.background, color,
                                     (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE - FRAME_WIDTH, TILE_SIZE - FRAME_WIDTH))
                if self.map[i][j].type != Tile.EMPTY:
                    pygame.draw.line(self.display.background, (0, 0, 0), (j * TILE_SIZE, i * TILE_SIZE),
                                     ((j + 1) * TILE_SIZE - 1, (i + 1) * TILE_SIZE - 1), 1)

                if self.map[i][j].type == Tile.EMPTY:
                    if self.map[i][j].value != -1:
                        self.drawValue(i, j)
                    else:
                        for k in range(10):
                            if self.map[i][j].isPossible(k):
                                self.drawPossibility(i, j, k)
                else:
                    self.drawSum(i, j)

    def deactivate(self):
        self.map[self.active[1]][self.active[0]].active = False
        self.active = (-1, -1)

    def activate(self, i, j):
        if self.map[j][i].type != Tile.EMPTY or self.active == (i, j):
            print("JEST")
            self.deactivate()
            return
        if self.active != (-1, -1):
            self.map[self.active[1]][self.active[0]].active = False
        self.active = (i, j)
        self.map[j][i].active = True



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
            tileX, tileY = map.getIndices(x, y)
            if tileX != -1:
                map.activate(tileX, tileY)



def init():
    print("Initializing game")
    pygame.init()
    display = Display()
    map = Map(display, "kakuro1")
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
