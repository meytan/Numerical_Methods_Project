import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from numerical_methods import sdm


def fft_plots(x1, y1, x2, y2):
    plt.subplot(2, 1, 1)
    plt.plot(x1, y1, '-')
    plt.title('FFT')
    plt.ylabel('Amplitude')
    plt.xlabel('time (s)')
    plt.grid(True, axis='y')

    plt.subplot(2, 1, 2)
    plt.plot(x2, y2, '-')
    plt.xlabel('frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.minorticks_on()
    plt.grid(True, which='both')
    plt.show()

    plt.show()


def sdm_plot(function, minimum, scope=(-3, 3)):
    def z_func(x, y):
        return eval(function)

    point = minimum.get("point")
    route = minimum.get("route")

    route_x = [x[0] for x in route]
    route_y = [y[1] for y in route]

    x = np.arange(scope[0], scope[1], abs(scope[1]-scope[0])/1000)
    y = np.arange(scope[0], scope[1], abs(scope[1]-scope[0])/1000)
    X, Y = np.meshgrid(x, y)
    # grid of point

    Z = z_func(X, Y)  # evaluation of the function on the grid

    f = Figure(figsize=(7, 7), dpi=250)
    a = f.add_subplot(111)

    im = a.imshow(Z, cmap=plt.cm.RdYlBu, extent=[scope[0], scope[1], scope[0], scope[1]],
                  interpolation='nearest')  # drawing the function

    f.colorbar(im)

    a.plot(point[0], point[1], 'bx')
    a.plot(route_x, route_y, 'g-')
    a.set_title(f'The value of minimum of this function is oscillate around \n{minimum.get("minimum")}\n at point '
             f'{minimum.get("point")}')
    return f




# (x+2*y-7)**2 + (2*x+y-5)**2
# 10*x+8*y-34
# 8*x+10*y-38