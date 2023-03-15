import random
import pygame
from pygame.locals import *

class cell:
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.data = data

class simulation:
    def __init__(self, score, cells, location):
        self.score = score
        self.cells = cells
        self.location = location
        self.actions = []
        self.ended = False

start_cell = 12
point_cell = 0
death_cell = 1

grid_size = 5
cell_size = 100
cell_margin = 10

generation = 0
generation_data = []

actions = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]
simulations_per_generation = 10

def start_generation():
    global generation_data
    generation_data = []
    for i in range(simulations_per_generation):
        cells = []
        for y in range(grid_size):
            for x in range(grid_size):
                cells.append(cell(x, y, "null"))
        cells[point_cell].data = "point"
        cells[death_cell].data = "death"
        generation_data.append(simulation(0, cells, start_cell))

start_generation()

def move(index, location, x, y):
    global generation_data

    target_x = generation_data[index].cells[location].x + x
    if target_x >= grid_size:
        generation_data[index].score -= 1
        target_x = grid_size - 1
    elif target_x < 0:
        generation_data[index].score -= 1
        target_x = 0

    target_y = generation_data[index].cells[location].y + y
    if target_y >= grid_size:
        generation_data[index].score -= 1
        target_y = grid_size - 1
    elif target_y < 0:
        generation_data[index].score -= 1
        target_y = 0

    target_index = location
    for i in range(len(generation_data[index].cells)):
        if (generation_data[index].cells[i].x == target_x and generation_data[index].cells[i].y == target_y):
            target_index = i
            break

    if generation_data[index].cells[target_index].data == "point":
        generation_data[index].score += 1
        generation_data[index].ended = True
    elif generation_data[index].cells[target_index].data == "death":
        generation_data[index].score -= 10
        generation_data[index].ended = True

    generation_data[index].cells[location].data = "null"
    generation_data[index].cells[target_index].data = "player"
    generation_data[index].location = target_index

pygame.init()
pygame.display.set_caption('AI game shit thing')
Icon = pygame.image.load('icon.jpeg')
pygame.display.set_icon(Icon)
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

    if len(generation_data) == 0:
        break

    best_index = 0
    best_score = 0
    for i in range(len(generation_data)):
        if generation_data[i].score > best_score:
            best_score = generation_data[i].score
            best_index = i

    for i in range(len(generation_data[0].cells)):
        x = generation_data[0].cells[i].x
        y = generation_data[0].cells[i].y

        color = (30, 30, 30)
        if i == point_cell:
            color = (70, 255, 70)
        elif i == death_cell:
            color = (255, 70, 70)

        pygame.draw.rect(screen, color, pygame.Rect(30 + ((cell_size + cell_margin) * x), 30 + ((cell_size + cell_margin) * y), cell_size, cell_size))

        cell_text = font.render("{x},{y} (id:{id})".format(x = x, y = y, id = i), False, (255, 255, 255))
        screen.blit(cell_text, (35 + ((cell_size + cell_margin) * x), 32 + ((cell_size + cell_margin) * y)))
            
        cell_data_text = font.render("data:{data}".format(data = generation_data[0].cells[i].data), False, (255, 255, 255))
        screen.blit(cell_data_text, (35 + ((cell_size + cell_margin) * x), 55 + ((cell_size + cell_margin) * y)))

    score_text = font.render("best: (index: {bin}, score: {bsc})".format(bin = best_index, bsc = best_score), False, (255, 255, 255))
    screen.blit(score_text, (50 + ((cell_size + cell_margin) * (x + 1)), 30))
    generaion_text = font.render("generation: {gen}".format(gen = generation), False, (255, 255, 255))
    screen.blit(generaion_text, (50 + ((cell_size + cell_margin) * (x + 1)), 50))

    end_count = 0
    for gen in generation_data:
        if gen.ended:
            end_count += 1

    if end_count == len(generation_data):
        #start_generation()
        generation += 1
    else:
        for g in range(len(generation_data)):
            if generation_data[g].ended:
                break

            x = generation_data[g].cells[generation_data[g].location].x
            y = generation_data[g].cells[generation_data[g].location].y

            pygame.draw.rect(screen, (70, 70, 255), pygame.Rect(30 + ((cell_size + cell_margin) * x), 30 + ((cell_size + cell_margin) * y), cell_size, cell_size))

            cell_text = font.render("{x},{y} (id:{id})".format(x = x, y = y, id = i), False, (255, 255, 255))
            screen.blit(cell_text, (35 + ((cell_size + cell_margin) * x), 32 + ((cell_size + cell_margin) * y)))
            cell_data_text = font.render("data:{data}".format(data = generation_data[g].cells[i].data), False, (255, 255, 255))
            screen.blit(cell_data_text, (35 + ((cell_size + cell_margin) * x), 55 + ((cell_size + cell_margin) * y)))

            action = actions[random.randint(0, len(actions) - 1)]
            move(g, generation_data[g].location, action[0], action[1])

    pygame.time.delay(300)

    pygame.display.flip()
    clock.tick(60) # fps limit

pygame.quit()