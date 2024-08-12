import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import noise as perlin_noise
import time
import random
from skimage import measure

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

# Функция для обновления кадра
def update(ax):
    base = random.randint(0, 1000)  # Случайный base для каждого кадра
    scale = random.uniform(1, 10)  # Случайный масштаб для каждого кадра
    noise = generate_noise(base, scale)
    U = np.where(noise > 0.5, noise, noise.min())  # Устанавливаем значение в минимальное, если шум ниже 0.5
    U = normalize_noise(U)  # Нормализация массива U

    ax.clear()  # Очистка текущего окна

    x, y, z = np.indices(U.shape)
    ax.scatter(x.ravel(), y.ravel(), z.ravel(), c=U.ravel(), cmap='viridis', alpha=0.1)

    # Создание изосурфейса
    verts, faces, normals, values = measure.marching_cubes(U, level=0.5)
    ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], color='r', alpha=0.5)

# Запуск анимации
plt.ion()  # Включение интерактивного режима
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(100):
    update(ax)
    plt.pause(0.1)  # Пауза между кадрами
    plt.draw()  # Отрисовка текущего кадра

plt.ioff()  # Выключение интерактивного режима
plt.show()  # Отображение окончательного кадра