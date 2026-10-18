import pygame 
import random
from enum import Enum

#Checks if we are called by doctest and if we are gives the SDL a dummy screen to draw to
import os
import sys

if "doctest" in sys.modules:
    os.environ["SDL_VIDEODRIVER"] = "dummy"


# Tracks CUrrent State of Game
class State(Enum):
    GAME_MENU = "Main Menu"
    GAME      = "Game Play"
    WIN_SCREEN = "Game was won"
    LOSE_SCREEN = "Game was Lost"
    HIGHSCORE = "Display Highscores"
    GAME_QUIT = "Close Game"


# Basic setup information
HIGHSCORE_FILE = "snake_highscore.txt"
resolution = (1280, 720)
screen_center = (resolution[0]//2, resolution[1]//2)

pygame.init()
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("CS471-Snake")
clock = pygame.time.Clock()

# Init Scoreboard
SCORE_INCERMENT = 10
score = 0
highscore = 0
try:    
    with open(HIGHSCORE_FILE, "r") as file:        
        highscore = int(file.read().strip())
except FileNotFoundError:      
    with open(HIGHSCORE_FILE, "w") as file:        
        file.write("0")
        
font = pygame.font.Font(None, 36)



# Snake Setup
CELL = 20          # size of one grid square in pixels
MOVE_EVERY = 6     # snake moves once every N frames (lower = faster)
MAX_SCORE = ((resolution[0]*resolution[1])/(CELL*CELL))/SCORE_INCERMENT
 
def reset_game():
    """
    Reset all games variables to have consistant game starts.
    
    >>> import game_loop as game
    >>> game.score = "Dummy"
    >>> game.snake_position = "Dummy"
    >>> game.snake_body = "Dummy"
    >>> game.direction = "Dummy"
    >>> game.change_to = "Dummy"
    >>> game.frame_count = "Dummy"
    
    >>> game.reset_game()
    
    >>> game.score
    0
    >>> game.snake_position
    [320, 360]
    >>> game.snake_body
    [[320, 360], [300, 360], [280, 360], [260, 360]]
    >>> game.direction
    'RIGHT'
    >>> game.change_to
    'RIGHT'
    >>> game.frame_count
    0
    """

    global score, snake_position, snake_body, direction, change_to, fruit_position, frame_count
    score = 0
    snake_position = [320, 360]
    snake_body = [[320, 360], [300, 360], [280, 360], [260, 360]]
    direction = 'RIGHT'
    change_to = 'RIGHT'
    fruit_position = new_fruit()
    frame_count = 0

def new_fruit():
    """
    Finds a spot for afruit on the game board, without colliding with the snake. 
    Returns [x, y]
    
    >>> import game_loop as game
    >>> for _i in range(resolution[0]*resolution[1]):
    ...     pos = new_fruit()
    ...     assert len(pos) == 2

    ...     for j in range(2):
    ...         assert pos[j] >= 0 + CELL
    
    ...         assert pos[j] <= game.resolution[j] - CELL
    
    ...     for j in snake_body:
    ...         assert pos != j
    """
    while True:
        pos = [random.randrange(0, resolution[0] // CELL) * CELL, random.randrange(0, resolution[1] // CELL) * CELL]
        if pos not in snake_body:
            return pos
        
def update_highscore():
    """
    Writes the new high score to file. Current highscore must be correct.
    No return.
    
    >>> import os
    >>> import game_loop as game
    
    >>> game.highscore = 1
    >>> game.HIGHSCORE_FILE = "test.temp"
    >>> open(game.HIGHSCORE_FILE, "w").close()
    >>> game.update_highscore()
    >>> with open(game.HIGHSCORE_FILE) as f:
    ...     contents = f.read()
    >>> int(contents) == game.highscore
    True
    >>> os.remove(game.HIGHSCORE_FILE)
    """
    with open(HIGHSCORE_FILE, "w") as file:
        file.write(str(highscore))
 


reset_game()
### UI Functions ###
def show_score():
    """
    Shows the score in the top left corner during the game. No return.
    
    >>> show_score()
    """
    
    score_text = font.render(f"Score: {score}", True, "white")
    screen.blit(score_text, (10, 10))

def nav_button(text, rect, events):
    """
    Renders and watches navigation buttons. Takes text as the message, rect as
    the area of placement, and events to watch. Returns True when mouse hovers
    over button, False otherwise.
    
    >>> nav_button("test", pygame.Rect(0,0,0,0), pygame.event.get())
    False
    """
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

def end_screen(events, message, state):
    """
    Workhorse for any end of game screen. Takes events for it's event handler,
    message to display to the player, and it's current state.
    
    >>> import game_loop as game
    >>> end_screen(pygame.event.get(), "Test",game.State.LOSE_SCREEN)
    <State.LOSE_SCREEN: 'Game was Lost'>
    """
    
    update_highscore()
    mpos = pygame.mouse.get_pos()
    screen.fill("black")

    # Display Results
    lines = [
        message,
        f"Score: {score}",
        f"Highscore: {highscore}",
    ]
   
    line_height = font.get_linesize()
    start_y = screen_center[1] - (len(lines) * line_height) // 2
    for i, text in enumerate(lines):
        line = font.render(text, True, "white")
        rect = line.get_rect(center=(screen_center[0], start_y + i * line_height))
        screen.blit(line, rect)

    # Nav Menu
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
            reset_game()
            return next_state

    return state
    
def win_screen(events):

    """
    Testing Win screen doesn't change without user input
    >>> win_screen([]) == State.WIN_SCREEN
    True
    """
    return end_screen(events, 
        "You win", 
        State.WIN_SCREEN)
    

def lose_screen(events):
    """
    Testing Lose screen doesn't change without user input
    
    >>> lose_screen([]) == State.LOSE_SCREEN
    True
    """
    return end_screen(events, 
        "You Lost!", 
        State.LOSE_SCREEN)


def game_screen(events):
    """
    Testing Game screen doesn't change without user input
    
    >>> game_screen([]) == State.GAME
    True
    """
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
        global fruit_position, score, highscore
        if direction == 'UP':
            snake_position[1] -= CELL
        if direction == 'DOWN':
            snake_position[1] += CELL
        if direction == 'LEFT':
            snake_position[0] -= CELL
        if direction == 'RIGHT':
            snake_position[0] += CELL

        snake_body.insert(0, list(snake_position))
        if snake_position == fruit_position:
            score += SCORE_INCERMENT
            if score > highscore:
                highscore = score
            fruit_position = new_fruit()
        else:
            snake_body.pop()

        # wall collision
        if (snake_position[0] < 0 or snake_position[0] > resolution[0] - CELL or 
                snake_position[1] < 0 or snake_position[1] > resolution[1] - CELL):
            return State.LOSE_SCREEN

        # self collision
        if snake_position in snake_body[1:]:
            return State.LOSE_SCREEN
        
        # board filled
        if score == MAX_SCORE:
            return State.WIN_SCREEN

# draw
    screen.fill("black")
    for pos in snake_body:
        pygame.draw.rect(screen, "green", pygame.Rect(pos[0], pos[1], CELL, CELL))
    pygame.draw.rect(screen, "white", pygame.Rect(fruit_position[0], fruit_position[1], CELL, CELL))
    show_score()
    return State.GAME

def highscore_screen(events):
    """
    Testing Highscore screen doesn't change without user input
    
    >>> highscore_screen([]) == State.HIGHSCORE
    True
    """
    screen.fill("green")
    show_score()
    print("Dummy Highscore Screen")
    return State.GAME_MENU

def game_menu(events):

    """
    Testing Menu screen doesn't change without user input
    
    >>> game_menu([]) == State.GAME_MENU
    True
    """

    mpos = pygame.mouse.get_pos()
    screen.fill("black")
    
    title = font.render("Snake", True, "white")
    title_rect = title.get_rect(center=(screen_center[0], screen_center[1]))
    screen.blit(title, title_rect)
    
    buttons = {
            "Play": State.GAME,
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

def game_loop():
    """
    Handles the changing states until the user quits.
    """

    state = State.GAME_MENU
    running = True 
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

if __name__ == "__main__":
    game_loop()
