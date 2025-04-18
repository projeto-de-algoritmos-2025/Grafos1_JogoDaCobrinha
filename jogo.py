import pygame
from collections import deque
from enum import Enum
import random


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

        # Obtém a posição atual da cabeça
        current = self.positions[0]

        # Determina a nova posição da cabeça
        x, y = current
        dx, dy = self.direction.value
        new_position = ((x + dx) % GRID_WIDTH, (y + dy) % GRID_HEIGHT)

         # Verifica colisão com o próprio corpo
        if new_position in self.positions[1:]:
            self.is_alive = False
            return

        # Move a cobrinha
        self.positions.insert(0, new_position)
        self.head_position = new_position

        # Remove o final da cauda se não estiver crescendo
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
            self.score += 1

    def grow_snake(self):
        self.grow = True

    def change_direction(self, direction):
    # Não pode mudar para a direção oposta
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
        # Obtém as quatro células adjacentes
        neighbors = [
            ((x + 1) % self.width, y),   # Direita
            ((x - 1) % self.width, y),   # Esquerda
            (x, (y + 1) % self.height),  # Baixo
            (x, (y - 1) % self.height)   # Cima
        ]
        # Filtra vizinhos que causariam colisão com o corpo da cobra
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
    
    def bfs(self):
        """aqui é o algoritmo da BFS pra encontrar o menor caminho até a comida"""
        start = self.snake.head_position
        queue = deque([start])
        visited = {start: None}
        
        while queue:
            current = queue.popleft()
            
            # Se a comida for encontrada
            if current == self.food.position:
                # Aqui se faz um backtrack pra encontrar o primeiro movimento.
                path = []
                while current != start:
                    path.append(current)
                    current = visited[current]
                
                # Aqui retorna a primera direção do movimento 
                if path:
                    next_pos = path[-1]
                    return self.calculate_direction(start, next_pos)
                return None  
            
            # Visitar os vizinhos
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited[neighbor] = current
                    queue.append(neighbor)
        
        # Se não exisitir  caminho para a comida, é só escolher um movimento válido.
        for direction in [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]:
            dx, dy = direction.value
            new_pos = ((start[0] + dx) % self.width, (start[1] + dy) % self.height)
            if new_pos not in self.snake.positions[1:]:
                return direction
                
        return None 
    
    def dfs(self):
        """Diferente da bfs a dsf apenas encontra um caminho para comida"""
        start = self.snake.head_position
        stack = [start]
        visited = {start: None}  # Aqui registra a posição anterior pro backtracking
        
        while stack:
            current = stack.pop()
            
            # Se a comida for encontrada
            if current == self.food.position:
                # Backtrack pra encontrar o primeiro movimento.
                path = []
                while current != start:
                    path.append(current)
                    current = visited[current]
                
                # Aqui retorna a primera direção do movimento 
                if path:
                    next_pos = path[-1]
                    return self.calculate_direction(start, next_pos)
                return None  
            
            # Aqui visita os vizinhos
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited[neighbor] = current
                    stack.append(neighbor)
        
        # Aqui se não houver caminho para a comida, basta escolher um movimento válido
        for direction in [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]:
            dx, dy = direction.value
            new_pos = ((start[0] + dx) % self.width, (start[1] + dy) % self.height)
            if new_pos not in self.snake.positions[1:]:
                return direction
                
        return None
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jogo da Cobrinha com BFS e DFS")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.graph = Graph(self.snake, self.food)
        self.algorithm = Algorithm.MANUAL
        self.game_speed = 10  

if __name__ == "__main__":
    game = Game()
    game.run()
    
def handle_events(self):
    # Lida com todos os eventos do Pygame (teclado, fechamento da janela)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Permite controle manual da direção apenas se o modo manual estiver ativo
            if event.key == pygame.K_UP and self.algorithm == Algorithm.MANUAL:
                self.snake.change_direction(Direction.UP)
            elif event.key == pygame.K_DOWN and self.algorithm == Algorithm.MANUAL:
                self.snake.change_direction(Direction.DOWN)
            elif event.key == pygame.K_LEFT and self.algorithm == Algorithm.MANUAL:
                self.snake.change_direction(Direction.LEFT)
            elif event.key == pygame.K_RIGHT and self.algorithm == Algorithm.MANUAL:
                self.snake.change_direction(Direction.RIGHT)
            # Troca entre os modos de controle (manual, BFS, DFS)
            elif event.key == pygame.K_1:
                self.algorithm = Algorithm.MANUAL
            elif event.key == pygame.K_2:
                self.algorithm = Algorithm.BFS
            elif event.key == pygame.K_3:
                self.algorithm = Algorithm.DFS
            # Reinicia o jogo
            elif event.key == pygame.K_r:
                self.reset()
            # Aumenta ou diminui a velocidade do jogo
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                self.game_speed = min(60, self.game_speed + 5)
            elif event.key == pygame.K_MINUS:
                self.game_speed = max(5, self.game_speed - 5)

def update(self):
    # Não atualiza se a cobra estiver morta (fim de jogo)
    if not self.snake.is_alive:
        return

    # Usa o algoritmo selecionado para decidir a direção da cobra
    if self.algorithm == Algorithm.BFS:
        direction = self.graph.bfs()
        if direction:
            self.snake.change_direction(direction)
    elif self.algorithm == Algorithm.DFS:
        direction = self.graph.dfs()
        if direction:
            self.snake.change_direction(direction)

    # Atualiza a posição da cobra no grid
    self.snake.update()

    # Verifica se a cobra comeu a comida
    if self.snake.head_position == self.food.position:
        self.snake.grow_snake()  # Aumenta o tamanho da cobra
        self.food.update(self.snake.positions)  # Posiciona nova comida

def draw(self):
    # Limpa a tela
    self.screen.fill(BLACK)

    # Desenha as linhas da grade (opcional)
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT), 1)
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y), 1)

    # Desenha a comida como um quadrado vermelho
    food_rect = pygame.Rect(
        self.food.position[0] * CELL_SIZE,
        self.food.position[1] * CELL_SIZE,
        CELL_SIZE, CELL_SIZE
    )
    pygame.draw.rect(self.screen, RED, food_rect)

    # Desenha cada parte da cobra
    for i, position in enumerate(self.snake.positions):
        snake_rect = pygame.Rect(
            position[0] * CELL_SIZE,
            position[1] * CELL_SIZE,
            CELL_SIZE, CELL_SIZE
        )
        if i == 0:  # Cabeça em azul
            pygame.draw.rect(self.screen, BLUE, snake_rect)
        else:       # Corpo em verde
            pygame.draw.rect(self.screen, GREEN, snake_rect)




    
