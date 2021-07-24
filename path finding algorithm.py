import pygame
from math import sqrt
from random import randint, choice
from time import sleep

pygame.init()
win_size = 600
win = pygame.display.set_mode((win_size, win_size))
pygame.display.set_caption('path finding algorithm')
row = 50
gap = win_size // row
stop = False
paint = False
start_end = []
start_path_finding = False
path_found = False
is_route_done = False
black_box = []


def draw_grid():
    win.fill((150, 150, 100))
    for i in range(0, win_size, gap):
        pygame.draw.line(win, (255, 255, 255), (0, i), (win_size, i))
        pygame.draw.line(win, (255, 255, 255), (i, 0), (i, win_size))


def redraw_board():
    draw_grid()
    for n in black_box:
        draw_rect(n, 1)
    for m in start_end:
        draw_rect(m, 2)


def notify():
    font = pygame.font.SysFont('comicsansms', 27)
    message = font.render('press SPACE BAR to start', True, (255, 0, 0))
    win.blit(message, (140, 225))


def draw_rect(position, color):
    if color == 1:
        pygame.draw.rect(win, (0, 0, 0), ((position[0] * gap) + 1, (position[1] * gap) + 1, gap - 1, gap - 1))
    elif color == 2:
        pygame.draw.rect(win, (255, 0, 0), ((position[0] * gap) + 1, (position[1] * gap) + 1, gap - 1, gap - 1))
    elif color == 3:
        pygame.draw.rect(win, (150, 255, 150),
                         ((position[0] * gap) + 1, (position[1] * gap) + 1, gap - 1, gap - 1))
    elif color == 4:
        pygame.draw.rect(win, (255, 255, 0), (position[0] * gap, position[1] * gap, gap - 1, gap - 1))
    else:
        pygame.draw.rect(win, (150, 150, 100), ((position[0] * gap) + 1, (position[1] * gap) + 1, gap - 1, gap - 1))
    pygame.display.update()


def make_obstacles():
    global black_box
    array = ['left', 'right', 'up', 'down']
    for x in range(row * 3):
        current_node = [randint(0, row), randint(0, row)]
        if current_node in black_box:
            continue
        direction_to_draw = choice(array)
        for y in range(randint(1, 3)):
            direction = {'right': [current_node[0] + 1, current_node[1]],
                         'left': [current_node[0] - 1, current_node[1]],
                         'up': [current_node[0], current_node[1] - 1],
                         'down': [current_node[0], current_node[1] + 1]}
            next_node = direction[direction_to_draw]
            if next_node in black_box:
                continue
            black_box.append(next_node)
            draw_rect(next_node, 1)
            if 0 <= next_node[0] < row and 0 <= next_node[1] < row:
                current_node = next_node
            else:
                break
            pygame.display.update()


def distance(x, y):
    return sqrt(((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2))


class Node(object):
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position
        self.neighbour = []
        self.f = 0
        self.g = 0
        self.h = 0

    def add_neighbour(self):
        if self.position[0] < row - 1:
            # appending right cell
            self.neighbour.append(Node(self, [self.position[0] + 1, self.position[1]]))
        if self.position[1] < row - 1:
            # appending upper cell
            self.neighbour.append(Node(self, [self.position[0], self.position[1] + 1]))
        if self.position[0] > 0:
            # appending left cell
            self.neighbour.append(Node(self, [self.position[0] - 1, self.position[1]]))
        if self.position[1] > 0:
            # appending bottom cell
            self.neighbour.append(Node(self, [self.position[0], self.position[1] - 1]))

    def __eq__(self, other):
        return self.position == other.position


def path_finder():
    global is_route_done
    start = Node(None, start_end[0])
    end = Node(None, start_end[1])
    current_node = start
    open_list = [start]
    close_list = []
    while len(open_list) > 0:
        index = 0
        for i in range(len(open_list)):
            if open_list[i].f < open_list[index].f:
                index = i

        if current_node == end:
            path = []
            temp = current_node
            while temp.parent is not None:
                path.append(temp.position)
                temp = temp.parent
            is_route_done = True
            return path

        current_node = open_list[index]
        open_list.remove(current_node)
        close_list.append(current_node)
        current_node.add_neighbour()

        new_path = False

        for neighbour in current_node.neighbour:
            if (neighbour in close_list) or (neighbour.position in black_box):
                continue
            temp_number = current_node.g + 1

            if neighbour in open_list:
                if temp_number < neighbour.g:
                    neighbour.g = temp_number
                    new_path = True
            else:
                neighbour.g = temp_number
                open_list.append(neighbour)
                new_path = True

            if new_path:
                neighbour.h = distance(neighbour.position, end.position)
                neighbour.f = neighbour.g + neighbour.h
                neighbour.parent = current_node

            if neighbour == end or neighbour == start:
                pass
            else:
                draw_rect(neighbour.position, 3)


def find_and_draw_path():
    shortest_route = path_finder()
    if shortest_route is not None:
        for m in shortest_route[1:]:
            draw_rect(m, 4)


def play():
    global stop, paint
    draw_grid()
    make_obstacles()
    while not stop:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                stop = True
                pygame.quit()
                exit()

            # to set events for mouse to draw boxes
            mouse = [pos[0] // gap, pos[1] // gap]
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    paint = True
                elif event.button == 3:
                    if mouse in black_box:
                        draw_rect(mouse, 5)
                        black_box.remove(mouse)
                    if mouse in start_end:
                        draw_rect(mouse, 5)
                        start_end.remove(mouse)
                '''elif event.button == 2:
                        if len(start_end) < 2:
                            draw_rect(mouse, 2)
                            if mouse in black_box:
                                black_box.remove(mouse)
                            start_end.append(mouse)'''

            if event.type == pygame.MOUSEBUTTONUP:
                paint = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if is_route_done:
                        redraw_board()
                        find_and_draw_path()
                    else:
                        find_and_draw_path()
                elif event.key == pygame.K_i:
                    if len(start_end) < 2:
                        draw_rect(mouse, 2)
                        if mouse in black_box:
                            black_box.remove(mouse)
                        start_end.append(mouse)

        # to draw the black box on board
        if paint:
            draw_rect([pos[0] // gap, pos[1] // gap], 1)
            # to store the position of the boxes which are black
            black_box_coordinates = [pos[0] // gap, pos[1] // gap]
            if not (black_box_coordinates in black_box):
                black_box.append(black_box_coordinates)

        pygame.display.update()


notify()
play()
