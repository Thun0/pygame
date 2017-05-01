#!/usr/bin/python3

import sys
import pygame

from tkinter import Tk, filedialog

MAX_FPS = 60
TILE_SIZE = 50
FRAME_WIDTH = 1
WIDTH = 800
HEIGHT = 600
FONT = "ubuntu"
drawPossibilities = False


class Tile:

    EMPTY = 0
    WALL = 1
    SUM_DOWN = 2
    SUM_RIGHT = 3
    SUM_BOTH = 4

    def __init__(self, val):
        self.type = self.EMPTY
        self.sumRight = -1
        self.sumDown = -1
        self.value = -1
        self.possible = []
        self.active = False
        self.possible = [True for i in range(10)]
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


class Board:
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
                self.downTiles[idx].sumDown = int(value)
                idx += 1
            # right sums
            line = f.readline()
            idx = 0
            for value in line.split():
                self.rightTiles[idx].sumRight = int(value)
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

class Solver:

    sums = []

    def __init__(self, board):
        self.board = board
        self.initSums()

    def initSums(self):
        sum1 = [[], [1], [2], [3], [4], [5], [6], [7], [8], [9]]

        sum2 = [[] for i in range(3)]
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

        sum3 = [[] for i in range(6)]
        sum3.append([1, 2, 3])
        sum3.append([1, 2, 4])
        sum3.append([1, 2, 3, 4, 5])
        sum3.append([1, 2, 3, 4, 5, 6])
        sum3.append([1, 2, 3, 4, 5, 6, 7])
        sum3.append([1, 2, 3, 4, 5, 6, 7, 8])
        for i in range(7):
            sum3.append([i for i in range(1, 10)])
        sum3.append([2, 3, 4, 5, 6, 7, 8, 9])
        sum3.append([3, 4, 5, 6, 7, 8, 9])
        sum3.append([4, 5, 6, 7, 8, 9])
        sum3.append([5, 6, 7, 8, 9])
        sum3.append([6, 8, 9])
        sum3.append([7, 8, 9])

        sum4 = [[] for i in range(10)]
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

        sum5 = [[] for i in range(15)]
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

        sum6 = [[] for i in range(21)]
        sum6.append([1, 2, 3, 4, 5, 6])
        sum6.append([1, 2, 3, 4, 5, 7])
        sum6.append([i for i in range(1, 9)])
        for i in range(13):
            sum6.append([j for j in range(1, 10)])
        sum6.append([i for i in range(2, 10)])
        sum6.append([3, 5, 6, 7, 8, 9])
        sum6.append([4, 5, 6, 7, 8, 9])

        sum7 = [[] for i in range(28)]
        sum7.append([1, 2, 3, 4, 5, 6, 7])
        sum7.append([1, 2, 3, 4, 5, 6, 8])
        for i in range(11):
            sum7.append([j for j in range(1, 10)])
        sum7.append([2, 4, 5, 6, 7, 8, 9])
        sum7.append([3, 4, 5, 6, 7, 8, 9])

        sum8 = [[] for i in range(36)]
        sum8.append([1, 2, 3, 4, 5, 6, 7, 8])
        sum8.append([1, 2, 3, 4, 5, 6, 7, 9])
        sum8.append([1, 2, 3, 4, 5, 6, 8, 9])
        sum8.append([1, 2, 3, 4, 5, 7, 8, 9])
        sum8.append([1, 2, 3, 4, 6, 7, 8, 9])
        sum8.append([1, 2, 3, 5, 6, 7, 8, 9])
        sum8.append([1, 2, 4, 5, 6, 7, 8, 9])
        sum8.append([1, 3, 4, 5, 6, 7, 8, 9])
        sum8.append([2, 3, 4, 5, 6, 7, 8, 9])

        sum9 = [[] for i in range(45)]
        sum9.append([i in range(1, 10)])

        self.sums.append([])
        self.sums.append(sum1)
        self.sums.append(sum2)
        self.sums.append(sum3)
        self.sums.append(sum4)
        self.sums.append(sum5)
        self.sums.append(sum6)
        self.sums.append(sum7)
        self.sums.append(sum8)
        self.sums.append(sum9)

    def getRightEmptyTilesCount(self, i, j):
        if self.board.map[i][j].type != Tile.SUM_RIGHT and self.board.map[i][j].type != Tile.SUM_BOTH:
            return -1
        count = 0
        j += 1
        while j < self.board.height and self.board.map[i][j].type == Tile.EMPTY:
            if self.board.map[i][j].value == -1:
                count += 1
            j += 1
        return count

    def getDownEmptyTilesCount(self, i, j):
        if self.board.map[i][j].type != Tile.SUM_DOWN and self.board.map[i][j].type != Tile.SUM_BOTH:
            return -1
        count = 0
        i += 1
        while i < self.board.width and self.board.map[i][j].type == Tile.EMPTY:
            if self.board.map[i][j].value == -1:
                count += 1
            i += 1
        return count

    def getRightTilesCount(self, i, j):
        if self.board.map[i][j].type != Tile.SUM_RIGHT and self.board.map[i][j].type != Tile.SUM_BOTH:
            return -1
        count = 0
        j += 1
        while j < self.board.height and self.board.map[i][j].type == Tile.EMPTY:
            count += 1
            j += 1
        return count

    def getDownTilesCount(self, i, j):
        if self.board.map[i][j].type != Tile.SUM_DOWN and self.board.map[i][j].type != Tile.SUM_BOTH:
            return -1
        count = 0
        i += 1
        while i < self.board.width and self.board.map[i][j].type == Tile.EMPTY:
            count += 1
            i += 1
        return count

    def updateTilePossibilities(self, tile, list):
        change = False
        for i in range(10):
            if i not in list and tile.possible[i] == True:
                tile.possible[i] = False
                change = True
        return change

    def updateRightPossibilities(self, i, j):
        change = False
        if self.board.map[i][j].sumRight == -1:
            return False
        sum = self.getRemainingRightSum(i, j)
        print("Remaining r-sum({}, {}): {}".format(i, j, sum))
        steps = self.getRightTilesCount(i, j)
        count = self.getRightEmptyTilesCount(i, j)
        for k in range(steps):
            j += 1
            if self.board.map[i][j].value == -1:
                print("Pos({}, {}): {}||{}".format(i, j, count, sum))
                change = change | self.updateTilePossibilities(self.board.map[i][j], self.sums[count][sum])
        return change

    def updateDownPossibilities(self, i, j):
        change = False
        if self.board.map[i][j].sumDown == -1:
            return False
        sum = self.getRemainingDownSum(i, j)
        print("Remaining d-sum({}, {}): {}".format(i, j, sum))
        steps = self.getDownTilesCount(i, j)
        count = self.getDownEmptyTilesCount(i, j)
        for k in range(steps):
            i += 1
            if self.board.map[i][j].value == -1:
                print("Pos({}, {}): {}||{}".format(i, j, count, sum))
                change = change | self.updateTilePossibilities(self.board.map[i][j], self.sums[count][sum])
        return change

    def updateValue(self, i, j):
        print("Updated val({}, {})".format(i, j))
        change = False
        if self.board.map[i][j].getPossibilitiesCount() == 1:
            for k in range(10):
                if self.board.map[i][j].possible[k] == True:
                    self.board.map[i][j].value = k
                    self.board.map[i][j].possible[k] = False
                    change = True
        return change

    def removeDuplicates(self, i, j):
        change = False
        val = self.board.map[i][j].value
        if val == -1:
            return change
        idx = j
        while idx > 0 and self.board.map[i][idx].type == Tile.EMPTY:
            idx -= 1
            if self.board.map[i][idx].possible[val]:
                self.board.map[i][idx].possible[val] = False
                self.updateValue(i, idx)
                self.removeDuplicates(i, idx)
                change = True
        idx = j
        while idx < self.board.height-1 and self.board.map[i][idx].type == Tile.EMPTY:
            idx += 1
            if self.board.map[i][idx].possible[val]:
                self.board.map[i][idx].possible[val] = False
                self.updateValue(i, idx)
                self.removeDuplicates(i, idx)
                change = True
        idx = i
        while idx > 0 and self.board.map[idx][j].type == Tile.EMPTY:
            idx -= 1
            if self.board.map[idx][j].possible[val]:
                self.board.map[idx][j].possible[val] = False
                self.updateValue(idx, j)
                self.removeDuplicates(idx, j)
                change = True
        idx = i
        while idx < self.board.height - 1 and self.board.map[idx][j].type == Tile.EMPTY:
            idx += 1
            if self.board.map[idx][j].possible[val]:
                self.board.map[idx][j].possible[val] = False
                self.updateValue(idx, j)
                self.removeDuplicates(idx, j)
                change = True
        return change

    def updatePossibilities(self):
        global drawPossibilities

        drawPossibilities = True
        change = True
        while change == True:
            change = False
            redraw(self.board, self.board.display)
            #waitForClick()
            print("Iteration!")
            for i in range(self.board.width):
                for j in range(self.board.height):
                    if self.board.map[i][j].type == Tile.EMPTY:
                        #change = change | self.updateValue(i, j)
                        #change = change | self.removeDuplicates(i, j)
                        if self.updateValue(i, j):
                            print("Update value for: {}, {}".format(i, j))
                            change = True
                        if self.removeDuplicates(i, j):
                            print("Removed duplicates for: {}, {}".format(i, j))
                            change = True
                    else:
                        #change = change | self.updateDownPossibilities(i, j)
                        #change = change | self.updateRightPossibilities(i, j)
                        if self.updateRightPossibilities(i, j):
                            print("Updated r-pos for: {}, {}".format(i, j))
                            change = True
                        if self.updateDownPossibilities(i, j):
                            print("Updated d-pos for: {}, {}".format(i, j))
                            change = True


    def getRemainingRightSum(self, i, j):
        idx = j
        if self.board.map[i][j].type != Tile.SUM_RIGHT and self.board.map[i][j].type != Tile.SUM_BOTH:
            return -1337
        currentSum = 0
        count = self.getRightTilesCount(i, j)
        for k in range(count):
            idx += 1
            if self.board.map[i][idx].value != -1:
                currentSum += self.board.map[i][idx].value
        return self.board.map[i][j].sumRight - currentSum

    def getRemainingDownSum(self, i, j):
        idx = i
        if self.board.map[i][j].type != Tile.SUM_DOWN and self.board.map[i][j].type != Tile.SUM_BOTH:
            return -1337
        currentSum = 0
        count = self.getDownTilesCount(i, j)
        for k in range(count):
            idx += 1
            if self.board.map[idx][j].value != -1:
                currentSum += self.board.map[idx][j].value
        return self.board.map[i][j].sumDown - currentSum

