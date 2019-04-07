import math
import random
import operator


class GeneticAlgorithm:
    def __init__(self, population_size=20, elite_rate=0.2, mutate_rate=0.1):
        self._elite_size = math.floor(population_size * elite_rate)
        self.mutate_rate = mutate_rate
        self.population_size = population_size
        self.population = None

    def run(self, max_iteration):
        self.initialise()

        fitnesses = [self.best_fitness_individual()]

        for i in range(max_iteration):
            self.evolve()
            fitnesses.append(self.best_fitness_individual())

        best_solution = max(fitnesses, key=operator.itemgetter(1))[0]

        return [fitness for (individual, fitness) in fitnesses], best_solution

    def best_fitness_individual(self):
        index, fitness = self._sort_population()[0]
        return self.population[index], fitness

    def _sort_population(self):
        fitnesses = list(
            (i, self.fitness(x)) for i, x in enumerate(self.population))

        return sorted(fitnesses, key=operator.itemgetter(1), reverse=True)

    def _natural_selection(self, sorted_population):
        mating_pool = []
        fitness_sum = sum([x[1] for x in sorted_population])

        for i in range(self._elite_size):
            mating_pool.append(sorted_population[i][0])

        for i in range(self.population_size - self._elite_size):
            pick = fitness_sum * random.random()
            # print(pick)
            local_fitness_sum = 0.0
            for i in range(self.population_size):
                local_fitness_sum += sorted_population[i][1]
                # print(local_fitness_sum)
                if pick < local_fitness_sum:
                    mating_pool.append(sorted_population[i][0])
                    break
        # import pdb; pdb.set_trace()

        return mating_pool

    def _breed(self, mating_pool):
        children = []

        for i in range(self._elite_size):
            children.append(self.population[mating_pool[i]])

        for i in range(self.population_size - self._elite_size):
            (parent1, parent2) = random.sample(mating_pool, 2)
            children.append(
                self.crossover(self.population[parent1],
                               self.population[parent2]))

        return children

    def _mutate_population(self, children):
        mutated = []
        for x in children:
            mutated.append(self.mutate(x))
        return mutated

    def evolve(self):
        sorted_population = self._sort_population()
        # print(sorted_population)
        # import pdb; pdb.set_trace()
        mating_pool = self._natural_selection(sorted_population)
        # print(mating_pool)
        # import pdb; pdb.set_trace()
        children = self._breed(mating_pool)
        next_population = self._mutate_population(children)
        self.population = next_population

    def initialise(self):
        raise NotImplementedError()

    def fitness(self, individual):
        raise NotImplementedError()

    def crossover(self, parent1, parent2):
        raise NotImplementedError()

    def mutate(self):
        raise NotImplementedError()


class TSPGA(GeneticAlgorithm):
    def __init__(self, city_coordinates, **kwargs):
        self._city_coordinates = city_coordinates
        self._distance_graph = self._generate_distance_graph(city_coordinates)
        self.n_city = len(city_coordinates)

        super(TSPGA, self).__init__(**kwargs)

    def _generate_individual(self):
        return random.sample(range(self.n_city), self.n_city)

    def initialise(self):
        self.population = list(
            self._generate_individual() for _ in range(self.population_size))

    def fitness(self, individual):
        distance = 0.0
        for i in range(self.n_city):
            source = individual[i]
            target = individual[(i + 1) % self.n_city]
            distance += self._distance_graph[source][target]
        return 1.0 / distance

    def crossover(self, parent1, parent2):
        cut1, cut2 = random.sample(range(self.n_city + 1), 2)

        cutL = min(cut1, cut2)
        cutR = max(cut1, cut2)

        segment = []

        for i in range(cutL, cutR):
            segment.append(parent1[i])

        child = [x for x in parent2 if x not in segment]

        for i in range(cutL, cutR):
            child.insert(i, parent1[i])

        return child

    def mutate(self, individual):
        mutated = list(individual)
        for i in range(len(individual)):
            if random.random() < self.mutate_rate:
                swap = int(random.random() * len(individual))
                mutated[i], mutated[swap] = mutated[swap], mutated[i]
        return mutated

    @staticmethod
    def _generate_distance_graph(city_coordinates):
        graph = []

        def distance(p1, p2):
            return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

        for i in range(len(city_coordinates)):
            row = []
            for j in range(len(city_coordinates)):
                row.append(distance(city_coordinates[i], city_coordinates[j]))
            graph.append(row)

        return graph


def city():
    return [
        (0, 0),
        (100, 0),
        (200, 0),
        (200, 100),
        (200, 200),
        (100, 200),
        (0, 200),
        (0, 100),
    ]


if __name__ == '__main__':
    city_coordinates = city()
    ga = TSPGA(city_coordinates)
    ga.run(1000)
