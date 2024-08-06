# Dumb game by Franz
# License issued by your mom


import pygame
import sys
import random
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
RED = (130, 215, 192)
YELLOW_FUD = (242,242,34)
PINK = (255, 105, 180)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Ghost Class
class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.released = False

    def move(self, pacman, maze):
        if not self.released:
            # Release the ghost after a delay
            self.released = random.choice([True, False])
            return

        # Basic AI: Move towards Pac-Man
        if random.random() < 0.5:
            if pacman.x > self.x:
                self.direction = RIGHT
            elif pacman.x < self.x:
                self.direction = LEFT
            elif pacman.y > self.y:
                self.direction = DOWN
            elif pacman.y < self.y:
                self.direction = UP
        else:
            new_direction = random.choice([UP, DOWN, LEFT, RIGHT])
            self.direction = new_direction

        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]

        # Check if the ghost can move in the current direction
        if maze[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        center = (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2 + 60)
        pygame.draw.circle(screen, self.color, center, CELL_SIZE // 2 - 2)
# Pacman Class
class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = LEFT
        self.next_direction = None
        self.mouth_open = True
        self.angle = 0

    def move(self, maze):
        # Check if next_direction is valid
        if self.next_direction:
            new_x = self.x + self.next_direction[0]
            new_y = self.y + self.next_direction[1]
            if maze[new_y][new_x] != 1:
                self.direction = self.next_direction
                self.next_direction = None

        # Continue moving in the current direction
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
pygame.display.set_caption("Fud-Man")
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
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 13
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],  # 14
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 15
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],  # 16
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 17
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],  # 18
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],  # 19
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1],  # 20
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],  # 21
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1],  # 22
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

# Create Ghosts
ghosts = [
    Ghost(13, 10, RED),
    Ghost(14, 10, PINK),
    Ghost(13, 11, CYAN),
    Ghost(14, 11, ORANGE)
]
# Start Screen Function
def start_screen():
    screen.fill(BLACK)
    title_surface = font.render("Fud-Man", True, YELLOW_FUD)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT + title_surface.get_height()))
    screen.blit(title_surface, title_rect)
    pygame.display.flip()
    return title_rect

# Start Screen Animation
def animate_start_screen():
    title_rect = start_screen()
    while title_rect.top > 10:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
        title_rect.y -= 25  # Faster movement
        screen.fill(BLACK)
        screen.blit(font.render("Fud-Man", True, YELLOW_FUD), title_rect)
        pygame.display.flip()
        clock.tick(FPS)

# Gameplay Transition Animation
def animate_gameplay_transition():
    title_surface = font.render("Fud-Man", True, YELLOW_FUD)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 15))

    score_surface = font.render(f"Score: {score}", True, YELLOW_FUD)
    score_rect = score_surface.get_rect(left=-score_surface.get_width(), top=10)

    while score_rect.left < 10:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if score_rect.left < 10:
            score_rect.x += 5

        screen.fill(BLACK)
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                if maze[y][x] == 1:
                    pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE + 60, CELL_SIZE, CELL_SIZE))
        pacman.draw(screen)
        draw_dots(screen, dots)
        screen.blit(title_surface, title_rect)
        screen.blit(score_surface, score_rect)
        pygame.display.flip()
        clock.tick(FPS)

# Main Game Loop
def main_game_loop():
    global score
    paused = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Control Pacman with Arrow Keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    while paused:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                paused = False
                elif event.key == pygame.K_UP:
                    pacman.next_direction = UP
                elif event.key == pygame.K_DOWN:
                    pacman.next_direction = DOWN
                elif event.key == pygame.K_LEFT:
                    pacman.next_direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    pacman.next_direction = RIGHT

        if not paused:
            # Update Pacman
            if pacman.move(maze):
                # Check for dot collection
                if (pacman.x, pacman.y) in dots:
                    dots.remove((pacman.x, pacman.y))
                    score += 10

            # Update Ghosts
            for ghost in ghosts:
                ghost.move(pacman, maze)

                # Check for collision with Pacman
                if ghost.x == pacman.x and ghost.y == pacman.y:
                    # Game Over
                    screen.fill(BLACK)
                    game_over_surface = font.render("Game Over", True, RED)
                    screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, SCREEN_HEIGHT // 2))
                    pygame.display.flip()
                    pygame.time.delay(3000)
                    pygame.quit()
                    sys.exit()

            # Draw Everything
            screen.fill(BLACK)

            # Draw Maze
            for y in range(len(maze)):
                for x in range(len(maze[y])):
                    if maze[y][x] == 1:
                        pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE + 60, CELL_SIZE, CELL_SIZE))

            # Draw Pacman
            pacman.draw(screen)

            # Draw Ghosts
            for ghost in ghosts:
                ghost.draw(screen)

            # Draw Dots
            draw_dots(screen, dots)

            # Draw Score
            score_surface = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_surface, (10, 10))

            pygame.display.flip()
            clock.tick(FPS)

# Run the Game
animate_start_screen()
animate_gameplay_transition()
main_game_loop()
