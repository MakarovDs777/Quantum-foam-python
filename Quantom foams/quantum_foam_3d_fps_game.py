import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from scipy.ndimage import gaussian_filter
from skimage import measure

# Инициализация Pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

# Настройка перспективы
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, -1.0, -5)

# Задание значения изоповерхности
isoval = 0.5

# Угол обзора камеры
angle_x = 0
angle_y = 0

# Функция для генерации квантовой пены
def generate_quantum_foam():
    # Генерация случайных данных
    np.random.seed(np.random.randint(0, 1000))
    data = np.random.rand(50, 50, 50)

    # Фильтрация данных
    data = gaussian_filter(data, sigma=2)

    # Создание изоповерхности
    verts, faces, _, _ = measure.marching_cubes(data, isoval)

    # Отрисовка изоповерхности
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vert in face:
            glVertex3fv(verts[vert] * 0.1)
    glEnd()

# Основной цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Управление камерой с помощью клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        glTranslatef(0, 0, 0.1)
    if keys[pygame.K_s]:
        glTranslatef(0, 0, -0.1)
    if keys[pygame.K_a]:
        glTranslatef(-0.1, 0, 0)
    if keys[pygame.K_d]:
        glTranslatef(0.1, 0, 0)

    # Управление камерой с помощью мыши
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:  # Левая кнопка мыши
        mouse_pos = pygame.mouse.get_pos()
        angle_x += (mouse_pos[1] - display[1] // 2) * 0.01
        angle_y += (mouse_pos[0] - display[0] // 2) * 0.01
        glRotatef(angle_x, 1, 0, 0)
        glRotatef(angle_y, 0, 1, 0)
        pygame.mouse.set_pos((display[0] // 2, display[1] // 2))

    # Отрисовка сцены
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    generate_quantum_foam()
    pygame.display.flip()
    pygame.time.wait(10)