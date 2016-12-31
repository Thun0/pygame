#!/usr/bin/python3

import sys

import pygame


class Settings:
    TILE_SIZE = 100
    FPS = 60
    BOARD_SIZE = 4
    FRAME_THICKNESS = 8
    OUTER_FRAME_THICKNESS = 20
    OFFSET = 60

class Board:

    def __init__(self):
        self.board = [[0 for i in range(Settings.BOARD_SIZE)] for j in range(Settings.BOARD_SIZE)]

    def tileColor(self, value):
        if value == 0:
            return (205, 193, 180)
        if value == 2:
            return (238, 228, 218)
        if value == 4:
            return (237, 224, 200)


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