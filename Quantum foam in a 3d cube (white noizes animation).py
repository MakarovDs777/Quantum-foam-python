import numpy as np
from mayavi import mlab
import noise as perlin_noise
import time
import pyautogui

# Параметры шума Перлина
octaves = 4
persistence = 0.5
lacunarity = 2

# Создание 3D-массива шума Перлина
shape = (32, 32, 32)
scale = 10.0

# Нормализация шума в диапазон от 0 до 1
def normalize_noise(noise):
    return (noise - noise.min()) / (noise.max() - noise.min())

# Генерация шума Перлина для одного кадра
def generate_noise():
    noise = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                noise[i][j][k] = perlin_noise.pnoise3(i/scale,
                                                     j/scale,
                                                     k/scale,
                                                     octaves=octaves,
                                                     persistence=persistence,
                                                     lacunarity=lacunarity,
                                                     repeatx=shape[0],
                                                     repeaty=shape[1],
                                                     repeatz=shape[2],
                                                     base=np.random.randint(0, 100))  # Случайная база для каждого кадра
    return normalize_noise(noise)

# Размер куба
cube_size = 10

# Создание 3D-сетки для куба
x, y, z = np.mgrid[0:cube_size:32j, 0:cube_size:32j, 0:cube_size:32j]

# Функция для обновления кадра
def update(frame):
    mlab.clf()  # Очистка текущего кадра
    noise = generate_noise()
    U = noise
    V = noise
    W = noise
    mlab.quiver3d(x.ravel(), y.ravel(), z.ravel(), U.ravel(), V.ravel(), W.ravel(), scale_factor=0.25)

# Создание анимации
fig = mlab.figure(size=(600, 600))

# Запуск анимации
for i in range(100):
    update(i)
    mlab.draw()
    mlab.show(stop=True)  # Показываем окно с кнопкой "Stop Interaction"
    time.sleep(0.1)  # Ждем немного, чтобы окно успело появиться
    pyautogui.click()  # Симулируем нажатие кнопки мыши
