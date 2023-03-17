import random
import pygame
from pygame.locals import *
import sys

class cell:
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.data = data

class simulation:
    def __init__(self, raw_score, cells, location):
        self.raw_score = raw_score
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

fallow_actions = 75 # percentage from 100
actions = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]
simulations_per_generation = 10

last_best = -sys.maxsize
last_actions = []

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
        generation_data[index].raw_score -= 1
        target_x = grid_size - 1
    elif target_x < 0:
        generation_data[index].raw_score -= 1
        target_x = 0

    target_y = generation_data[index].cells[location].y + y
    if target_y >= grid_size:
        generation_data[index].raw_score -= 1
        target_y = grid_size - 1
    elif target_y < 0:
        generation_data[index].raw_score -= 1
        target_y = 0

    target_index = location
    for i in range(len(generation_data[index].cells)):
        if (generation_data[index].cells[i].x == target_x and generation_data[index].cells[i].y == target_y):
            target_index = i
            break

    if generation_data[index].cells[target_index].data == "point":
        generation_data[index].raw_score += 50
        generation_data[index].ended = True
    elif generation_data[index].cells[target_index].data == "death":
        generation_data[index].raw_score = -sys.maxsize
        generation_data[index].ended = True

    generation_data[index].cells[location].data = "null"
    if (generation_data[index].cells[target_index].data != "death" and generation_data[index].cells[target_index].data != "point"):
        generation_data[index].cells[target_index].data = "player"
    generation_data[index].location = target_index
    generation_data[index].actions.append([target_x, target_y])

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

    best_index = -1
    best_score = -sys.maxsize
    for i in range(len(generation_data)):
        score = (generation_data[i].raw_score - len(generation_data[i].actions))
        if score > best_score:
            best_score = score
            best_index = i

    for i in range(len(generation_data[0].cells)):
        x = generation_data[0].cells[i].x
        y = generation_data[0].cells[i].y

        color = (30, 30, 30)
        if i == point_cell:
            color = (235, 210, 70)
        elif i == death_cell:
            color = (255, 70, 70)

        pygame.draw.rect(screen, color, pygame.Rect(30 + ((cell_size + cell_margin) * x), 30 + ((cell_size + cell_margin) * y), cell_size, cell_size))

        cell_text = font.render("{x},{y} (id:{id})".format(x = x, y = y, id = i), False, (255, 255, 255))
        screen.blit(cell_text, (35 + ((cell_size + cell_margin) * x), 32 + ((cell_size + cell_margin) * y)))
            
        cell_data_text = font.render("data:{data}".format(data = generation_data[0].cells[i].data), False, (255, 255, 255))
        screen.blit(cell_data_text, (35 + ((cell_size + cell_margin) * x), 55 + ((cell_size + cell_margin) * y)))

    score_text = font.render("best: (index: {bin}, score: {bsc}, location: {loc})".format(bin = best_index, bsc = best_score, loc = generation_data[best_index].location), False, (255, 255, 255))
    screen.blit(score_text, (50 + ((cell_size + cell_margin) * (x + 1)), 30))
    generaion_text = font.render("generation: {gen}".format(gen = generation), False, (255, 255, 255))
    screen.blit(generaion_text, (50 + ((cell_size + cell_margin) * (x + 1)), 50))

    end_count = 0
    for gen in generation_data:
        if gen.ended:
            end_count += 1

    if end_count == len(generation_data): 
        if last_best < best_score:
            last_best = best_score
            last_actions = generation_data[best_index].actions
        print("best from gen {gen} was {ind} with {scr} points".format(gen = generation, ind = best_index, scr = best_score))
        start_generation()
        generation += 1

        pygame.time.delay(1000)
    else:
        for g in range(len(generation_data)):
            if generation_data[g].ended:
                continue

            x = generation_data[g].cells[generation_data[g].location].x
            y = generation_data[g].cells[generation_data[g].location].y

            pygame.draw.rect(screen, (70, 70, 255), pygame.Rect(30 + ((cell_size + cell_margin) * x), 30 + ((cell_size + cell_margin) * y), cell_size, cell_size))

            cell_text = font.render("{x},{y} (id:{id})".format(x = x, y = y, id = generation_data[g].location), False, (255, 255, 255))
            screen.blit(cell_text, (35 + ((cell_size + cell_margin) * x), 32 + ((cell_size + cell_margin) * y)))
            cell_data_text = font.render("data:{data}".format(data = generation_data[g].cells[i].data), False, (255, 255, 255))
            screen.blit(cell_data_text, (35 + ((cell_size + cell_margin) * x), 55 + ((cell_size + cell_margin) * y)))
            simulation_text = font.render("score:{sc}".format(sc = generation_data[g].raw_score), False, (255, 255, 255))
            screen.blit(simulation_text, (35 + ((cell_size + cell_margin) * x), 78 + ((cell_size + cell_margin) * y)))

            if random.randrange(0, 100) < fallow_actions and len(last_actions) > 0 and len(generation_data[g].actions) < len(last_actions):
                action = last_actions[len(generation_data[g].actions)]
            else:
                action = actions[random.randint(0, len(actions) - 1)]
            
            move(g, generation_data[g].location, action[0], action[1])

            if (generation_data[g].raw_score < -30):
                generation_data[g].raw_score = -sys.maxsize
                generation_data[g].ended = True

    # draw the best simulation
    x = generation_data[best_index].cells[generation_data[best_index].location].x
    y = generation_data[best_index].cells[generation_data[best_index].location].y

    pygame.draw.rect(screen, (70, 255, 70), pygame.Rect(30 + ((cell_size + cell_margin) * x), 30 + ((cell_size + cell_margin) * y), cell_size, cell_size))

    cell_text = font.render("{x},{y} (id:{id})".format(x = x, y = y, id = generation_data[best_index].location), False, (255, 255, 255))
    screen.blit(cell_text, (35 + ((cell_size + cell_margin) * x), 32 + ((cell_size + cell_margin) * y)))
    cell_data_text = font.render("data:{data}".format(data = generation_data[best_index].cells[i].data), False, (255, 255, 255))
    screen.blit(cell_data_text, (35 + ((cell_size + cell_margin) * x), 55 + ((cell_size + cell_margin) * y)))
    simulation_text = font.render("score:{sc}".format(sc = generation_data[best_index].raw_score), False, (255, 255, 255))
    screen.blit(simulation_text, (35 + ((cell_size + cell_margin) * x), 78 + ((cell_size + cell_margin) * y)))

    #pygame.time.delay(100)

    pygame.display.flip()
    clock.tick(60) # fps limit

pygame.quit()