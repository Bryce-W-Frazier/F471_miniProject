import pygame 
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
    screen.fill("black")
    show_score()
    print("Dummy Game Screen")
    return State.LOSE_SCREEN

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
