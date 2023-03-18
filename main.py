import pygame
import time
from Snake_logic import Snake

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


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill((0, 155, 0))
    clock = pygame.time.Clock()
    snake = Snake(map_size=res)

    while not snake.is_lose():
        draw_board(screen, snake.map)
        event = pygame.event.poll()

        button_map = [['w', 'w', 'w', 'w', 'w', 'w', 'w', 'd'],
                      ['d', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
                      ['w', 'd', 'w', 'w', 'w', 'w', 'w', 'w'],
                      ['w', 'w', 'd', 'w', 'w', 'w', 'w', 'w'],
                      ['w', 'w', 'w', 'd', 'w', 'w', 'w', 'w'],
                      ['w', 'w', 'w', 'w', 'd', 'w', 'w', 'w'],
                      ['w', 'w', 'w', 'w', 'w', 'd', 'w', 'w'],
                      ['w', 'w', 'w', 'w', 'w', 'w', 'd', 'w']]
        move = {'w': (0, 1), 'd': (1, 0), 's': (0, -1), 'a': (-1, 0)}

        if snake.snake_cords() == snake.apple_cords():
            if snake.is_win():
                break
            snake.eat_apple()

        nx, ny = snake.snake_cords()
        movement = move[button_map[nx][ny]]
        x, y = movement
        snake.snake_move(x, y)
        time.sleep(0.02)
        if event.type == pygame.QUIT:
            pygame.quit()
        pygame.display.flip()
    print(f"Score:{snake.length_snake}\nSteps:{snake.steps}")

