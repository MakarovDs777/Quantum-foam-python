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
def generate_noise(base, offset, scale):
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

# Чанки и их шум
chunks = {}  # Словарь для хранения шума каждого чанка

# Создание чанка и добавление его в словарь
def create_chunk(offset):
    base = random.randint(0, 1000)  # Случайный base для каждого чанка
    scale = random.uniform(1, 10)  # Случайный масштаб для каждого чанка
    noise = generate_noise(base, offset, scale)
    chunks[tuple(offset)] = noise

# Функция для обновления кадра
def update(offset):
    # Проверить, существует ли шум для текущего чанка
    if tuple(offset) not in chunks:
        create_chunk(offset)  # Создать чанк, если его нет

    noise = chunks[tuple(offset)]  # Получить шум для текущего чанка
    U = np.where(noise > 0.5, noise, noise.min())  # Установить значение в минимальное, если шум ниже 0.5
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

# Гиперкуб Хорэдема
def generate_hypercube(offset):
    # Создание 3D-массива случайных чисел
    random_array = np.random.rand(*shape)

    # Определение типа каждой ячейки гиперкуба
    cell_types = np.where(random_array < 0.5, 0, 1)  # 0 - портал, 1 - комната

    # Определение свойств каждой ячейки
    cell_properties = np.random.rand(*shape, 3)  # цвет, размер, форма

    # Создание вершин и граней гиперкуба
    verts = []
    faces = []
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                if cell_types[i][j][k] == 0:  # портал
                    verts.append([i, j, k])
                    faces.append([i, j, k])
                elif cell_types[i][j][k] == 1:  # комната
                    verts.append([i, j, k])
                    faces.append([i, j, k])

    # Отрисовка гиперкуба
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

def draw_text(position, text_string, color):
    font = pygame.font.SysFont("Arial", 20)
    text_surface = font.render(text_string, True, color, (0, 0, 0, 255))
    text_data = pygame.image.tostring(text_surface, 'RGBA', True)
    glRasterPos3d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

x_input = ""
y_input = ""
z_input = ""
active_field = "x"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                offset[2] += 1
            if event.key == pygame.K_s:
                offset[2] -= 1
            if event.key == pygame.K_a:
                offset[0] -= 1
            if event.key == pygame.K_d:
                offset[0] += 1
            if event.key == pygame.K_q:
                offset[1] -= 1
            if event.key == pygame.K_e:
                offset[1] += 1
            if event.key == pygame.K_RETURN:
                if x_input!= "" and y_input!= "" and z_input!= "":
                    offset = [int(x_input), int(y_input), int(z_input)]
                    x_input = ""
                    y_input = ""
                    z_input = ""
            if event.key == pygame.K_BACKSPACE:
                if active_field == "x" and x_input!= "":
                    x_input = x_input[:-1]
                elif active_field == "y" and y_input!= "":
                    y_input = y_input[:-1]
                elif active_field == "z" and z_input!= "":
                    z_input = z_input[:-1]
            if event.key == pygame.K_TAB:
                if active_field == "x":
                    active_field = "y"
                elif active_field == "y":
                    active_field = "z"
                elif active_field == "z":
                    active_field = "x"
            if event.unicode.isdigit() or event.unicode == "-":
                if active_field == "x":
                    x_input += event.unicode
                elif active_field == "y":
                    y_input += event.unicode
                elif active_field == "z":
                    z_input += event.unicode

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    update(offset)
    generate_hypercube(offset)

    # Отрисовка координат
    draw_text((-23, 32.0, 0), "X: " + str(offset[0]), (255, 255, 255))
    draw_text((-17, 32.0, 0), "Y: " + str(offset[1]), (255, 255, 255))
    draw_text((-11, 32.0, 0), "Z: " + str(offset[2]), (255, 255, 255))

    # Отрисовка полей ввода
    if active_field == "x":
        draw_text((-23, 28.0, 0), "Координата X: " + x_input + "_", (255, 255, 255))
    else:
        draw_text((-23, 28.0, 0), "Координата X: " + x_input, (255, 255, 255))
    if active_field == "y":
        draw_text((-23.5, 25, 0), "Координата Y: " + y_input + "_", (255, 255, 255))
    else:
        draw_text((-23.5, 25, 0), "Координата Y: " + y_input, (255, 255, 255))
    if active_field == "z":
        draw_text((-24, 22.0, 0), "Координата Z: " + z_input + "_", (255, 255, 255))
    else:
        draw_text((-24, 22.0, 0), "Координата Z: " + z_input, (255, 255, 255))

    # Отрисовка кнопки отправить
    draw_text((-25, 18.0, 0), "Переключиться Tab", (255, 255, 255))

    pygame.display.flip()
    clock.tick(60)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    update(offset)
    generate_hypercube(offset)

    # Отрисовка координат
    draw_text((-23, 32.0, 0), "X: " + str(offset[0]), (255, 255, 255))
    draw_text((-17, 32.0, 0), "Y: " + str(offset[1]), (255, 255, 255))
    draw_text((-11, 32.0, 0), "Z: " + str(offset[2]), (255, 255, 255))

    # Отрисовка полей ввода
    draw_text((-23, 28.0, 0), "Координата X: " + x_input, (255, 255, 255))
    draw_text((-23.5, 25, 0), "Координата Y: " + y_input, (255, 255, 255))
    draw_text((-24, 22.0, 0), "Координата Z: " + z_input, (255, 255, 255))

    # Отрисовка кнопки отправить
    draw_text((-25, 18.0, 0), "Переключиться Tab", (255, 255, 255))

    pygame.display.flip()
    clock.tick(60)
