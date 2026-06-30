import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            print("resize", event.size)
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

    screen.fill((30, 30, 30))
    pygame.display.flip()

pygame.quit()