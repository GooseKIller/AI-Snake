from random import randint, choice


class Snake:
    def __init__(self, map_size=8):
        self.map_size = map_size
        self.map = self.__empty_map()
        self.dx, self.dy = 0, 0  # move cords
        self.length_snake = 1
        self.steps = 0
        self.x, self.y = randint(0, self.map_size - 1), randint(0, self.map_size - 1)  # snake cords
        self.snake = [(self.x, self.y)]
        self.apple = choice(self.__empty_ceils())  # apple cords
        self.map[self.x][self.y] = "SS"  # snake
        self.map[self.apple[0]][self.apple[1]] = "AA"  # apple

    def snake_cords(self):
        return self.snake[-1]

    def apple_cords(self):
        return self.apple

    def look_direction(self, direction):
        def plus(arr, arr1):
            norm = lambda num: (self.map_size + num) % self.map_size
            for i in range(len(arr)):
                arr[i] = norm(arr[i] + arr1[i])
            return arr

        vision_direction = ['', 0]
        position = [self.x, self.y]
        distance = 1
        position = plus(position, direction)

        # move while we can
        while self.map[position[0]][position[1]] == '--':
            distance += 1
            position = plus(position, direction)

        object = self.map[position[0]][position[1]]
        object_id = {'SS': -1, '--': 0, 'AA': 1}
        vision_direction[0] = object_id[object]
        vision_direction[1] = 1 / distance
        return vision_direction



    def snake_vision(self):
        """
        find the type of object
        and return the type
        :return:
        """

        vision_distanse = []
        vision_object = []
        # up
        up = self.look_direction([-1, 0])
        vision_distanse += [up[1]]
        vision_object += [up[0]]

        # right up
        up_r = self.look_direction([-1, 1])
        vision_distanse += [up_r[1]]
        vision_object += [up_r[0]]

        # right
        right = self.look_direction([0, 1])
        vision_distanse += [right[1]]
        vision_object += [right[0]]

        # down right
        down_r = self.look_direction([+1, +1])
        vision_distanse += [down_r[1]]
        vision_object += [down_r[0]]

        # down
        down = self.look_direction([+1, 0])
        vision_distanse += [down[1]]
        vision_object += [down[0]]

        # down left
        down_l = self.look_direction([+1, -1])
        vision_distanse += [down_l[1]]
        vision_object += [down_l[0]]

        # left
        left = self.look_direction([0, -1])
        vision_distanse += [left[1]]
        vision_object += [left[0]]

        # left up
        up_l = self.look_direction([-1, -1])
        vision_distanse += [up_l[1]]
        vision_object += [up_l[0]]

        return vision_distanse + vision_object

    def update_units(self):
        """
        Updating units on map
        :return: None
        """
        self.map = self.__empty_map()
        self.map[self.apple[0]][self.apple[1]] = "AA"
        for x, y in self.snake:
            self.map[x][y] = "SS"

    def show_map(self):
        [print(*i) for i in self.map]
        return self.map

    def __empty_ceils(self):
        return [(x, y) for x in range(self.map_size) for y in range(self.map_size) if self.map[x][y] == '--']

    def __empty_map(self):
        return [[f"--" for _ in range(self.map_size)] for _ in range(self.map_size)]

    def eat_apple(self):
        self.apple = choice(self.__empty_ceils())
        self.length_snake += 1  # apple
        self.update_units()

    def __normalize(self):
        """
        normalizes x and y coordinates
        """
        self.x = (self.map_size + self.x) % self.map_size
        self.y = (self.map_size + self.y) % self.map_size

    def snake_move(self, dx=0, dy=0):
        self.x -= dy
        self.y += dx
        self.__normalize()
        self.dx, self.dy = dx, dy
        self.snake.append((self.x, self.y))
        self.snake = self.snake[-self.length_snake:]
        self.steps += 1
        self.update_units()

    def apple_move(self, dx=0, dy=0):
        def normalize_this(x, y):
            x = (self.map_size + x) % self.map_size
            y = (self.map_size + y) % self.map_size
            return x, y

        x, y = normalize_this(self.apple[0] - dx, self.apple[1] + dy)
        self.apple = (x, y)
        self.update_units()

    def is_lose(self):
        return len(set(self.snake)) != self.length_snake

    def is_win(self):
        return len(self.__empty_ceils()) == 0


if __name__ == "__main__":
    snake = Snake(map_size=8)

    snake.show_map()
    snake.snake_vision()
