import math
import random
import pdb

import matplotlib.pyplot as plt

from ga import TSPGA


class TSPGA_PMX(TSPGA):
    def crossover(self, parent1, parent2):
        cut1, cut2 = random.sample(range(self.n_city + 1), 2)

        cutL = min(cut1, cut2)
        cutR = max(cut1, cut2)

        child = list(parent1)

        child[cutL:cutR] = parent2[cutL:cutR]

        used = []

        for i in range(len(parent1)):
            if i in range(cutL, cutR) or child[i] not in child[cutL:cutR]:
                used.append(child[i])

        for i in range(len(parent1)):
            if i not in range(
                    cutL, cutR
            ) and child[i] in child[cutL:cutR] and child[i] in used:
                while child[i] in used:
                    child[i] = (child[i] + 1) % self.n_city
                used.append(child[i])

        return child


class TSPGA_OX(TSPGA):
    def crossover(self, parent1, parent2):
        cut1, cut2 = random.sample(range(self.n_city + 1), 2)

        cutL = min(cut1, cut2)
        cutR = max(cut1, cut2)

        child = list(parent2)

        j = cutR % self.n_city

        for i in list(range(cutR, len(child))) + list(range(cutL)):
            while parent1[j] in child[cutL:cutR]:
                j = (j + 1) % self.n_city
            child[i] = parent1[j]
            j = (j + 1) % self.n_city

        return child


class TSPGA_CX(TSPGA):
    def crossover(self, parent1, parent2):
        child = list(parent2)

        reverse1 = list(parent1)
        for i in range(len(parent1)):
            reverse1[parent1[i]] = i

        i = 0
        while child[i] != parent1[i]:
            child[i] = parent1[i]
            i = reverse1[parent2[i]]

        return child


class TSPGA_MX(TSPGA):
    def crossover(self, parent1, parent2):
        cut = random.sample(range(self.n_city + 1), 1)[0]
        child = list(parent1)
        j = 0
        for i in range(cut, len(parent2)):
            while parent2[j] in child[:cut]:
                j = (j + 1) % self.n_city
            child[i] = parent2[j]
            j = (j + 1) % self.n_city

        return child


def generate_city_circle(n_city, radius=10.0):
    cities = []

    for i in range(n_city):
        hdg = math.pi * 2.0 / n_city * i
        x = math.cos(hdg) * radius
        y = math.sin(hdg) * radius
        cities.append((x, y))

    return cities


def plot_city(cities, path):
    x = []
    y = []

    for i in path:
        x.append(cities[i][0])
        y.append(cities[i][1])

    scale = max(x) / 100.0

    plt.plot(x, y, 'co')

    for i in range(-1, len(path) - 1):
        plt.arrow(
            x[i],
            y[i], (x[i + 1] - x[i]), (y[i + 1] - y[i]),
            head_width=scale,
            color='g',
            length_includes_head=True)

    plt.show()


if __name__ == '__main__':
    cities = generate_city_circle(30)
    kwargs = {
        'population_size': 50,
        'mutate_rate': 0.02,
        'elite_rate': 0.4,
    }
    N = 500
    fitnesses1, best_result = TSPGA_PMX(cities, **kwargs).run(N)
    plot_city(cities, best_result)
    fitnesses2, best_result = TSPGA_CX(cities, **kwargs).run(N)
    plot_city(cities, best_result)
    fitnesses3, best_result = TSPGA_OX(cities, **kwargs).run(N)
    plot_city(cities, best_result)
    fitnesses4, best_result = TSPGA(cities, **kwargs).run(N)
    plot_city(cities, best_result)

    plt.plot([1.0 / f for f in fitnesses1], label='PMX')
    plt.plot([1.0 / f for f in fitnesses2], label='CX')
    plt.plot([1.0 / f for f in fitnesses3], label='OX')
    plt.plot([1.0 / f for f in fitnesses4], label='X')
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.legend()
    plt.show()
