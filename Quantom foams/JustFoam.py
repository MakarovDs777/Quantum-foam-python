import numpy as np
import matplotlib.pyplot as plt
from perlin_numpy import generate_perlin_noise_3d
from mayavi import mlab

# Параметры шума Перлина
octaves = 4
persistence = 0.5
lacunarity = 2

# Создание 3D-массива шума Перлина
noise = generate_perlin_noise_3d(
    (32, 32, 32), (octaves, persistence, lacunarity), tileable=(False, False, False)
)

# Размер куба
cube_size = 10

# Создание 3D-сетки для куба
x, y, z = np.mgrid[0:cube_size:32j, 0:cube_size:32j, 0:cube_size:32j]

# Применение шума Перлина к сетке
U = noise[x, y, z]
V = noise[x, y, z]
W = noise[x, y, z]

# Визуализация шумового поля в кубе
mlab.quiver3d(x, y, z, U, V, W, scale_factor=0.25)
mlab.show()
