import random
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols
from mayavi import mlab

x,y,z = symbols('x y z')


def gradient(f):
    return (f.diff(x), f.diff(y),f.diff(z))


def generate_random_field(xrange, yrange, zrange):
    """генерирует случайное векторное поле в пределах заданных диапазонов."""
    X,Y,Z = np.meshgrid(xrange, yrange, zrange)
    U = np.random.rand(X.shape[0], X.shape[1], X.shape[2])
    V = np.random.rand(X.shape[0], X.shape[1], X.shape[2])
    W = np.random.rand(X.shape[0], X.shape[1], X.shape[2])
    return X, Y, Z, U, V, W


def plot_vector_field(X, Y, Z, U, V, W):
    """Постройте векторное поле с помощью Mayavi."""
    mlab.quiver3d(X,Y,Z,U,V,W)
    mlab.show()


# Укажите диапазоны для векторного поля
xrange = np.linspace(-3,3,15)
yrange = np.linspace(-3,3,15)
zrange = np.linspace(-3,3,15)

# Сгенерируйте случайное векторное поле
X, Y, Z, U, V, W = generate_random_field(xrange, yrange, zrange)

# Построим векторное поле
plot_vector_field(X, Y, Z, U, V, W)