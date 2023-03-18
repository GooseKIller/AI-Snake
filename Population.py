from NeuralNet import NeuralNet
from Snake_logic import Snake


class Population:
    def __init__(self, size_population=1, gens=1, moves=5000, map_size=8, load=False):
        # size of 1 generation
        self.size_population = size_population
        self.gens = gens
        self.snakes = [NeuralNet(16, 18, 4) for i in range(self.size_population)]
        self.moves = moves
        self.map_size = map_size
        self.best_snakes = [(self.snakes[0], 0)]
        self.mutation_rate = 0.01
        if load:
            snake = self.snakes[0].table_to_net()
            self.best_snakes = [snake, snake]
            self.new_generation()

    def learn_snake(self, snake_brain=NeuralNet(16, 18, 4)):
        def max_index(arr):
            max_val = max(arr)
            move_id = arr.index(max_val)
            return move_id

        snake = Snake(self.map_size)
        for i in range(self.moves):
            if snake.is_lose():
                break
            move = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            vision = snake.snake_vision()
            decision = snake_brain.output(vision)
            dx, dy = move[max_index(decision)]
            snake.snake_move(dx, dy)
        self.best_snakes.append((snake_brain, snake.length_snake))

    def best_snakes(self):
        mom, dad = sorted(self.best_snakes(), key=lambda x: x[1], reverse=True)[:2]
        print(f"Best Score:{mom[1]}")
        return mom, dad

    def natural_selection(self):
        for snake in self.snakes:
            self.learn_snake(snake)

    def new_generation(self):
        mom, dad = self.best_snakes()
        child = mom.mutate(dad)
        child.net_to_table()
        snakes = []

        for i in range(self.size_population):
            snakes.append(child.copy().mutate(self.mutation_rate))

        self.snakes = snakes

    def start_learning(self):
        for i in range(self.gens):
            self.natural_selection()
            self.new_generation()


if __name__ == "__main__":
    population = Population(size_population=2000, gens=3, moves=3000)