import random
import pygame
from pygame.locals import *

class cell:
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.data = data

player = 12
cells = []
for y in range(5):
    for x in range(5):
        cells.append(cell(x, y, "null"))

cells[player].data = "player"

point_active = False

cell_size = 100
cell_margin = 10

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

pygame.font.init()
font = pygame.font.SysFont('arial', 18, bold=True)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("#101010")

    # render the screen
    for i in range(len(cells)):
        x = cells[i].x
        y = cells[i].y

        if not point_active:
            # randomize the point
            rand = random.randint(0, len(cells))
            while (cells[rand].data == "player" or cells[rand].data == "point" or cells[rand].data == "death"):
                rand += 1
                if rand >= len(cells):
                    rand = 0
        
            cells[rand].data = "point"

            # randomize the death cell
            rand = random.randint(0, len(cells))
            while (cells[rand].data == "player" or cells[rand].data == "point" or cells[rand].data == "death"):
                rand += 1
                if rand >= len(cells):
                    rand = 0
        
            cells[rand].data = "death"

            point_active = True

        # get color for cells
        color = (30, 30, 30)
        if cells[i].data == "player":
            color = (70, 70, 255)
        elif cells[i].data == "point":
            color = (70, 255, 70)
        elif cells[i].data == "death":
            color = (255, 70, 70)

        pygame.draw.rect(screen, color, pygame.Rect(30 + ((cell_size + cell_margin) * x), 30 + ((cell_size + cell_margin) * y), cell_size, cell_size))

        cell_text = font.render("{x},{y} (id:{id})".format(x = x, y = y, id = i), False, (255, 255, 255))
        screen.blit(cell_text, (35 + ((cell_size + cell_margin) * x), 32 + ((cell_size + cell_margin) * y)))
            
        cell_data_text = font.render("data:{data}".format(data = cells[i].data), False, (255, 255, 255))
        screen.blit(cell_data_text, (35 + ((cell_size + cell_margin) * x), 55 + ((cell_size + cell_margin) * y)))
    
    pygame.time.delay(1)

    pygame.display.flip()
    clock.tick(60) # fps limit

pygame.quit()
