import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols
from mayavi import mlab

x,y,z = symbols('x y z')
def gradient(f):
    return (f.diff(x), f.diff(y),f.diff(z))

f = x*y**2+z**2
g = gradient(f)

xrange = np.linspace(-3,3,15)
yrange = np.linspace(-3,3,15)
zrange = np.linspace(-3,3,15)
X,Y,Z = np.meshgrid(xrange, yrange, zrange)

U = np.zeros((15,15,15))
V = np.zeros((15,15,15))
W = np.zeros((15,15,15))

for i in range(len(xrange)):
    for j in range(len(yrange)):
        for k in range(len(zrange)):
            x1 = X[i,j,k]
            y1 = Y[i,j,k]
            z1 = Z[i,j,k]
            U[i,j,k] = g[0].subs({x:x1, y:y1, z:z1})
            V[i,j,k] = g[1].subs({x:x1, y:y1, z:z1})
            W[i,j,k] = g[2].subs({x:x1, y:y1, z:z1})


mlab.quiver3d(X,Y,Z,U,V,W)
mlab.show()
