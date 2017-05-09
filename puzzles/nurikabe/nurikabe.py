import sys
import pygame

MAX_FPS = 60
TILE_SIZE = 20
FRAME_WIDTH = 1
WIDTH = 800
HEIGHT = 600
FONT = "ubuntu"


class Board:
    EMPTY = 0
    FILL = 5
    ISLAND = 6
    map = []
    width = 0
    height = 0

    def __init__(self, display, filename):
        zz = []
        self.display = display
        self.valueFont = pygame.font.SysFont(FONT, int(TILE_SIZE / 1.5))
        with open(filename) as f:
            line = f.readline()
            self.width, self.height = [int(x) for x in line.split()]
            for i in range(self.width):
                line = f.readline()
                zz.append([int(x) for x in line.split()])
            self.map = list(map(list, zip(*zz)))

    def draw(self):
        for i in range(self.width):
            for j in range(self.height):
                color = (255, 255, 255)
                if self.map[i][j] == Board.FILL:
                    color = (0, 0, 0)
                pygame.draw.rect(self.display.background, (0, 0, 0),
                                 (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(self.display.background, color,
                                 (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE - FRAME_WIDTH, TILE_SIZE - FRAME_WIDTH))
                if self.map[i][j] == self.ISLAND:
                    pygame.draw.ellipse(self.display.background, (0, 0, 0),
                                        (i * TILE_SIZE+TILE_SIZE/4, j * TILE_SIZE+TILE_SIZE/4, TILE_SIZE/2, TILE_SIZE/2))
                if 4 >= self.map[i][j] >= 1:
                    color = (0, 0, 0)
                    textVal = self.valueFont.render(str(self.map[i][j]), True, color)
                    textSize = self.valueFont.size(str(self.map[i][j]))
                    textX = i * TILE_SIZE + TILE_SIZE / 2 - textSize[0] / 1.75
                    textY = j * TILE_SIZE + TILE_SIZE / 2 - textSize[1] / 1.8
                    self.display.background.blit(textVal, (textX, textY))

    def getIndices(self, x, y):
        tileX = int(x / TILE_SIZE)
        tileY = int(y / TILE_SIZE)
        if tileX >= self.width or tileY >= self.height or 4 >= self.map[tileX][tileY] >= 1:
            return -1, -1
        return tileX, tileY

    def toggleFill(self, x, y):
        if self.map[x][y] == self.FILL:
            self.map[x][y] = self.EMPTY
        else:
            self.map[x][y] = self.FILL

    def toggleIsland(self, x, y):
        if self.map[x][y] == self.ISLAND:
            self.map[x][y] = self.EMPTY
        else:
            self.map[x][y] = self.ISLAND


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


def handleInput(map, display):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            tileX, tileY = map.getIndices(x, y)
            if tileX != -1:
                if event.button == 1:
                    map.toggleFill(tileX, tileY)
                elif event.button == 3:
                    map.toggleIsland(tileX, tileY)


def init():
    print("Initializing game")
    pygame.init()
    display = Display()
    map = Board(display, "nurikabe1")
    return map, display


def redraw(map, display):
    map.draw()
    display.blit()
    pygame.time.wait(50)
    pygame.display.flip()


def loop(map, display):
    global MAX_FPS

    clock = pygame.time.Clock()
    while True:
        clock.tick(MAX_FPS)
        handleInput(map, display)
        redraw(map, display)


def main():
    map, display = init()
    loop(map, display)


if __name__ == "__main__":
    main()
