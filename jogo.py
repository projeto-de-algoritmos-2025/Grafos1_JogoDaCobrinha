import pygame
from collections import deque
from enum import Enum

# Inicializar o pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GRAY = (150, 150, 150)

FONT = pygame.font.SysFont('Arial', 25)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Algorithm(Enum):
    MANUAL = 0
    BFS = 1
    DFS = 2

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.head_position = self.positions[0]
        #Inicializar o corpo com posições à esquerda da cabeça
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0] - i, self.positions[0][1]))
        self.is_alive = True
        self.score = 0
        self.grow = False
        