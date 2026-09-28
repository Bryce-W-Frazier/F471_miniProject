import pygame

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


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ### Game Loop Functions ###
    def show_score():
        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (10, 10))

    ### Screens ###
    def win_screen(): # TODO in Vaildate
        screen.fill("green")
        
        score_text = font.render(f" You win!, Score: {score}", True, "white")
        score_rect = score_text.get_rect(center=screen_center)
        screen.blit(score_text, score_rect)

    def lose_screen():
        # TODO in Specify
        print('dummy')

    def game_screen():
        screen.fill("green")
        pygame.draw.circle(screen, "yellow", ((620,360)), 100) 
        show_score()

    game_screen()

    pygame.display.flip()
    clock.tick(60) #Sets the framerate

pygame.quit()
