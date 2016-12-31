#!/usr/bin/python3

import pygame
import sys

clock = pygame.time.Clock()
MAX_FPS = 60
MAP_WIDTH = 80
MAP_HEIGHT = 50
TILE_SIZE = 20
FRAME_WIDTH = 2

class Map:
    """ map class """
    
    def __init__(self):
        self.map = [[0 for i in range(MAP_WIDTH)] for j in range(MAP_HEIGHT)]
        print("Initializing map")

    def draw(self, display):
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                color = 0
                if self.map[i][j] == 0:
                    color = 255
                pygame.draw.rect(display.background, (0, 0, 0),
                                 (j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(display.background, (color, color, color),
                                 (j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE-FRAME_WIDTH, TILE_SIZE-FRAME_WIDTH))

    def countNeighbours(self, old, tileX, tileY):
        neighbours = 0
        if tileX > 0:
            neighbours += old[tileX-1][tileY]
            if tileY > 0:
                neighbours += old[tileX-1][tileY-1]
            if tileY < MAP_WIDTH-1:
                neighbours += old[tileX-1][tileY+1]
        if tileX < MAP_HEIGHT-1:
            neighbours += old[tileX+1][tileY]
            if tileY > 0:
                neighbours += old[tileX+1][tileY-1]
            if tileY < MAP_WIDTH-1:
                neighbours += old[tileX+1][tileY+1]
        if tileY > 0:
            neighbours += old[tileX][tileY-1]
        if tileY < MAP_WIDTH-1:
                neighbours += old[tileX][tileY+1]
        return neighbours

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

    def paint(self, tileX, tileY):
        self.map[tileY][tileX] = Settings.painting

    def setPainting(self):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        tileX = int(mouseX / TILE_SIZE)
        tileY = int(mouseY / TILE_SIZE)
        if self.map[tileY][tileX] == 0:
            Settings.painting = 1
        else:
            Settings.painting = 0

class Display:

    def __init__(self):
        print("Initializing display")
        self.resolution = (MAP_WIDTH*TILE_SIZE, MAP_HEIGHT*TILE_SIZE)
        self.screen = pygame.display.set_mode(self.resolution)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((255, 255, 255))
        self.background = self.background.convert()

    def blit(self):
        self.screen.blit(self.background, (0, 0))

class Settings:
    mousePressed = 0
    painting = 1
    started = False
    delay = 30

def handleInput(map):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            Settings.started = not Settings.started
            if Settings.started:
                print("Simulation started")
            else:
                print("Simulation stopped")
        if not Settings.started:
            if event.type == pygame.MOUSEBUTTONDOWN:
                Settings.mousePressed = True
                map.setPainting();
            elif event.type == pygame.MOUSEBUTTONUP:
                Settings.mousePressed = False


def init():
    print("Initializing game")
    pygame.init()
    display = Display()
    map = Map()
    return map, display;


def update(delta, map):
    global clock
    text = "FPS: {0:.2f}".format(clock.get_fps())
    pygame.display.set_caption(text)
    (mouseX, mouseY) = pygame.mouse.get_pos()
    tileX = int(mouseX / TILE_SIZE)
    tileY = int(mouseY / TILE_SIZE)
    if Settings.mousePressed:
        map.paint(tileX, tileY)
    if Settings.started:
        map.update()
        pygame.time.wait(Settings.delay)

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
        update(delta, map)
        redraw(map, display)


def main():
    map, display = init()
    loop(map, display)


if __name__ == "__main__" :
    main()