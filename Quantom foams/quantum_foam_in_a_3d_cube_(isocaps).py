import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import gaussian_filter
from skimage import measure

# Генерация случайных данных
np.random.seed(0)
data = np.random.rand(50, 50, 50)

# Фильтрация данных
data = gaussian_filter(data, sigma=2)

# Создание изоповерхности
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Задание значения изоповерхности
isoval = 0.5

# Создание изоповерхности
verts, faces, _, _ = measure.marching_cubes(data, isoval)

# Визуализация изоповерхности
ax.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2], triangles=faces, cmap='viridis', alpha=0.5)

# Настройка освещения
ax.set_axis_off()
ax.set_aspect('equal')
ax.view_init(elev=30, azim=60)

plt.show()