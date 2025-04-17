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

  def update(self):
        if not self.is_alive:
            return
            
        # Get current head position
        current = self.positions[0]
        
        # Determine new head position
        x, y = current
        dx, dy = self.direction.value
        new_position = ((x + dx) % GRID_WIDTH, (y + dy) % GRID_HEIGHT)
        
        # Check for collision with self
        if new_position in self.positions[1:]:
            self.is_alive = False
            return
            
        # Move the snake
        self.positions.insert(0, new_position)
        self.head_position = new_position
        
        # Remove the tail if not growing
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
            self.score += 1
            
    def grow_snake(self):
        self.grow = True
    
    def change_direction(self, direction):
        # Can't move in the opposite direction
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        if direction != opposite_directions[self.direction]:
            self.direction = direction

class Food:
    def __init__(self):
        self.position = self.generate_position([])
        
    def generate_position(self, snake_positions):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if position not in snake_positions:
                return position
    
    def update(self, snake_positions):
        self.position = self.generate_position(snake_positions)

class Graph:
    def __init__(self, snake, food):
        self.snake = snake
        self.food = food
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        
    def get_neighbors(self, position):
        x, y = position
        # Get the four adjacent cells
        neighbors = [
            ((x + 1) % self.width, y),   # Right
            ((x - 1) % self.width, y),   # Left
            (x, (y + 1) % self.height),  # Down
            (x, (y - 1) % self.height)   # Up
        ]
        # Filter out neighbors that would cause collision with snake body
        valid_neighbors = [neighbor for neighbor in neighbors if neighbor not in self.snake.positions[:-1]]
        return valid_neighbors
    
    def calculate_direction(self, from_pos, to_pos):
        dx = (to_pos[0] - from_pos[0]) % self.width
        if dx > self.width // 2:
            dx = dx - self.width
        
        dy = (to_pos[1] - from_pos[1]) % self.height
        if dy > self.height // 2:
            dy = dy - self.height
            
        if dx == 1 or (dx < 0 and dx != -1):
            return Direction.RIGHT
        elif dx == -1 or (dx > 0 and dx != 1):
            return Direction.LEFT
        elif dy == 1 or (dy < 0 and dy != -1):
            return Direction.DOWN
        elif dy == -1 or (dy > 0 and dy != 1):
            return Direction.UP
        return None