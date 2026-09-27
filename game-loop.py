import pygame

# Basic setup information
pygame.init()
screen = pygame.display.set_mode((1280, 720))
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
            

    screen.fill("green")
    pygame.draw.circle(screen, "yellow", ((620,360)), 100) 
    show_score()

    pygame.display.flip()
    clock.tick(60) #Sets the framerate

pygame.quit()
