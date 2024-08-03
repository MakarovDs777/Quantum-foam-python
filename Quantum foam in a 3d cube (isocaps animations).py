import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import gaussian_filter
from skimage import measure

# Настройка интерактивного режима Matplotlib
plt.ion()

# Создание окна для графика
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Задание значения изоповерхности
isoval = 0.5

# Функция для генерации случайных данных и визуализации изоповерхности
def generate_and_plot():
    # Генерация случайных данных
    np.random.seed(np.random.randint(0, 1000))
    data = np.random.rand(50, 50, 50)

    # Фильтрация данных
    data = gaussian_filter(data, sigma=2)

    # Создание изоповерхности
    verts, faces, _, _ = measure.marching_cubes(data, isoval)

    # Визуализация изоповерхности
    ax.clear()
    ax.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2], triangles=faces, cmap='viridis', alpha=0.5)

    # Настройка освещения
    ax.set_axis_off()
    ax.set_aspect('equal')
    ax.view_init(elev=30, azim=60)

    # Пауза для анимации
    plt.pause(0.5)

# Генерация и визуализация случайных данных в цикле
while True:
    generate_and_plot()

# Выключение интерактивного режима Matplotlib
plt.ioff()
