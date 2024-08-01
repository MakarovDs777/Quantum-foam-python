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
                                                 base=42)

# Нормализация шума в диапазон от 0 до 1
noise = (noise - noise.min()) / (noise.max() - noise.min())

# Размер куба
cube_size = 10

# Создание 3D-сетки для куба
x, y, z = np.mgrid[0:cube_size:32j, 0:cube_size:32j, 0:cube_size:32j]

# Применение шума Перлина к сетке
U = noise
V = noise
W = noise

# Визуализация шумового поля в кубе
mlab.quiver3d(x.ravel(), y.ravel(), z.ravel(), U.ravel(), V.ravel(), W.ravel(), scale_factor=0.25)
mlab.show()
