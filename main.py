import asyncio
import pygame
import time
import random

snake_speed = 15

# Window size (Adjusted to accommodate touch buttons at the bottom)
window_x = 720
window_y = 600  # Increased from 480 to 600 to add control pad space
game_area_y = 480  # The original boundary for the snake game

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
gray = pygame.Color(60, 60, 60)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('My Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position 
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]
            
# fruit position 
fruit_position = [random.randrange(1, (window_x//10)) * 10,
                  random.randrange(1, (game_area_y//10)) * 10]
fruit_spawn = True

# setting default snake direction 
direction = 'RIGHT'
change_to = direction

# initial score
score = 0

# Define Touch Screen Button Rectangles (X, Y, Width, Height)
btn_w, btn_h = 70, 50
up_btn = pygame.Rect(window_x // 2 - btn_w // 2, game_area_y + 10, btn_w, btn_h)
down_btn = pygame.Rect(window_x // 2 - btn_w // 2, game_area_y + 70, btn_w, btn_h)
left_btn = pygame.Rect(window_x // 2 - btn_w * 1.5 - 10, game_area_y + 40, btn_w, btn_h)
right_btn = pygame.Rect(window_x // 2 + btn_w * 0.5 + 10, game_area_y + 40, btn_w, btn_h)

# displaying Score function
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

# Simple, seamless reset feature that completely eliminates the glitchy loop
def reset_game():
    global snake_position, snake_body, fruit_position, fruit_spawn, direction, change_to, score
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (game_area_y // 10)) * 10]
    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

# Async Main Function wrapper for web/mobile browsers
async def main():
    global direction, change_to, snake_position, snake_body, fruit_position, fruit_spawn, score

    while True:
        # handling key events and touch events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            # Keyboard handling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
            
            # Mobile touch handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if up_btn.collidepoint(mouse_pos):
                    change_to = 'UP'
                elif down_btn.collidepoint(mouse_pos):
                    change_to = 'DOWN'
                elif left_btn.collidepoint(mouse_pos):
                    change_to = 'LEFT'
                elif right_btn.collidepoint(mouse_pos):
                    change_to = 'RIGHT'

        # Ensure snake doesn't move immediately backwards into itself
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        # Snake body growing mechanism 
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()
            
        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                              random.randrange(1, (game_area_y//10)) * 10]
            
        fruit_spawn = True
        game_window.fill(black)
        
        # Draw game boundaries divider line
        pygame.draw.line(game_window, gray, (0, game_area_y), (window_x, game_area_y), 2)
        
        # Draw mobile UI D-pad buttons
        pygame.draw.rect(game_window, gray, up_btn, border_radius=5)
        pygame.draw.rect(game_window, gray, down_btn, border_radius=5)
        pygame.draw.rect(game_window, gray, left_btn, border_radius=5)
        pygame.draw.rect(game_window, gray, right_btn, border_radius=5)
        
        # Draw simple text indicator arrows on the buttons
        btn_font = pygame.font.SysFont('Arial', 24, bold=True)
        game_window.blit(btn_font.render('^', True, white), (up_btn.x + 28, up_btn.y + 8))
        game_window.blit(btn_font.render('v', True, white), (down_btn.x + 28, down_btn.y + 12))
        game_window.blit(btn_font.render('<', True, white), (left_btn.x + 26, left_btn.y + 12))
        game_window.blit(btn_font.render('>', True, white), (right_btn.x + 26, right_btn.y + 12))
        
        # Drawing game components
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
            
        pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

        # Instant Restart Conditions (Removes flickering entirely)
        if snake_position[0] < 0 or snake_position[0] > window_x-10:
            reset_game()
        if snake_position[1] < 0 or snake_position[1] > game_area_y-10:
            reset_game()
        
        # Touching the snake body causes an instant reset
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                reset_game()
        
        # displaying score continuously
        show_score(1, white, 'times new roman', 20)
        
        # Refresh game screen
        pygame.display.update()

        # Frame Per Second /Refresh Rate
        fps.tick(snake_speed)
        
        # CRITICAL FOR WEB: yields execution to the web browser to prevent tab freezing
        await asyncio.sleep(0)

# Run the game wrapper
asyncio.run(main())
