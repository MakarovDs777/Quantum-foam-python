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
# icon = pygame.image.load('PGM.png') 
# pygame.display.set_icon(icon)
pygame.display.set_caption('Procedural generator maker')
pygame.display.set_mode((0, 0), FULLSCREEN | DOUBLEBUF | OPENGL)

# Инициализация камеры
gluPerspective(25, (display[0]/display[1]), 0.1, 1000.0)
glTranslatef(-15, 0.0, -150.0)  # Переместить камеру вниз и назад
glRotatef(35, 1, 0, 0)  # Повернуть камеру на 35 градусов вокруг оси X

# Параметры шума Перлина
octaves = 4
persistence = 0.5
lacunarity = 2
scale = 10
smear = 0

# Размер чанка
chunk_size = 32

# Создание 3D-массива шума Перлина
shape = (chunk_size, chunk_size, chunk_size)

# Нормализация шума в диапазон от 0 до 1
def normalize_noise(noise):
    return (noise - noise.min()) / (noise.max() - noise.min())

# Генерация сид мира
seed = random.randint(0, 1000)

# Генерация шума Перлина для одного кадра
def generate_noise(base, offset):
    np.random.seed(seed)  # Установка сид для numpy
    random.seed(seed)  # Установка сид для random
    noise = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                # Добавьте уникальный шум для каждого чанка
                noise[i][j][k] = perlin_noise.pnoise3((i + offset[0]) / scale,
                                                     (j + offset[1]) / scale,
                                                     (k + offset[2]) / scale,
                                                     octaves=octaves,
                                                     persistence=persistence,
                                                     lacunarity=lacunarity,
                                                     repeatx=shape[0],
                                                     repeaty=shape[1],
                                                     repeatz=shape[2],
                                                     base=base) + \
                                perlin_noise.pnoise3((i + offset[0]) / (scale * 10),
                                                     (j + offset[1]) / (scale * 10),
                                                     (k + offset[2]) / (scale * 10),
                                                     octaves=octaves,
                                                     persistence=persistence,
                                                     lacunarity=lacunarity,
                                                     repeatx=shape[0],
                                                     repeaty=shape[1],
                                                     repeatz=shape[2],
                                                     base=random.randint(0, 1000))
    return normalize_noise(noise)

# Оператор размазывания
def smear_operator(noise):
    smeared_noise = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                smeared_noise[i][j][k] = (noise[i][j][k] + noise[(i+1)%shape[0]][j][k] + noise[i][(j+1)%shape[1]][k] + noise[i][j][(k+1)%shape[2]]) / 4
    return smeared_noise

# Чанки и их шум
chunks = {}  # Словарь для хранения шума каждого чанка

# Создание чанка и добавление его в словарь
def create_chunk(offset):
    base = random.randint(0, 1000)  # Случайный base для каждого чанка
    noise = generate_noise(base, offset)
    for i in range(50 - smear):  # 50 размазываний
        noise = smear_operator(noise)
    chunks[tuple(offset)] = noise

# Функция для обновления кадра
def update(offset):
    if current_mode != "optional":
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

        return verts, faces

# Функция для сохранения чанка в формате.obj
def save_chunk(verts, faces, filename):
    with open(filename, 'w') as f:
        for v in verts:
            f.write('v {:.6f} {:.6f} {:.6f}\n'.format(v[0], v[1], v[2]))
        for face in faces:
            f.write('f {} {} {}\n'.format(face[0]+1, face[1]+1, face[2]+1))

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
chunk_size_input = ""
seed_input = str(seed)
lang_input = ""
octaves_input = ""
persistence_input = ""
lacunarity_input = ""
scale_input = ""
smear_input = ""
single_base_input = "no"
active_field = "x"
current_mode = "main"
move_mode = "chunk"  # "chunk" для перемещения по чанкам, "free" для свободного режима перемещения
move_speed = 0.5
move_speed_input = ""
auto_chunk_random_input = ""
auto_chunk_random = ""
auto_chunk_random_speed = 1  # Скорость перемещения по случайным координатам
auto_chunk_random_speed_input = ""

