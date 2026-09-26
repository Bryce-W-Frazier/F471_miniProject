import pygame

#Basic setup information
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("CS471-Snake")
clock = pygame.time.Clock()
running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            

    screen.fill("green")
    pygame.draw.circle(screen, "yellow", ((620,360)), 100) 
    pygame.display.flip()

    clock.tick(60) #Sets the framerate

pygame.quit()
