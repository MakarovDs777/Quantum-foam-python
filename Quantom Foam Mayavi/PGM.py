import numpy as np
from mayavi import mlab

# Параметры моделирования
N = 128  # Размер куба
L = 1.0  # Размер куба
N_steps = 1000  # Количество шагов в моделировании

# Создание массива для хранения значений поля
phi = np.zeros((N, N, N))

# Инициализация поля случайными значениями
phi += np.random.rand(N, N, N) * 2 * np.pi

# Моделирование поведения поля с помощью метода Монте-Карло
for step in range(N_steps):
    # Выбор случайной точки в объеме
    i, j, k = np.random.randint(0, N, 3)

    # Вычисление среднего значения поля в окрестности выбранной точки
    phi_avg = (phi[i, j, k] +
               phi[(i+1)%N, j, k] +
               phi[(i-1)%N, j, k] +
               phi[i, (j+1)%N, k] +
               phi[i, (j-1)%N, k] +
               phi[i, j, (k+1)%N] +
               phi[i, j, (k-1)%N]) / 7

    # Обновление значения поля в выбранной точке
    phi[i, j, k] = phi_avg + np.random.normal(0, 1) / np.sqrt(N)

# Визуализация результатов
fig = mlab.figure()
mlab.clf()

# Создание изолиний поверхности поля
mlab.contour3d(phi, contours=[0.5], opacity=0.8, colormap='viridis')

# Настройка отображения
mlab.title('Quantum Foam')
mlab.xlabel('X')
mlab.ylabel('Y')
mlab.zlabel('Z')
mlab.show()