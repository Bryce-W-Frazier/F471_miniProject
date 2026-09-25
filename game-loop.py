import pygame

#Basic setup information
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("CS471-Snake")
pos = (620, 360)
clock = pygame.time.Clock()
running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                print("W was pressed")
            

    screen.fill("green")
    pygame.draw.circle(screen, "yellow", ((620,360)), 100, draw_top_right = False) 
    pygame.display.flip()

    clock.tick(60) #Sets the framerate

pygame.quit()