class Editor:
    def __init__(self):
        print("Initializing editor")

    def blit(self):
        pass


class Button:

    x = 0
    y = 0
    w = 100
    h = 40
    text = "Button"
    onClick = lambda *args: None

    def __init__(self, display, text):
        self.display = display
        self.text = text
        self.font = pygame.font.SysFont(FONT, int(self.h / 2))

    def setDimensions(self, width, height):
        self.w = width
        self.h = height

    def setHeight(self, height):
        self.h = height

    def setWidth(self, width):
        self.w = width

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(self.display.background, self.color, (self.x, self.y, self.w, self.h))
        textVal = self.font.render(str(self.text), True, (0, 0, 0))
        textSize = self.font.size(str(self.text))
        textX = self.x + self.w/2 - textSize[0] / 2
        textY = self.y + self.h/2 - textSize[1] / 2
        self.display.background.blit(textVal, (textX, textY))

    def inBounds(self, x, y):
        if x >= self.x and x <= self.x+self.w and y >= self.y and y <= self.y+self.w:
            return True
        return False

    color = (150, 150, 150)


class Display:

    drawables = []

    def __init__(self):
        print("Initializing display")
        self.resolution = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(self.resolution)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255, 255, 255))
        self.background = self.background.convert()

    def blit(self):
        for drawable in self.drawables:
            drawable.draw()
        self.screen.blit(self.background, (0, 0))

    def add(self, drawable):
        self.drawables.append(drawable)

    def checkClick(self, x, y):
        print("C1: {}, {}".format(x, y))
        for drawable in self.drawables:
            print("C2: ({}, {}) - ({}, {})".format(drawable.x, drawable.y, drawable.x + drawable.w, drawable.y + drawable.h))
            if type(drawable) is Button and drawable.inBounds(x, y):
                drawable.onClick()


