import pygame

display = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    display.fill((255, 255, 255))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
