import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import noise as perlin_noise
import time

# Параметры шума Перлина
octaves = 4
persistence = 0.5
lacunarity = 2

# Создание 3D-массива шума Перлина
shape = (64, 64, 64)
scale = 10.0

# Нормализация шума в диапазон от 0 до 1
def normalize_noise(noise):
    return (noise - noise.min()) / (noise.max() - noise.min())

# Генерация шума Перлина для одного кадра
def generate_noise(base):
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

# Размер куба
cube_size = 10

# Создание 3D-сетки для куба
x, y, z = np.mgrid[0:cube_size:64j, 0:cube_size:64j, 0:cube_size:64j]

# Оператор размазывания
def smear_operator(noise):
    smeared_noise = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                smeared_noise[i][j][k] = (noise[i][j][k] + noise[(i+1)%shape[0]][j][k] + noise[i][(j+1)%shape[1]][k] + noise[i][j][(k+1)%shape[2]]) / 4
    return smeared_noise

# Функция для обновления кадра
def update(frame, base):
    noise = generate_noise(base)
    for i in range(50):  # 50 размазываний
        noise = smear_operator(noise)
    U = np.where(noise > 0.5, noise, 0)  # Устанавливаем значение в 0, если шум ниже 0.5
    V = np.where(noise < 0.5, noise, 0)  # Устанавливаем значение в 0, если шум выше 0.5
    ax.clear()  # Очистка текущего кадра
    ax.scatter(x.ravel(), y.ravel(), z.ravel(), c=U.ravel(), cmap='viridis', alpha=0.5)
    ax.scatter(x.ravel(), y.ravel(), z.ravel(), c=V.ravel(), cmap='plasma', alpha=0.5)

# Создание анимации
base = 0  # Начальная база
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.ion()  # Включение интерактивного режима

# Запуск анимации
for i in range(100):
    base += 1  # Изменяем базу на 1
    update(i, base)
    plt.pause(0.1)  # Пауза между кадрами
    plt.draw()
