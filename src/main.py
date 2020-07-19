import pygame

pygame.init()
pygame.font.init()

from Grid import Grid


screen = pygame.display.set_mode((390, 390))
screen.fill((0, 0, 0))


sudoku = Grid(screen, lvl=1)

sudoku.draw()
sudoku.solve()

pygame.time.delay(3000)

pygame.quit()
