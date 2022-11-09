import pygame
import numpy as np
from math import *

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 700

pygame.display.set_caption("3d projection surface")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 50
circle_pos = [WIDTH/2, HEIGHT/2+150]
angle = 0

f1 = lambda x, y: 1/2 * (x**2 + y**2)
f2 = lambda x, y: 1/3 * (x**3 - y**3)
f3 = lambda x, y: 1/2 * (x**2 - y**2)
f4 = lambda x, y: cos(x)+sin(y)
f5 = lambda x, y: (e**(x) + e**(-y))/4

# Domain range ------------------------------------------------------------- #
x_start, x_end, y_start, y_end = -3, 3, -3, 3

# How many points I wanna map in X direction and Y direction
x_density, y_density = 20, 20

points = []
for i in range(y_density):
    for j in range(x_density):
        x_range, y_range = (x_end-x_start), (y_end-y_start)
        dx, dy = x_range/(x_density-1), y_range/(y_density-1)
        x_coord, y_coord = (x_start + i*dx), (y_start + j*dy)
        
        point = [x_coord, y_coord, f5(x_coord, y_coord)]
        points.append(point)

#aggregated_points = [points[i:i + x_density] for i in range(0, len(points), x_density)]

P = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]])

projected_points = [[n, n] for n in range(len(points))]

def connect_points(i, j, points_set):
    pygame.draw.line(screen, BLACK, (points_set[i][0], points_set[i][1]), (points_set[j][0], points_set[j][1]))

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
    
    screen.fill(WHITE)

    x_angle = 3*pi/12
    y_angle = 0
    z_angle = angle
    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(x_angle), -sin(x_angle)],
        [0, sin(x_angle), cos(x_angle)]
    ])
    rotation_y = np.matrix([
        [cos(y_angle), 0, -sin(y_angle)],
        [0, 1, 0],
        [sin(y_angle), 0, cos(y_angle)]
    ])
    rotation_z = np.matrix([
        [cos(z_angle), -sin(z_angle), 0],
        [sin(z_angle), cos(z_angle), 0],
        [0, 0, 1]
    ])

    angle += pi/360

    i = 0
    for point in points:
        rotated2d = np.dot(rotation_z, np.array(point).reshape((3,1)))
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)
        
        projected2d = np.dot(P, rotated2d)
        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, RED, (x,y), 0)
        i+=1
    
    for i in range(0, x_density*y_density, x_density):
        for p in range(x_density-1):
            pygame.draw.line(screen, BLACK, projected_points[i+p], projected_points[i+p+1])
    
    for j in range(x_density):
        for p in range(y_density-1):
            pygame.draw.line(screen, BLACK, projected_points[p*x_density + j], projected_points[(p+1)*x_density + j])
    
    for k in range(y_density-1):
        for p in range(k*x_density, (k+1)*x_density-1):
            pygame.draw.line(screen, BLACK, projected_points[p+1], projected_points[x_density+p])
    
    
    pygame.display.update()