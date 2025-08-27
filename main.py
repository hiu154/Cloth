import pygame
import sys
import numpy as np
import config
from cloth import Cloth

pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Cloth Simulation - Tearable Fabric")
clock = pygame.time.Clock()

cloth = Cloth(30, 20, config.POINT_SPACING)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    mouse_pressed = pygame.mouse.get_pressed()[0]
    mouse_pos = np.array(pygame.mouse.get_pos(), dtype=float)
    if mouse_pressed:
        cloth.cut(mouse_pos)

    cloth.update()

    screen.fill((30, 30, 30))
    # vẽ các đường nối
    for stick in cloth.sticks:
        if not stick.broken:
            pygame.draw.line(screen, (200, 200, 200),
                             stick.p1.pos, stick.p2.pos, 1)

    pygame.display.flip()
    clock.tick(60)
