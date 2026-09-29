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
mpos = pygame.mouse.get_pos

# Init Scoreboard
score = 0
font = pygame.font.Font(None, 36)



    ### Game Loop Functions ###
def show_score():
    score_text = font.render(f"Score: {score}", True, "white")
    screen.blit(score_text, (10, 10))



### Screens ###

def win_screen(): # TODO in Vaildate
    mpos = pygame.mouse.get_pos()
    message = f" You win!, Score: {score}, Click to return to menu."
    screen.fill("green")
    score_text = font.render(message, True, "white")
    score_rect = score_text.get_rect(center=screen_center)
    if score_rect.collidepoint(mpos):

        score_text = font.render(message, True, "red")
        if pygame.mouse.get_pressed()[0]:
            return State.GAME_MENU
    screen.blit(score_text, score_rect)
    return State.WIN_SCREEN

def lose_screen():
    # TODO in Specify
    screen.fill("blue")
    print('Dummy lose Screen')
    return State.GAME_MENU

def game_screen():
    screen.fill("black")
    show_score()
    print("Dummy Game Screen")
    return State.LOSE_SCREEN

def highscore_screen():
    screen.fill("green")
    show_score()
    print("Dummy Highscore Screen")
    return State.GAME_MENU

def game_menu():

    mpos = pygame.mouse.get_pos()
    play = font.render("Play", True, (0,0,0))
    highscore = font.render("Highscores", True, (0,0,0))
    gameQuit = font.render("Quit", True, (0,0,0))

    play_rect = play.get_rect(center=(620,540))
    highscore_rect = highscore.get_rect(center=(620, 570))
    gameQuit_rect = gameQuit.get_rect(center=(620,600))

    if play_rect.collidepoint(mpos):
        play = font.render("Play", True, (255,0,0))

        if pygame.mouse.get_pressed()[0]:
            print("Play pressed")
            return State.GAME

    if highscore_rect.collidepoint(mpos):
        highscore = font.render("Highscores", True, (255,0,0))

        if pygame.mouse.get_pressed()[0]:
            print("Highscore Pressed")
            return State.HIGHSCORE

    if gameQuit_rect.collidepoint(mpos):
        gameQuit = font.render("Quit", True, (255,0,0))

        if pygame.mouse.get_pressed()[0]:
            print("Quit Pressed")
            return State.GAME_QUIT

    screen.fill("white")
    screen.blit(play, play_rect)
    screen.blit(highscore, highscore_rect)
    screen.blit(gameQuit, gameQuit_rect)
    return State.GAME_MENU

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if state == State.GAME_MENU:
        state = game_menu()
    if state == State.GAME:
        state = game_screen()
    if state == State.GAME_QUIT:
        running = False
    if state == State.LOSE_SCREEN:
        state = lose_screen()
    if state == State.HIGHSCORE:
        state = highscore_screen()
    if state == State.WIN_SCREEN:
        state = win_screen()

    pygame.display.flip()
    clock.tick(60) #Sets the framerate

pygame.quit()
