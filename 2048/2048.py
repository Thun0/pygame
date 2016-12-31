#!/usr/bin/python3

import sys

import pygame
import random

class Settings:
    TILE_SIZE = 100
    FPS = 60
    BOARD_SIZE = 4
    FRAME_THICKNESS = 8
    OUTER_FRAME_THICKNESS = 20
    OFFSET = 60
    FONT = "freeserif"

class Board:

    def __init__(self):
        self.board = [[0 for i in range(Settings.BOARD_SIZE)] for j in range(Settings.BOARD_SIZE)]
        self.board[random.randint(0, Settings.BOARD_SIZE - 1)][random.randint(0, Settings.BOARD_SIZE - 1)] += 2
        self.board[random.randint(0, Settings.BOARD_SIZE - 1)][random.randint(0, Settings.BOARD_SIZE - 1)] += 2
        self.board[random.randint(0, Settings.BOARD_SIZE - 1)][random.randint(0, Settings.BOARD_SIZE - 1)] += 2
        self.font = pygame.font.SysFont(Settings.FONT, int(Settings.TILE_SIZE/2))

    def tileColor(self, value):
        if value == 0:
            return (205, 193, 180)
        if value == 2:
            return (238, 228, 218)
        if value == 4:
            return (237, 224, 200)
        if value == 8:
            return (242, 177, 121)
        if value == 16:
            return (236, 141, 83)
        if value == 32:
            return (245, 124, 95)
        if value == 64:
            return (247, 94, 60)
        if value == 128:
            return (244, 216, 109)
        if value == 256:
            return (241, 208, 75)
        if value == 512:
            return (228, 192, 42)
        if value == 1024:
            return (239, 196, 65)
        else:
            return (238, 194, 46)


    def draw(self, display):

        frameSize = Settings.TILE_SIZE * Settings.BOARD_SIZE + 2*Settings.OUTER_FRAME_THICKNESS - Settings.FRAME_THICKNESS
        pygame.draw.rect(display.background, (187, 173, 160),
                         (Settings.OFFSET - Settings.OUTER_FRAME_THICKNESS,
                          Settings.OFFSET - Settings.OUTER_FRAME_THICKNESS, frameSize, frameSize))

        for i in range(Settings.BOARD_SIZE):
            for j in range(Settings.BOARD_SIZE):
                pygame.draw.rect(display.background, self.tileColor(self.board[i][j]),
                                 (j * Settings.TILE_SIZE + Settings.OFFSET,
                                  i * Settings.TILE_SIZE + Settings.OFFSET,
                                  Settings.TILE_SIZE - Settings.FRAME_THICKNESS,
                                  Settings.TILE_SIZE - Settings.FRAME_THICKNESS))
                if self.board[i][j] > 0:
                    if self.board[i][j] < 8:
                        color = (119, 110, 101)
                    else:
                        color = (248, 246, 242)
                    textVal = self.font.render(str(self.board[i][j]), True, color)
                    textSize = self.font.size(str(self.board[i][j]))
                    textX = j * Settings.TILE_SIZE + Settings.OFFSET + Settings.TILE_SIZE/2 - textSize[0]/1.75
                    textY = i * Settings.TILE_SIZE + Settings.OFFSET + Settings.TILE_SIZE/2 - textSize[1]/1.8
                    display.background.blit(textVal, (textX, textY))


class Display:


    def __init__(self):
        displaySize = Settings.BOARD_SIZE*Settings.TILE_SIZE + 2*Settings.OFFSET
        self.resolution = (displaySize, displaySize)
        self.screen = pygame.display.set_mode(self.resolution)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((250, 248, 239))
        self.background = self.background.convert()

    def blit(self):
        self.screen.blit(self.background, (0, 0))


def init():
    print("Initializing game")
    pygame.init()
    pygame.display.set_caption("2048")
    display = Display()
    board = Board()
    return board, display


def handleInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            pass


def update(delta):
    (mouseX, mouseY) = pygame.mouse.get_pos()


def redraw(board, display):
    display.blit()
    board.draw(display)
    pygame.display.flip()


def loop(board, display):
    clock = pygame.time.Clock()

    while True:
        delta = clock.tick(Settings.FPS)
        handleInput()
        update(delta)
        redraw(board, display)


def main():
    board, display = init()
    loop(board, display)


if __name__ == "__main__" :
    main()