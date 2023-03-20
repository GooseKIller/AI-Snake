from NeuralNet import NeuralNet
from Snake_logic import Snake

import pygame
import time


width, height = 512, 512
res = 8
sq_size = height // res

def draw_board(screen, map):
    colors = [pygame.Color((238, 238, 210)), pygame.Color((118, 150, 86))]
    for r in range(res):
        for c in range(res):
            color = colors[(r + c) % 2]
            unit = map[r][c]
            units = {"--": color, "SS": (0, 0, 0), "AA": (255, 0, 0)}
            pygame.draw.rect(screen, units[unit], pygame.Rect(c * sq_size, r * sq_size, sq_size, sq_size))


class Population:
    def __init__(self, size_population=1, gens=1, moves=5000, map_size=8, load=False):
        # size of 1 generation
        self.size_population = size_population
        self.gens = gens
        self.snakes = [NeuralNet(16, 18, 4) for _ in range(self.size_population)]
        self.moves = moves
        self.map_size = map_size
        self.all_snakes = [(self.snakes[0], 0)]
        self.mutation_rate = -0.5
        if load:
            snake = Snake(self.map_size)

            pygame.init()
            screen = pygame.display.set_mode((width, height))
            screen.fill((0, 155, 0))

            draw_board(screen, snake.map)

            snake_ai = NeuralNet(16, 18, 4)
            snake_ai.table_to_net()
            snake = Snake(self.map_size)
            for i in range(self.moves):

                draw_board(screen, snake.map)
                event = pygame.event.poll()

                if snake.is_lose():
                    break

                if snake.snake_cords() == snake.apple_cords():
                    if snake.is_win():
                        break
                    snake.eat_apple()
                move = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                vision = snake.snake_vision()
                mv = self.__max_index(snake_ai.output(snake.snake_vision()))
                decision = snake_ai.output(vision)
                dx, dy = move[mv]
                snake.snake_move(dx, dy)
                time.sleep(0.1)

                if event.type == pygame.QUIT:
                    pygame.quit()
                pygame.display.flip()

            print(snake.steps)
            self.all_snakes = [(snake_ai, snake.length_snake), (snake_ai, snake.length_snake)]
            # self.start_learning()

    @staticmethod
    def __max_index(arr):
        max_val = max(arr)
        move_id = arr.index(max_val)
        return move_id

    def learn_snake(self, snake_brain=NeuralNet(16, 18, 4), id=0):
        def max_index(arr):
            max_val = max(arr)
            move_id = arr.index(max_val)
            return move_id

        snake = Snake(self.map_size)

        for i in range(self.moves):
            if snake.is_lose():
                break
            if snake.snake_cords() == snake.apple_cords():
                if snake.is_win():
                    break
                snake.eat_apple()
            move = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            vision = snake.snake_vision()
            decision = snake_brain.output(vision)
            dx, dy = move[max_index(decision)]
            snake.snake_move(dx, dy)

        print(f"Length snake:{snake.length_snake}")
        self.all_snakes.append((snake_brain, snake.length_snake, id))

    def best_snakes(self):
        mom, dad, *others = sorted(self.all_snakes, key=lambda x: x[1], reverse=True)
        print(f"Best Scores:№1:{mom}\n№2:{dad}")
        mom[0].net_to_table(path=f"data(SCORE:{mom[1]}, ID:{mom[2]}).csv")
        return mom, dad

    def natural_selection(self):
        for snake in self.snakes:
            print(f"ID snake:{self.snakes.index(snake)}")
            self.learn_snake(snake, self.snakes.index(snake))

    def new_generation(self):
        mom, dad = self.best_snakes()
        self.all_snakes = []
        print(mom)
        mom, dad = mom[0], dad[0]
        child = mom.crossover(dad)
        child.net_to_table()
        snakes = []

        for i in range(self.size_population):
            new_snake = mom.crossover(dad)
            new_snake.mutate(self.mutation_rate)
            snakes.append(new_snake)

        self.snakes = [mom, dad]
        self.snakes += snakes

    def start_learning(self):
        for i in range(self.gens):
            self.natural_selection()
            self.new_generation()
        return 0


if __name__ == "__main__":
    # population = Population(size_population=2000, gens=3, moves=3000)
    population = Population(size_population=1000, gens=10, moves=500, load=True)
    population.start_learning()