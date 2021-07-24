import pygame
from random import randint as r_int
from random import uniform as uni
from math import pi, sqrt, sin, cos
from datetime import datetime
from numpy import array, vstack

width, height = 900, 700
pygame.init()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Planet simulation')
clock = pygame.time.Clock()
planets = []
running = True
dt = 0.5


def generate_random_color():
    return r_int(0, 255), r_int(0, 255), r_int(0, 255)


def calculate_radius(start_time, end_time):
    return abs(end_time - start_time) * 2


class Planet(object):
    global planets, dt

    def __init__(self, x, y, color, mass, radius, density, is_star=False):
        self.mass = mass
        self.radius = radius
        self.density = density
        self.color = color
        self.position_vector = [x, y]
        self.gravity = -6.67
        self.velocity = [0, 0]
        self.theta = 0
        self.momentum = [0, 0]
        self.trail = array([self.position_vector])
        self.is_star = is_star

    def simulate(self):
        if not self.is_star:
            self.update_vector()
        self.draw()

    def draw(self):
        pygame.draw.circle(window, self.color, self.position_vector, self.radius)
        self.trail = vstack([self.trail, self.position_vector])
        for x in self.trail:
            pygame.draw.circle(window, self.color, x, 1)
        pygame.display.update()

    def update_vector(self):
        self.calculate_velocity()
        x = []
        force = [0, 0]
        x_sum = lambda array: [a for a, b in array]
        y_sum = lambda array: [b for a, b in array]
        for planet in planets:
            if self.position_vector == planet.ret_self_pos():
                continue
            x.append(self.calculate_force(planet))
        if x:
            force[0] = sum(x_sum(x))
            force[1] = sum(y_sum(x))

        velocity = self.calculate_velocity()

        # self.momentum[0] = self.momentum[0] + (force[0] * dt) * velocity
        # self.momentum[1] = self.momentum[1] + (force[1] * dt) * velocity

        self.velocity[0] = (force[0] * dt) * velocity
        self.velocity[1] = (force[1] * dt) * velocity

        self.position_vector = self.rotate_vector(self.position_vector)
        # self.position_vector[0] = self.position_vector[0] + self.momentum[0] / self.mass * dt
        # self.position_vector[1] = self.position_vector[1] + self.momentum[1] / self.mass * dt
        self.position_vector[0] = self.position_vector[0] + self.velocity[0] / self.mass * dt
        self.position_vector[1] = self.position_vector[1] + self.velocity[1] / self.mass * dt

    def calculate_force(self, planet):
        planet_pos = planet.ret_self_pos()
        r_vec = [self.position_vector[0] - planet_pos[0], self.position_vector[1] - planet_pos[1]]
        r_mag = sqrt(r_vec[0] ** 2 + r_vec[1] ** 2)
        r_hat = [r_vec[0] / r_mag, r_vec[1] / r_mag]
        force_mag = (self.gravity * self.mass * planet.ret_self_mass()) / (r_mag ** 2)
        force_vec = [force_mag * r_hat[0], force_mag * r_hat[1]]
        return force_vec

    def calculate_velocity(self):
        # sqrt(GM/r)
        mass = [1]
        dist = [1]
        for planet in planets:
            if (planet.ret_self_pos() != self.position_vector) and (self.mass > planet.ret_self_mass()):
                mass.append(planet.ret_self_mass())
                dist.append(self.calculate_distance(self.position_vector, planet.ret_self_pos()))
        return sqrt(abs((self.gravity * sum(mass)) / sum(dist))) * 0.1

    def calculate_distance(self, vector1, vector2):
        a = (vector2[0] - vector1[0]) ** 2
        b = (vector2[1] - vector1[1]) ** 2
        return sqrt(a + b)

    def rotate_vector(self, vector):
        x = (vector[0] * cos(pi / 2)) - (vector[1] * sin(pi / 2))
        y = (vector[0] * sin(pi / 2)) + (vector[1] * cos(pi / 2))
        return [x, y]

    def ret_self_pos(self):
        return self.position_vector

    def ret_self_mass(self):
        return self.mass

    def ret_self_radius(self):
        return self.radius


def initialize_planet(radius, color, pos):
    density = uni(0.1, 2.5)
    volume = (4 / 3) * pi * (radius ** 3)
    mass = density * volume
    return Planet(pos[0], pos[1], color, mass * 10, radius, density)


def play():
    global running

    calculate_start_time = False
    is_start_time_done = False
    calculate_end_time = False
    is_end_time_done = True
    start_time = end_time = None
    draw_planet = False

    while running:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
                return

            if keys[pygame.K_SPACE] and (not is_start_time_done):
                calculate_start_time = True

            if (not keys[pygame.K_SPACE]) and (not is_end_time_done):
                calculate_end_time = True

        if calculate_start_time:
            start_time = float(datetime.utcnow().strftime('%S.%f'))
            draw_planet = True
            calculate_start_time = False
            is_start_time_done = True
            is_end_time_done = False

        if calculate_end_time:
            end_time = float(datetime.utcnow().strftime('%S.%f'))
            draw_planet = False
            calculate_end_time = False
            is_end_time_done = True
            is_start_time_done = False
            planets.append(initialize_planet(calculate_radius(start_time, end_time), generate_random_color(), pos))

        if draw_planet:
            pygame.draw.circle(window, 'white', (pos[0], pos[1]),
                               calculate_radius(start_time, float(datetime.utcnow().strftime('%S.%f'))))

        for planet in planets:
            planet.simulate()
            planet.draw()
        window.fill('black')
        clock.tick(60)
        pygame.display.update()


p1 = initialize_planet(8, generate_random_color(), [width / 4, height / 2])
sun = initialize_planet(20, generate_random_color(), [width / 2, height / 2])
sun.is_star = True
# sun.mass = 10e1000
planets.append(p1)
planets.append(sun)
play()
