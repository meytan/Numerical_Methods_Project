import math
from cmath import exp, pi

import numpy as np


def sdm(function, gradient, start, step, accuracy=(0.001, 0.001, 0.001)):
    def fun(point1):
        x, y = point1
        return eval(function)

    def vector_length(point_a, point_b):
        return ((point_a - point_b) ** 2).sum() ** 0.5

    def grad(point3):
        x, y = point3
        return np.array([eval(gradient[0]), eval(gradient[1])]) * -1

    def unit_vector(v):
        return v / (v ** 2).sum() ** 0.5

    point = np.array(start)
    route = [point]
    n = 1
    while True:
        last_point = point
        grad_in_point = grad(point)
        if np.isnan(grad_in_point[0]):
            minimum1 = sdm(function, gradient, (point[0]+step, point[1]), step, accuracy)
            minimum2 = sdm(function, gradient, (point[0]-step, point[1]), step, accuracy)
            if minimum1['minimum'] > minimum2['minimum']:
                route.extend(minimum2['route'])

            else:
                route.extend(minimum1['route'])
            point = route[-1]
            break
        elif np.isnan(grad_in_point[1]):
            minimum1 = sdm(function, gradient, (point[0], point[1]+step), step, accuracy)
            minimum2 = sdm(function, gradient, (point[0], point[1]-step), step, accuracy)
            if minimum1['minimum'] > minimum2['minimum']:
                route.extend(minimum2['route'])

            else:
                route.extend(minimum1['route'])
            point = route[-1]
            break


        u = unit_vector(grad_in_point)
        point = last_point + u * step

        route.append(point)
        n += 1

        if vector_length(point, last_point) < accuracy[0]:
            break
        elif (grad_in_point ** 2).sum() ** 0.5 < accuracy[1]:
            break
        elif abs(fun(last_point) - fun(point)) < accuracy[2]:
            break
        elif abs(fun(last_point) - fun(point)) < step and n % 10000 == 0:
            step /= 2
        elif n == 1000000:
            raise ValueError()

    return {"minimum": fun(point), "point": point, "route": route}


def fft(samples):
    N = len(samples)
    if N <= 1: return samples
    even = fft(samples[0::2])
    odd = fft(samples[1::2])
    T = [exp(-2j * pi * k / N) * odd[k] for k in range(N // 2)]
    return [even[k] + T[k] for k in range(N // 2)] + [even[k] - T[k] for k in range(N // 2)]
