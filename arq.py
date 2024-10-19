import random

class GeneticAlgorithm:
    def __init__(self, population_size, generations, mutation_rate, crossover_rate):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = []

    def initialize_population(self, individual_size, representation="integer"):
        """Inicializa a população com soluções aleatórias"""
        if representation == "integer":
            self.population = [
                [random.randint(0, 100) for _ in range(individual_size)]
                for _ in range(self.population_size)
            ]
        elif representation == "real":
            self.population = [
                [random.uniform(0, 1) for _ in range(individual_size)]
                for _ in range(self.population_size)
            ]

    def fitness(self, individual):
        """Calcula e retorna a adequação (fitness) de um indivíduo"""
        # Exemplo: Soma de todos os elementos do indivíduo
        return sum(individual)

    def selection(self):
        """Seleciona um indivíduo usando roleta viciada"""
        total_fitness = sum(self.fitness(ind) for ind in self.population)
        pick = random.uniform(0, total_fitness)
        current = 0

        for individual in self.population:
            current += self.fitness(individual)
            if current >= pick:
                return individual

    def crossover_integer(self, parent1, parent2):
        """Crossover de ponto único para inteiros"""
        point = random.randint(1, len(parent1) - 1)
        offspring1 = parent1[:point] + parent2[point:]
        offspring2 = parent2[:point] + parent1[point:]
        return offspring1, offspring2

    def crossover_real(self, parent1, parent2):
        """Crossover aritmético para valores reais"""
        alpha = random.uniform(0, 1)
        offspring1 = [(alpha * p1 + (1 - alpha) * p2) for p1, p2 in zip(parent1, parent2)]
        offspring2 = [(alpha * p2 + (1 - alpha) * p1) for p1, p2 in zip(parent1, parent2)]
        return offspring1, offspring2

    def mutation(self, individual, representation="integer"):
        """Realiza a mutação em um indivíduo"""
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                if representation == "integer":
                    individual[i] = random.randint(0, 100)
                elif representation == "real":
                    individual[i] = random.uniform(0, 1)

    def evolve(self, individual_size, representation="integer"):
        """Executa o ciclo evolutivo do algoritmo genético"""
        self.initialize_population(individual_size, representation)

        for generation in range(self.generations):
            # Avalia a adequação de cada indivíduo na população
            fitness_scores = [self.fitness(individual) for individual in self.population]

            # Seleciona indivíduos para a reprodução
            new_population = []
            while len(new_population) < self.population_size:
                parent1 = self.selection()
                parent2 = self.selection()

                # Realiza o crossover
                if random.random() < self.crossover_rate:
                    if representation == "integer":
                        offspring1, offspring2 = self.crossover_integer(parent1, parent2)
                    elif representation == "real":
                        offspring1, offspring2 = self.crossover_real(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1, parent2

                # Realiza a mutação
                self.mutation(offspring1, representation)
                self.mutation(offspring2, representation)

                new_population.extend([offspring1, offspring2])

            # Atualiza a população
            self.population = new_population[:self.population_size]

            # Exibir melhor indivíduo por geração (opcional)
            best_individual = max(self.population, key=self.fitness)
            print(f"Geração {generation + 1}: Melhor Fitness = {self.fitness(best_individual)}")

if __name__ == "__main__":
    # Exemplo de como iniciar o algoritmo genético
    ga = GeneticAlgorithm(population_size=20, generations=10, mutation_rate=0.1, crossover_rate=0.8)
    ga.evolve(individual_size=5, representation="integer")  # Para inteiros
    # ga.evolve(individual_size=5, representation="real")  # Para valores reais
