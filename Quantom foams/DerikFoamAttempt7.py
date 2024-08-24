import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import noise as perlin_noise
from skimage import measure
import random

# Инициализация Pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Инициализация камеры
gluPerspective(25, (display[0]/display[1]), 0.1, 1000.0)
glTranslatef(-15, 0.0, -150.0)  # Переместить камеру вниз и назад
glRotatef(35, 1, 0, 0)  # Повернуть камеру на 35 градусов вокруг оси X

# Параметры шума Перлина
octaves = 4
persistence = 0.5
lacunarity = 2
scale = 10

# Создание 3D-массива шума Перлина
shape = (32, 32, 32)

# Нормализация шума в диапазон от 0 до 1
def normalize_noise(noise):
    return (noise - noise.min()) / (noise.max() - noise.min())

# Генерация шума Перлина для одного кадра
def generate_noise(base, offset):
    noise = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                noise[i][j][k] = perlin_noise.pnoise3((i + offset[0]) / scale,
                                                     (j + offset[1]) / scale,
                                                     (k + offset[2]) / scale,
                                                     octaves=octaves,
                                                     persistence=persistence,
                                                     lacunarity=lacunarity,
                                                     repeatx=shape[0],
                                                     repeaty=shape[1],
                                                     repeatz=shape[2],
                                                     base=int(base))
    return normalize_noise(noise)

# Оператор размазывания
def smear_operator(noise):
    smeared_noise = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                smeared_noise[i][j][k] = (noise[i][j][k] + noise[(i+1)%shape[0]][j][k] + noise[i][(j+1)%shape[1]][k] + noise[i][j][(k+1)%shape[2]]) / 4
    return smeared_noise

# Функция для обновления кадра
def update(offset):
    base = random.randint(0, 1000)  # Случайное значение base
    noise = generate_noise(base, offset)
    for i in range(50):  # 50 размазываний
        noise = smear_operator(noise)
    U = np.where(noise > 0.5, noise, noise.min())  # Устанавливаем значение в минимальное, если шум ниже 0.5
    U = normalize_noise(U)  # Нормализация массива U

    # Создание изосурфейса
    verts, faces, normals, values = measure.marching_cubes(U, level=0.5)

    # Отрисовка изосурфейса
    glColor4f(0.0, 1.0, 0.0, 0.5)  # Зеленый полупрозрачный цвет
    glEnable(GL_BLEND)  # Включить смешивание цветов
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Установить функцию смешивания
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex_index in face:
            vertex = verts[vertex_index]
            glVertex3fv(vertex)
    glEnd()
    glDisable(GL_BLEND)  # Выключить смешивание цветов

# Основной цикл
offset = [0, 0, 0]
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                offset[2] += 5
            if event.key == pygame.K_s:
                offset[2] -= 5
            if event.key == pygame.K_a:
                offset[0] -= 5
            if event.key == pygame.K_d:
                offset[0] += 5
            if event.key == pygame.K_q:
                offset[1] -= 5
            if event.key == pygame.K_e:
                offset[1] += 5

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    update(offset)
    pygame.display.flip()
    clock.tick(60)
