import pygame
import sys
import math

# Constants
SCREEN_WIDTH = 560
SCREEN_HEIGHT = 620
CELL_SIZE = 20
FPS = 10

# Colors
BLACK = (44, 44, 44)
WHITE = (255, 255, 255)
BLUE = (13, 16, 12)
YELLOW = (222, 216, 177)
RED = (255, 204, 204)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Pacman Class
class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = LEFT
        self.mouth_open = True
        self.angle = 0

    def move(self, maze):
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]
        if maze[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y
            return True
        return False

    def draw(self, screen):
        center = (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2 + 60)
        radius = CELL_SIZE // 2 - 2
        mouth_angle = 30 if self.mouth_open else 0

        pygame.draw.circle(screen, YELLOW, center, radius)

        if self.direction == RIGHT:
            self.angle = 0
        elif self.direction == LEFT:
            self.angle = 180
        elif self.direction == UP:
            self.angle = 90
        elif self.direction == DOWN:
            self.angle = 270

        pygame.draw.polygon(screen, BLACK, [
            center,
            (center[0] + radius * math.cos(math.radians(self.angle - mouth_angle)),
             center[1] - radius * math.sin(math.radians(self.angle - mouth_angle))),
            (center[0] + radius * math.cos(math.radians(self.angle + mouth_angle)),
             center[1] - radius * math.sin(math.radians(self.angle + mouth_angle))),
        ])

        self.mouth_open = not self.mouth_open

# Game Initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

# Font for Title and Score
font = pygame.font.SysFont("arial", 24)

# Initial Score
score = 0

# Define the Maze (Classic Layout)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 0
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 1
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1],  # 2
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],  # 3
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1],  # 4
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],  # 5
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1],  # 6
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 7
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],  # 8
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],  # 9
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],  # 10
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 11
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],  # 12
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],  # 13
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],  # 14
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 15
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],  # 16
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 17
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],  # 18
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],  # 19
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1],  # 20
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],  # 21
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],  # 22
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 23
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 24
]

# Create Pacman
pacman = Pacman(1, 1)

# Define Collectible Dots
dots = [(x, y) for y in range(1, len(maze) - 1) for x in range(1, len(maze[y]) - 1) if maze[y][x] == 0]

def draw_dots(screen, dots):
    for dot in dots:
        pygame.draw.circle(screen, RED, (dot[0] * CELL_SIZE + CELL_SIZE // 2, dot[1] * CELL_SIZE + CELL_SIZE // 2 + 60), 5)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Control Pacman with Arrow Keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if maze[pacman.y - 1][pacman.x] != 1:
                    pacman.direction = UP
            elif event.key == pygame.K_DOWN:
                if maze[pacman.y + 1][pacman.x] != 1:
                    pacman.direction = DOWN
            elif event.key == pygame.K_LEFT:
                if maze[pacman.y][pacman.x - 1] != 1:
                    pacman.direction = LEFT
            elif event.key == pygame.K_RIGHT:
                if maze[pacman.y][pacman.x + 1] != 1:
                    pacman.direction = RIGHT

    # Update Pacman
    if pacman.move(maze):
        # Check for dot collection
        if (pacman.x, pacman.y) in dots:
            dots.remove((pacman.x, pacman.y))
            score += 69

    # Draw Everything
    screen.fill(BLACK)

    # Draw Maze
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE + 60, CELL_SIZE, CELL_SIZE))

    # Draw Pacman
    pacman.draw(screen)

    # Draw Dots
    draw_dots(screen, dots)

    # Draw Title
    title_surface = font.render("Pac-Man", True, WHITE)
    screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 10))

    # Draw Score
    score_surface = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, (10, 10))

    # Update the Display
    pygame.display.flip()

    # Cap the Frame Rate
    clock.tick(FPS)
