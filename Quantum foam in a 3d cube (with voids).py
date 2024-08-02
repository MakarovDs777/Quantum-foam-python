import noise as perlin_noise
import numpy as np
from mayavi import mlab

# Параметры шума Перлина
octaves = 4
persistence = 0.5
lacunarity = 2

# Создание 3D-массива шума Перлина
shape = (32, 32, 32)
scale = 10.0

# Размер куба
cube_size = 10

# Создание 3D-сетки для куба
x, y, z = np.mgrid[0:cube_size:32j, 0:cube_size:32j, 0:cube_size:32j]

# Инициализация фигуры
fig = mlab.figure()

# Анимационный цикл
for i in range(100):
    # Генерация нового шума Перлина
    noise = np.zeros(shape)
    for j in range(shape[0]):
        for k in range(shape[1]):
            for l in range(shape[2]):
                noise[j][k][l] = perlin_noise.pnoise3(j/scale, 
                                                     k/scale, 
                                                     l/scale, 
                                                     octaves=octaves, 
                                                     persistence=persistence, 
                                                     lacunarity=lacunarity, 
                                                     repeatx=shape[0], 
                                                     repeaty=shape[1], 
                                                     repeatz=shape[2], 
                                                     base=i)

    # Нормализация шума в диапазон от 0 до 1
    noise = (noise - noise.min()) / (noise.max() - noise.min())

    # Применение шума Перлина к сетке
    U = noise
    V = noise
    W = noise

    # Создание областей пустоты (войдов)
    voids = noise < 0.5
    voids_1d = np.ravel(voids)

    # Очистка предыдущей фигуры
    mlab.clf()

    # Визуализация шумового поля в кубе
    x_filt = x.ravel()[~voids_1d]
    y_filt = y.ravel()[~voids_1d]
    z_filt = z.ravel()[~voids_1d]
    U_filt = U.ravel()[~voids_1d]
    V_filt = V.ravel()[~voids_1d]
    W_filt = W.ravel()[~voids_1d]

    mlab.quiver3d(x_filt, y_filt, z_filt, U_filt, V_filt, W_filt, scale_factor=0.25, color=(1.0, 0.0, 0.0))

mlab.show()
