#!/usr/bin/python3

import sys

import pygame

TILE_SIZE = 50
FRAME_WIDTH = 1
WIDTH = 600
HEIGHT = 600
FONT = "ubuntu"
drawPossibilities = False


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
    sums = []

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

        self.initSums()
        self.sumFont = pygame.font.SysFont(FONT, int(TILE_SIZE / 2))
        self.possibilitiesFont = pygame.font.SysFont(FONT, int(TILE_SIZE / 3.5))
        self.valueFont = pygame.font.SysFont(FONT, int(TILE_SIZE / 1.5))

    def initSums(self):
        sum2 = [[] in range(3)]
        sum2.append([1, 2])
        sum2.append([1, 3])
        sum2.append([1, 2, 3, 4])
        sum2.append([1, 2, 4, 5])
        sum2.append([1, 2, 3, 4, 5, 6])
        sum2.append([1, 2, 3, 5, 6, 7])
        sum2.append([1, 2, 3, 4, 5, 6, 7, 8])
        sum2.append([1, 2, 3, 4, 6, 7, 8, 9])
        sum2.append([2, 3, 4, 5, 6, 7, 8, 9])
        sum2.append([3, 4, 5, 7, 8, 9])
        sum2.append([4, 5, 6, 7, 8, 9])
        sum2.append([5, 6, 8, 9])
        sum2.append([6, 7, 8, 9])
        sum2.append([7, 9])
        sum2.append([8, 9])

        sum3 = [[] in range(6)]
        sum3.append([1, 2, 3])
        sum3.append([1, 2, 4])
        sum3.append([1, 2, 3, 4, 5])
        sum3.append([1, 2, 3, 4, 5, 6])
        sum3.append([1, 2, 3, 4, 5, 6, 7])
        sum3.append([1, 2, 3, 4, 5, 6, 7, 8])
        for i in range(7):
            sum3.append([i in range(1, 10)])
        sum3.append([2, 3, 4, 5, 6, 7, 8, 9])
        sum3.append([3, 4, 5, 6, 7, 8, 9])
        sum3.append([4, 5, 6, 7, 8, 9])
        sum3.append([5, 6, 7, 8, 9])
        sum3.append([6, 8, 9])
        sum3.append([7, 8, 9])

        sum4 = [[]in range(10)]
        sum4.append([1, 2, 3, 4])
        sum4.append([1, 2, 3, 5])
        sum4.append([1, 2, 3, 4, 5, 6])
        sum4.append([1, 2, 3, 4, 5, 6, 7])
        sum4.append([1, 2, 3, 4, 5, 6, 7, 8])
        for i in range(11):
            sum4.append([j for j in range(1, 10)])
        sum4.append([2, 3, 4, 5, 6, 7, 8, 9])
        sum4.append([3, 4, 5, 6, 7, 8, 9])
        sum4.append([4, 5, 6, 7, 8, 9])
        sum4.append([5, 7, 8, 9])
        sum4.append([6, 7, 8, 9])

        sum5 = [[]in range(15)]
        sum5.append([i for i in range(1, 6)])
        sum5.append([1, 2, 3, 4, 6])
        sum5.append([i in range(1, 8)])
        sum5.append([i in range(1, 9)])
        for i in range(13):
            sum5.append([j for j in range(1, 10)])
        sum5.append([i in range(2, 10)])
        sum5.append([i in range(3, 10)])
        sum5.append([4, 6, 7, 8, 9])
        sum5.append([5, 6, 7, 8, 9])

        sum6 = [[]in range(21)]
        sum6.append([1, 2, 3, 4, 5, 6])
        sum6.append([1, 2, 3, 4, 5, 7])
        sum6.append([i for i in range(1, 9)])
        for i in range(13):
            sum6.append([j for j in range(1, 10)])
        sum6.append([i in range(2, 10)])
        sum6.append([3, 5, 6, 7, 8, 9])
        sum6.append([4, 5, 6, 7, 8, 9])

        sum7 = [[] in range(28)]
        sum7.append([1, 2, 3, 4, 5, 6, 7])
        sum7.append([1, 2, 3, 4, 5, 6, 8])
        for i in range(11):
            sum7.append([j for j in range(1, 10)])
        sum7.append([2, 4, 5, 6, 7, 8, 9])
        sum7.append([3, 4, 5, 6, 7, 8, 9])

        sum8 = [[] in range(36)]
        sum8.append([1, 2, 3, 4, 5, 6, 7, 8])
        sum8.append([1, 2, 3, 4, 5, 6, 7, 9])
        sum8.append([1, 2, 3, 4, 5, 6, 8, 9])
        sum8.append([1, 2, 3, 4, 5, 7, 8, 9])
        sum8.append([1, 2, 3, 4, 6, 7, 8, 9])
        sum8.append([1, 2, 3, 5, 6, 7, 8, 9])
        sum8.append([1, 2, 4, 5, 6, 7, 8, 9])
        sum8.append([1, 3, 4, 5, 6, 7, 8, 9])
        sum8.append([2, 3, 4, 5, 6, 7, 8, 9])

        sum9 = [[] in range(45)]
        sum9.append([i in range(1, 10)])

        self.sums.append([])
        self.sums.append([])
        self.sums.append([sum2])
        self.sums.append([sum3])
        self.sums.append([sum4])
        self.sums.append([sum5])
        self.sums.append([sum6])
        self.sums.append([sum7])
        self.sums.append([sum8])
        self.sums.append([sum9])

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
        global drawPossibilities

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
                        if drawPossibilities:
                            for k in range(10):
                                if self.map[i][j].isPossible(k):
                                    self.drawPossibility(i, j, k)
                else:
                    self.drawSum(i, j)

    def drawValue(self, i, j):
        color = (0, 0, 0)
        textVal = self.valueFont.render(str(self.map[i][j].value), True, color)
        textSize = self.valueFont.size(str(self.map[i][j].value))
        textX = j * TILE_SIZE + TILE_SIZE /2 - textSize[0] / 1.75
        textY = i * TILE_SIZE + TILE_SIZE / 2 - textSize[1] / 1.8
        self.display.background.blit(textVal, (textX, textY))

    def deactivate(self):
        self.map[self.active[0]][self.active[1]].active = False
        self.active = (-1, -1)

    def activate(self, i, j):
        if self.map[j][i].type != Tile.EMPTY or self.active == (j, i):
            self.deactivate()
            return
        if self.active != (-1, -1):
            self.map[self.active[0]][self.active[1]].active = False
        self.active = (j, i)
        self.map[j][i].active = True

    def insertValue(self, val):
        if self.active != (-1, -1):
            self.map[self.active[0]][self.active[1]].value = val

    def deleteValue(self):
        if self.active != (-1, -1):
            self.map[self.active[0]][self.active[1]].value = -1


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
    global drawPossibilities

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                tileX, tileY = map.getIndices(x, y)
                if tileX != -1:
                    map.activate(tileX, tileY)
            if event.button == 3:
                drawPossibilities = not drawPossibilities
        if event.type == pygame.KEYDOWN:
            val = event.key - 48
            if 1 <= val <= 9:
                map.insertValue(val)
            if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                map.deleteValue()
            if event.key == pygame.K_ESCAPE:
                map.deactivate()


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
