import numpy as np
from mayavi import mlab
import noise as perlin_noise
import time
import random

# Параметры шума Перлина
octaves = 4
persistence = 0.5
lacunarity = 2

# Создание 3D-массива шума Перлина
shape = (32, 32, 32)

# Нормализация шума в диапазон от 0 до 1
def normalize_noise(noise):
    return (noise - noise.min()) / (noise.max() - noise.min())

# Генерация шума Перлина для одного кадра
def generate_noise(base, scale):
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
                                                     base=int(base))
    return normalize_noise(noise)

# Создание 3D-сетки
x, y, z = np.mgrid[0:10:32j, 0:10:32j, 0:10:32j]

# Функция для обновления кадра
def update():
    base = random.randint(0, 1000)  # Случайный base для каждого кадра
    scale = random.uniform(1, 10)  # Случайный масштаб для каждого кадра
    noise = generate_noise(base, scale)
    U = np.where(noise > 0.5, noise, noise.min())  # Устанавливаем значение в минимальное, если шум ниже 0.5
    U = normalize_noise(U)  # Нормализация массива U
    mlab.clf()  # Очистка текущего кадра
    mlab.contour3d(U, contours=[0.5])  # Создание контура шума

# Запуск анимации
for i in range(100):
    update()
    mlab.draw()
    time.sleep(0.1)  # Пауза между кадрами
mlab.show()  # Отображение окна Mayavi