class MenuView:

    x = 0
    y = 0
    SPACING = 10

    def __init__(self, display):
        self.buttons = []
        self.display = display

    def addButton(self, button):
        if len(self.buttons) == 0:
            buttonY = self.y
        else:
            buttonY = self.buttons[-1].y + self.buttons[-1].h + self.SPACING
        self.buttons.append(button)
        self.buttons[-1].setPos(self.x, buttonY)
        self.display.add(self.buttons[-1])

    def setPos(self, x, y):
        self.x = x
        self.y = y
        # TODO: update buttons positions


def initMainMenu(display, solver):
    mainMenu = MenuView(display)
    mainMenu.setPos(550, 50)
    b = Button(display, "Solve")
    b.onClick = solver.updatePossibilities
    mainMenu.addButton(b)
    b = Button(display, "Editor")
    mainMenu.addButton(b)


def handleInput(map, display, solver):
    global drawPossibilities

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                display.checkClick(x, y)
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
    map = Board(display, "kakuro1")
    solver = Solver(map)
    return map, display, solver


def waitForClick():
    zzz = True
    while zzz:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                zzz = False


def chooseFile():
    Tk().withdraw()
    filename = filedialog.askopenfilename()
    return filename


def redraw(map, display):
    map.draw()
    display.blit()
    pygame.time.wait(50)
    pygame.display.flip()


def loop(map, display, solver):
    global MAX_FPS

    clock = pygame.time.Clock()
    while True:
        clock.tick(MAX_FPS)
        handleInput(map, display, solver)
        redraw(map, display)


def main():
    map, display, solver = init()
    initMainMenu(display, solver)
    loop(map, display, solver)


if __name__ == "__main__":
    main()
