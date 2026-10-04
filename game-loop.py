import pygame 
import random
from enum import Enum


# Tracks CUrrent State of Game
class State(Enum):
    GAME_MENU = "Main Menu"
    GAME      = "Game Play"
    WIN_SCREEN = "Game was won"
    LOSE_SCREEN = "Game was Lost"
    HIGHSCORE = "Display Highscores"
    GAME_QUIT = "Close Game"



state = State.WIN_SCREEN

# Basic setup information
resolution = (1280, 720)
screen_center = (resolution[0]//2, resolution[1]//2)

pygame.init()
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("CS471-Snake")
clock = pygame.time.Clock()
running = True 

# Init Scoreboard
score = 0
font = pygame.font.Font(None, 36)

# Snake Setup
CELL = 20          # size of one grid square in pixels
MOVE_EVERY = 6     # snake moves once every N frames (lower = faster)
 
def reset_game():
    global score, snake_position, snake_body, direction, change_to, fruit_position, frame_count
    score = 0
    snake_position = [320, 360]
    snake_body = [[320, 360], [300, 360], [280, 360], [260, 360]]
    direction = 'RIGHT'
    change_to = 'RIGHT'
    fruit_position = new_fruit()
    frame_count = 0

def new_fruit():
     return [random.randrange(0, resolution[0] // CELL) * CELL, random.randrange(0, resolution[1] // CELL) * CELL]
 
reset_game()



### UI Functions ###
def show_score():
    score_text = font.render(f"Score: {score}", True, "white")
    screen.blit(score_text, (10, 10))

def nav_button(text, rect, events):
    mpos = pygame.mouse.get_pos()
    left_click = False

    pygame.draw.rect(screen, "black", rect, border_radius=8)
    pygame.draw.rect(screen, "white", rect, width=2, border_radius=8)

    button_text = font.render(text, True, "gray")
    text_rect = button_text.get_rect(center=rect.center)  

    if rect.collidepoint(mpos) and pygame.mouse.get_pressed()[0]:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
    elif rect.collidepoint(mpos):
        button_text = font.render(text, True, "white")

    screen.blit(button_text, text_rect)
    return False



### Screens ###
def win_screen(events):
    mpos = pygame.mouse.get_pos()
    message = f" You win!, Score: {score}"
    screen.fill("green")

    score_text = font.render(message, True, "white")
    score_rect = score_text.get_rect(center=screen_center)
    screen.blit(score_text, score_rect)

    buttons = {
            "Menu": State.GAME_MENU,
            "Restart": State.GAME,
            }

    for i, (text, next_state) in enumerate(buttons.items()):
        button_rect = pygame.Rect(
                    screen_center[0] - 150,
                    screen_center[1] + (80 * (i + 1)),
                    300,
                    60
                )

        if nav_button(text, button_rect, events):
            return next_state

    return State.WIN_SCREEN

def lose_screen(events):
    # TODO in Specify
    screen.fill("blue")
    print('Dummy lose Screen')
    return State.GAME_MENU

def game_screen(events):
    global direction, change_to, frame_count
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
 
    # don't allow the snake to reverse into itself
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # only move on each MOVE_EVERY frames so the snake isn't too fast
    frame_count += 1
    if frame_count % MOVE_EVERY == 0:
        if direction == 'UP':
            snake_position[1] -= CELL
        if direction == 'DOWN':
            snake_position[1] += CELL
        if direction == 'LEFT':
            snake_position[0] -= CELL
        if direction == 'RIGHT':
            snake_position[0] += CELL

        snake_body.insert(0, list(snake_position))
        snake_body.pop()

# draw
    screen.fill("black")
    for pos in snake_body:
        pygame.draw.rect(screen, "green", pygame.Rect(pos[0], pos[1], CELL, CELL))
    pygame.draw.rect(screen, "white", pygame.Rect(fruit_position[0], fruit_position[1], CELL, CELL))
    show_score()
    return State.GAME

def highscore_screen(events):
    screen.fill("green")
    show_score()
    print("Dummy Highscore Screen")
    return State.GAME_MENU

def game_menu(events):

    mpos = pygame.mouse.get_pos()
    screen.fill("white")
    buttons = {
            "Play": State.GAME,
            "Highscore": State.HIGHSCORE,
            "Quit": State.GAME_QUIT,

            }

    for i, (text, next_state) in enumerate(buttons.items()):

        button_rect = pygame.Rect(
                screen_center[0]-150,
                screen_center[1]+(80 * (i+1)),
                300,
                80,
        )
        if nav_button(text, button_rect, events):
            return next_state 
    return State.GAME_MENU

while running:

    leftClick = False
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
   
    match state: 
        case State.GAME_MENU:
            state = game_menu(events)
        case State.GAME:
            state = game_screen(events)
        case State.GAME_QUIT:
            running = False
        case State.LOSE_SCREEN:
            state = lose_screen(events)
        case State.HIGHSCORE:
            state = highscore_screen(events)
        case State.WIN_SCREEN:
            state = win_screen(events)

    pygame.display.flip()
    clock.tick(60) #Sets the framerate

pygame.quit()