draw_text_position = []
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if move_mode == "chunk":
                if event.key == pygame.K_w:
                    offset[2] += chunk_size * move_speed
                if event.key == pygame.K_s:
                    offset[2] -= chunk_size * move_speed
                if event.key == pygame.K_a:
                    offset[0] -= chunk_size * move_speed
                if event.key == pygame.K_d:
                    offset[0] += chunk_size * move_speed
                if event.key == pygame.K_q:
                    offset[1] -= chunk_size * move_speed
                if event.key == pygame.K_e:
                    offset[1] += chunk_size * move_speed
            else:
                if event.key == pygame.K_w:
                    offset[2] += move_speed
                if event.key == pygame.K_s:
                    offset[2] -= move_speed
                if event.key == pygame.K_a:
                    offset[0] -= move_speed
                if event.key == pygame.K_d:
                    offset[0] += move_speed
                if event.key == pygame.K_q:
                    offset[1] -= move_speed
                if event.key == pygame.K_e:
                    offset[1] += move_speed

            if event.key == pygame.K_RETURN:
                if x_input!= "" and y_input!= "" and z_input!= "":
                    offset[0] = int(x_input)
                    offset[1] = int(y_input)
                    offset[2] = int(z_input)
                    x_input = ""
                    y_input = ""
                    z_input = ""
                elif active_field == "octaves":
                    octaves = int(octaves_input)
                    octaves_input = ""
                elif active_field == "persistence":
                    persistence = float(persistence_input)
                    persistence_input = ""
                elif active_field == "lacunarity":
                    lacunarity = float(lacunarity_input)
                    lacunarity_input = ""
                elif active_field == "scale":
                    scale = float(scale_input)
                    scale_input = ""
                elif active_field == "smear":
                    smear = int(smear_input)
                    smear_input = ""
                elif active_field == "single_base":
                    if single_base_input.lower() == "yes":
                        base = random.randint(0, 1000)
                        chunks = {}  # Очистка словаря чанков
                        for offset in chunks:
                            noise = generate_noise(base, offset)
                            for i in range(50 - smear):  # 50 размазываний
                                noise = smear_operator(noise)
                            chunks[offset] = noise
                    elif single_base_input.lower() == "no":
                        chunks = {}  # Очистка словаря чанков
                    single_base_input = ""
                elif active_field == "move_speed":
                    try:
                        move_speed = float(move_speed_input)
                        move_speed_input = ""
                    except ValueError:
                        # Ignore invalid input (e.g., empty string or invalid format)
                        pass
                elif active_field == "auto_chunk_random":
                    if auto_chunk_random_input.lower() == "on":
                        auto_chunk_random = True
                    elif auto_chunk_random_input.lower() == "off":
                        auto_chunk_random = False
                    auto_chunk_random_input = ""
                elif active_field == "auto_chunk_random_speed":
                    try:
                        auto_chunk_random_speed = float(auto_chunk_random_speed_input)
                        auto_chunk_random_speed_input = ""
                    except ValueError:
                        # Ignore invalid input (e.g., empty string or invalid format)
                        pass
            if event.key == pygame.K_BACKSPACE:
                if active_field == "x" and x_input!= "":
                    x_input = x_input[:-1]
                elif active_field == "y" and y_input!= "":
                    y_input = y_input[:-1]
                elif active_field == "z" and z_input!= "":
                    z_input = z_input[:-1]
                elif active_field == "chunk_size" and chunk_size_input!= "":
                    chunk_size_input = chunk_size_input[:-1]
                elif active_field == "seed" and seed_input!= "":
                    seed_input = seed_input[:-1]
                elif active_field == "lang" and lang_input!= "":
                    lang_input = lang_input[:-1]
                elif active_field == "octaves" and octaves_input!= "":
                    octaves_input = octaves_input[:-1]
                elif active_field == "persistence" and persistence_input!= "":
                    persistence_input = persistence_input[:-1]
                elif active_field == "lacunarity" and lacunarity_input!= "":
                    lacunarity_input = lacunarity_input[:-1]
                elif active_field == "scale" and scale_input!= "":
                    scale_input = scale_input[:-1]
                elif active_field == "smear" and smear_input!= "":
                    smear_input = smear_input[:-1]
                elif active_field == "single_base" and single_base_input!= "":
                    single_base_input = single_base_input[:-1]
                elif active_field == "move_speed" and move_speed_input!= "":
                    move_speed_input = move_speed_input[:-1]
                elif active_field == "auto_chunk_random" and auto_chunk_random_input!= "":
                    auto_chunk_random_input = auto_chunk_random_input[:-1]
                elif active_field == "auto_chunk_random_speed" and auto_chunk_random_speed_input != "":
                    auto_chunk_random_speed_input = auto_chunk_random_speed_input[:-1]
            if event.key == pygame.K_TAB:
                if active_field == "x":
                    active_field = "y"
                elif active_field == "y":
                    active_field = "z"
                elif active_field == "z":
                    active_field = "chunk_size"
                elif active_field == "chunk_size":
                    active_field = "seed"
                elif active_field == "seed":
                    active_field = "single_base"
                elif active_field == "single_base":
                    active_field = "move_speed"
                elif active_field == "move_speed":
                    active_field = "auto_chunk_random"
                elif active_field == "auto_chunk_random":
                     active_field = "auto_chunk_random_speed"
                elif active_field == "auto_chunk_random_speed":
                    active_field = "x"
                elif active_field == "lang":
                    active_field = "octaves"
                elif active_field == "octaves":
                    active_field = "persistence"
                elif active_field == "persistence":
                    active_field = "lacunarity"
                elif active_field == "lacunarity":
                    active_field = "scale"
                elif active_field == "scale":
                    active_field = "smear"
                elif active_field == "smear":
                    active_field = "optional"
                elif active_field == "optional":
                    active_field = "x"
                    current_mode = "main"
            if event.unicode.isalpha() or event.unicode == "/":
                if active_field == "x":
                    x_input += event.unicode
                elif active_field == "y":
                    y_input += event.unicode
                elif active_field == "z":
                    z_input += event.unicode
                elif active_field == "chunk_size":
                    chunk_size_input += event.unicode
                elif active_field == "seed":
                    seed_input += event.unicode
                elif active_field == "lang":
                    lang_input += event.unicode
                elif active_field == "octaves":
                    octaves_input += event.unicode
                elif active_field == "persistence":
                    persistence_input += event.unicode
                elif active_field == "lacunarity":
                    lacunarity_input += event.unicode
                elif active_field == "scale":
                    scale_input += event.unicode
                elif active_field == "smear":
                    smear_input += event.unicode
                elif active_field == "single_base":
                    single_base_input += event.unicode
                elif active_field == "move_speed":
                    move_speed_input += event.unicode
                elif active_field == "auto_chunk_random":
                    auto_chunk_random_input += event.unicode
            if event.unicode.isalpha():
                if active_field == "lang":
                    lang_input += event.unicode
                elif active_field == "optional":
                    single_base_input += event.unicode
                elif active_field == "single_base":
                    single_base_input += event.unicode
            if event.key == pygame.K_r:
                verts, faces = update(offset)
                save_chunk(verts, faces, 'chunk.obj')
            if event.key == pygame.K_ESCAPE: 
                pygame.quit()
                quit()
            if event.key == pygame.K_F2:
                chunk_size = int(chunk_size_input)
                shape = (chunk_size, chunk_size, chunk_size)
            if event.key == pygame.K_F2:
                chunk_size = int(chunk_size_input)
                chunk_size_input = ""
                shape = (chunk_size, chunk_size, chunk_size)
            if event.key == pygame.K_RETURN:
                seed = int(seed_input)
                chunks = {}  # Очистка словаря чанков
            if event.key == pygame.K_F3:
                if current_mode == "main":
                    current_mode = "lang"
                    active_field = "lang"
                elif current_mode == "lang":
                    current_mode = "optional"
                    active_field = "optional"
                else:
                    current_mode = "main"
                    active_field = "x"
            if event.key == pygame.K_F4:
                if move_mode == "chunk":
                    move_mode = "free"
                else:
                    move_mode = "chunk"
            if event.unicode.isdigit() or event.unicode == '.':
                auto_chunk_random_speed_input += event.unicode
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    update(offset)

    if auto_chunk_random:
        if pygame.time.get_ticks() % 1000 < 50:
            offset = [random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100)]
            offset = [offset[0] * auto_chunk_random_speed, offset[1] * auto_chunk_random_speed, offset[2] * auto_chunk_random_speed]
    if current_mode == "main":
        if active_field == "x":
            draw_text((-24, 20.0, 0), "Координата X: " + x_input + "_", (255, 255, 255))
        else:
            draw_text((-24, 20.0, 0), "Координата X: " + x_input, (255, 255, 255))
        if active_field == "y":
            draw_text((-24.5, 17, 0), "Координата Y: " + y_input + "_", (255, 255, 255))
        else:
            draw_text((-24.5, 17, 0), "Координата Y: " + y_input, (255, 255, 255))
        if active_field == "z":
            draw_text((-25, 14, 0), "Координата Z: " + z_input + "_", (255, 255, 255))
        else:
            draw_text((-25, 14, 0), "Координата Z: " + z_input, (255, 255, 255))
        if active_field == "chunk_size":
            draw_text((-25.5, 11.0, 0), "LOD: " + chunk_size_input + "_", (255, 255, 255))
        else:
            draw_text((-25.5, 11.0, 0), "LOD: " + str(chunk_size), (255, 255, 255))
        if active_field == "seed":
            draw_text((-26, 8.0, 0), "Поменять сид: " + seed_input + "_", (255, 255, 255))
        else:
            draw_text((-26, 8.0, 0), "Поменять сид: " + str(seed), (255, 255, 255))
        if active_field == "single_base":
            draw_text((-26.5, 5.0, 0), "Единый base мира (yes/no): " + single_base_input + "_", (255, 255, 255))
        else:
            draw_text((-26.5, 5.0, 0), "Единый base мира (yes/no): " + single_base_input, (255, 255, 255))
        if active_field == "move_speed":
            draw_text((-27, 2.0, 0), "Скорость перемещения: " + move_speed_input + "_", (255, 255, 255))
        else:
            draw_text((-27, 2.0, 0), "Скорость перемещения: " + str(move_speed), (255, 255, 255))
        if active_field == "auto_chunk_random":
            draw_text((-27.5, -1.0, 0), "Auto chunk random (on/off): " + auto_chunk_random_input + "_", (255, 255, 255))
        else:
            draw_text((-27.5, -1.0, 0), "Auto chunk random (on/off): " + str(auto_chunk_random), (255, 255, 255))
        if active_field == "auto_chunk_random_speed":
            draw_text((-28, -4.0, 0), "Auto chunk random speed: " + auto_chunk_random_speed_input + "_", (255, 255, 255))
        else:
            draw_text((-28, -4.0, 0), "Auto chunk random speed: " + str(auto_chunk_random_speed), (255, 255, 255))
        # Отрисовка координат
        draw_text((-22.1, 32.0, 0), "X: " + str(offset[0]), (255, 255, 255))
        draw_text((-22.6, 29.0, 0), "Y: " + str(offset[1]), (255, 255, 255))
        draw_text((-23, 26.0, 0), "Z: " + str(offset[2]), (255, 255, 255))

        # Отрисовка сид мира
        draw_text((-23.5, 23.0, 0), "Сид мира: " + str(seed), (255, 255, 255))

    elif current_mode == "lang":
        # Отрисовка полей ввода для параметров шума Перлина
        if active_field == "octaves":
            draw_text((-22, 32.0, 0), "Octaves: " + octaves_input + "_", (255, 255, 255))
        else:
            draw_text((-22, 32.0, 0), "Octaves: " + octaves_input, (255, 255, 255))

        if active_field == "persistence":
            draw_text((-22.5, 29.0, 0), "Persistence: " + persistence_input + "_", (255, 255, 255))
        else:
            draw_text((-22.5, 29.0, 0), "Persistence: " + persistence_input, (255, 255, 255))

        if active_field == "lacunarity":
            draw_text((-23, 26.0, 0), "Lacunarity: " + lacunarity_input + "_", (255, 255, 255))
        else:
            draw_text((-23, 26.0, 0), "Lacunarity: " + lacunarity_input, (255, 255, 255))

        if active_field == "scale":
            draw_text((-23.5, 23.0, 0), "Scale: " + scale_input + "_", (255, 255, 255))
        else:
            draw_text((-23.5, 23.0, 0), "Scale: " + scale_input, (255, 255, 255))

        if active_field == "smear":
            draw_text((-24, 20.0, 0), "Smear APE: " + smear_input + "_", (255, 255, 255))
        else:
            draw_text((-24, 20.0, 0), "Smear APE: " + smear_input, (255, 255, 255))

    elif current_mode == "optional":
        pass
            
    # Отрисовка кнопки Merge
    draw_text((-35, -45.0, 0), "Переключиться Tab/Ввести случайный сид F1/Очистить размер чанка F2/Сохранить дамп чанка R/переключение вкладок F3/Режим камеры (Почанковое;свободное) перемещение F4", (255, 255, 255))

    pygame.display.flip()
    clock.tick(60)
