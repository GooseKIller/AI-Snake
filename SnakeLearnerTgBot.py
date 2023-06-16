import telebot
import torch

from SnakeNNet import SnakeNNet
from Snake_logic import Snake


def draw_board(snake_map):
    answer_map = ""
    colors = ["🟨", "🟩"]
    size = len(snake_map)
    for r in range(size):
        for c in range(len(snake_map[r])):
            color = colors[(r + c) % 2]
            unit = snake_map[r][c]
            units = {"--": color, "SS": "⬛", "AA": "🟥"}
            answer_map += units[unit]
        answer_map += "\n"
    return answer_map


def max_index(arr):
    max_val = max(arr)
    move_index = arr.index(max_val)
    return move_index


bot = telebot.TeleBot('')  # Telegram API

model = SnakeNNet()
criterion = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

snake = Snake(10)

learning = False


@bot.message_handler(commands=['snk'])
def snake_game(message):
    global learning
    global model
    global snake
    text_message: str = message.text.replace("/snk", '').strip()
    if text_message == "save":
        torch.save(model.state_dict(), 'model.pth')
        bot.send_message(message.chat.id, "Saved.")
    elif text_message == "load":
        model.load_state_dict(torch.load("model.pth"))
        bot.send_message(message.chat.id, "Loaded.")
    elif "start" in text_message:
        learning = True
        if len(text_message.split()) == 1:
            snake = Snake(10)
        elif len(text_message.split()) == 2:
            snake = Snake(int(text_message.split()[1]))
        bot.send_message(message.chat.id, "Started.")
        bot.send_message(message.chat.id, draw_board(snake.map))
    elif text_message == "end":
        learning = False
        bot.send_message(message.chat.id, "Ended.")


# ^ - say NNet to move up
# ^^ - say NNet to move up and snake move up
# > - say NNet to move right
# >> - say NNet to move right and snake move right
# v - say NNet to move down
# vv - say NNet to move down and snake move down
# < - say NNet to move left
# << - say NNet to move left and snake move right left
# s - support the neural network solution
# sk.+ (<-regex)- correlation of weights does not occur
@bot.message_handler(content_types=["text"])
def repeat(message):
    text_message: str = message.text.lower()

    if len(set(text_message) & set('<^>vsk')) != 0 and learning:
        answers = {
            "^": torch.tensor([0.8, 0.2, 0.2, 0.2], dtype=torch.float32),
            ">": torch.tensor([0.2, 0.8, 0.2, 0.2], dtype=torch.float32),
            "v": torch.tensor([0.2, 0.2, 0.8, 0.2], dtype=torch.float32),
            "<": torch.tensor([0.2, 0.2, 0.2, 0.8], dtype=torch.float32)
        }
        move = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        move_emoji = ["⬆️", "➡️", "⬇️", "⬅️"]
        snake_info = torch.tensor(snake.snake_vision(), dtype=torch.float32)
        output = model(snake_info)

        target = answers[text_message[0]] if text_message[0] != 's' else tuple(answers.values())[
            max_index(output.tolist())]

        if len(text_message) == 2:
            move = {"^": (0, 1), ">": (1, 0), "v": (0, -1), "<": (-1, 0)}
            dx, dy = move[text_message[0]]
        else:
            dx, dy = move[max_index(output.tolist())]

        if snake.snake_cords() == snake.apple_cords():
            snake.eat_apple()

        snake.snake_move(dx, dy)

        if 'k' not in text_message:
            loss = criterion(output, target)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        snake_info = torch.tensor(snake.snake_vision(), dtype=torch.float32)
        bot.send_message(message.chat.id, str(snake.snake_cords()) + f"\n{output.tolist()}\n" + draw_board(
            snake.map) + f"\nNext:{move_emoji[max_index(model(snake_info).tolist())]}")
