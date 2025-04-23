import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prantik_das.objects import Menu, Windows

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Drone simulation")

clock = pygame.time.Clock()
running = True

mouseClicked = False
dt = 0

SERVER_URL = "ws://localhost:8765"
BLACK = (0, 0, 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseClicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseClicked = False

    screen.fill(BLACK)
    menu = Menu(screen, SERVER_URL)
    windows = Windows(screen)

    for btn in menu.buttons:
        if btn[0].collidepoint(pygame.mouse.get_pos()) and mouseClicked:
            btn[1]()

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
