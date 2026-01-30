#!/usr/bin/env python3
"""
Snake Game - A classic arcade game implementation
Controls:
- Arrow keys or WASD to move
- ESC to quit
"""

try:
    import pygame
    import random
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("pygame not installed. Install with: pip install pygame")
    print("Falling back to text-based version...")
    import random

import sys
import time

# Game constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class SnakeGame:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        """Reset the game state"""
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.food = self.place_food()
        self.score = 0
        self.game_over = False
        
    def place_food(self):
        """Place food at a random location not occupied by the snake"""
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), 
                   random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food
                
    def update(self):
        """Update game state"""
        if self.game_over:
            return
            
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        # Check for collisions with walls
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over = True
            return
            
        # Check for collisions with self
        if new_head in self.snake:
            self.game_over = True
            return
            
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            self.score += 1
            self.food = self.place_food()
        else:
            self.snake.pop()
            
    def change_direction(self, new_direction):
        """Change snake direction, preventing 180-degree turns"""
        # Prevent moving in opposite direction
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction


def run_pygame_version():
    """Run the graphical pygame version"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    game = SnakeGame()
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_UP, pygame.K_w):
                    game.change_direction(UP)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    game.change_direction(DOWN)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    game.change_direction(LEFT)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    game.change_direction(RIGHT)
                elif event.key == pygame.K_SPACE and game.game_over:
                    game.reset_game()
        
        # Update game
        if not game.game_over:
            game.update()
        
        # Draw everything
        screen.fill(BLACK)
        
        # Draw snake
        for segment in game.snake:
            rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE,
                             GRID_SIZE - 1, GRID_SIZE - 1)
            pygame.draw.rect(screen, GREEN, rect)
        
        # Draw food
        food_rect = pygame.Rect(game.food[0] * GRID_SIZE, game.food[1] * GRID_SIZE,
                               GRID_SIZE - 1, GRID_SIZE - 1)
        pygame.draw.rect(screen, RED, food_rect)
        
        # Draw score
        score_text = font.render(f"Score: {game.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if game.game_over:
            game_over_text = font.render("Game Over! Press SPACE to restart", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
        clock.tick(10)  # 10 FPS
    
    pygame.quit()


def run_text_version():
    """Run a simple text-based version for systems without pygame"""
    print("\nText-based Snake Game")
    print("This is a simplified version. Install pygame for the full experience!")
    print("Install pygame with: pip install pygame\n")
    
    game = SnakeGame()
    
    print("Controls: w=up, s=down, a=left, d=right, q=quit")
    print("Starting game...\n")
    
    try:
        import msvcrt  # Windows
        def get_key():
            if msvcrt.kbhit():
                return msvcrt.getch().decode('utf-8').lower()
            return None
    except ImportError:
        # Unix-like systems
        import tty
        import termios
        import select
        
        def get_key():
            if select.select([sys.stdin], [], [], 0)[0]:
                old_settings = termios.tcgetattr(sys.stdin)
                try:
                    tty.setraw(sys.stdin.fileno())
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                return ch.lower()
            return None
    
    while True:
        # Handle input
        key = get_key()
        if key == 'q':
            break
        elif key == 'w':
            game.change_direction(UP)
        elif key == 's':
            game.change_direction(DOWN)
        elif key == 'a':
            game.change_direction(LEFT)
        elif key == 'd':
            game.change_direction(RIGHT)
        elif key == ' ' and game.game_over:
            game.reset_game()
        
        # Update game
        if not game.game_over:
            game.update()
        
        # Clear screen and draw
        print("\033[2J\033[H")  # Clear screen
        print(f"Score: {game.score}")
        print("─" * (GRID_WIDTH + 2))
        
        for y in range(GRID_HEIGHT):
            row = "│"
            for x in range(GRID_WIDTH):
                if (x, y) in game.snake:
                    if (x, y) == game.snake[0]:
                        row += "O"  # Head
                    else:
                        row += "o"  # Body
                elif (x, y) == game.food:
                    row += "*"
                else:
                    row += " "
            row += "│"
            print(row)
        
        print("─" * (GRID_WIDTH + 2))
        
        if game.game_over:
            print("Game Over! Press SPACE to restart or Q to quit")
        
        time.sleep(0.1)  # Control game speed
    
    print("\nThanks for playing!")


if __name__ == "__main__":
    if PYGAME_AVAILABLE:
        run_pygame_version()
    else:
        run_text_version()
