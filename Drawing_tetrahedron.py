import pygame, random
import numpy as np
from math import *


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600

pygame.display.set_caption("3d projection dodecahedron")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 100
circle_pos = [WIDTH/2, HEIGHT/2]
angle = 0

coordinates = [
    [  1,  1,  1],
    [  1, -1, -1],
    [ -1, -1,  1],
    [ -1,  1, -1]
]

points = []
for coordinate in coordinates:
    points.append(np.matrix(coordinate))

P = np.matrix([[1, 0, 0], [0, 1, 0]])

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

    x_angle = pi/4
    y_angle = 5*pi/12
    z_angle = angle

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(x_angle), -sin(x_angle)],
        [0, sin(x_angle),  cos(x_angle)]
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
        rotated2d = np.dot(rotation_z, point.reshape((3,1)))
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)
        
        projected2d = np.dot(P, rotated2d)
        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, RED, (x,y), 0)
        i+=1

    for i in range(4):
        for j in range(4):
            pygame.draw.line(screen, BLACK, projected_points[i], projected_points[j])
    
    
    pygame.display.update()






