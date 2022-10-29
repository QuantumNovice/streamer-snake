import pygame as pg
import time
import random
from enum import Enum
from flask import request, Flask
from threading import Thread

import toml

from const import *
from utils import *

config = toml.load("config.toml")

inp_buff = [None, 0]


class Dir(Enum):
    """direction vectors 

    Args:
        Enum (Tuple(xdir, ydir)): direction vector for each direction

    Returns:
        _type_: _description_
    """

    UP = (0, -10)
    DOWN = (0, 10)
    LEFT = (-10, 0)
    RIGHT = (10, 0)

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


def event_process(event_tree, inp_buff, game_over, dx, dy):
    """Process events from pygame.event.get()

    Args:
        event_tree (_type_): _description_
        inp_buff (_type_): _description_
        game_over (_type_): _description_
        dx (_type_): _description_
        dy (_type_): _description_

    Returns:
        _type_: _description_
    """
    for event in event_tree:
        if event.type == pg.QUIT:
            game_over = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                dx, dy = Dir.LEFT.value
            elif event.key == pg.K_RIGHT:
                dx, dy = Dir.RIGHT.value
            elif event.key == pg.K_UP:
                dx, dy = Dir.UP.value
            elif event.key == pg.K_DOWN:
                dx, dy = Dir.DOWN.value

    if inp_buff[0] is not None:
        if inp_buff[0] == "left":
            dx, dy = Dir.LEFT.value
        elif inp_buff[0] == "right":
            dx, dy = Dir.RIGHT.value
        if inp_buff[0] == "up":
            dx, dy = Dir.UP.value
        elif inp_buff[0] == "down":
            dx, dy = Dir.DOWN.value
    # dx, dy = random.choice(Dir.list())

    return dx, dy, game_over


def game(inp_buff) -> None:
    """main game loop

    Args:
        inp_buff (_type_): _description_
    """
    global wx, wy

    pg.init()
    surf = pg.display.set_mode((wx, wy))

    pg.display.update()
    pg.display.set_caption("Snake Game")

    x1 = wx / 2
    y1 = wy / 2

    snake_block:int = 10
    snake_speed:int = 30

    font_style = pg.font.SysFont("bahnschrift", 25)
    score_font = pg.font.SysFont("arial", 35)

    game_over = False
    dx = 0
    dy = 0

    foodx = round(random.randrange(0, wx - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, wy - snake_block) / 10.0) * 10.0

    snake_List = []
    Length_of_snake = 1

    clock = pg.time.Clock()
    while not game_over:

        dx, dy, game_over = event_process(pg.event.get(), inp_buff, game_over, dx, dy)

        # if x1 > wx or x1 < 0 or y1 > wy or y1 < 0:
        #    game_over = True

        if x1 > wx:
            x1 = 0
        elif x1 < 0:
            x1 = wx

        if y1 > wx:
            y1 = 0
        elif y1 < 0:
            y1 = wy

        x1 += dx
        y1 += dy
        surf.fill(black)

        pg.draw.rect(surf, red, [foodx, foody, snake_block, snake_block])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                # game_over = True
                score = 0
        our_snake(surf, snake_block, snake_List)
        print_score(surf, score_font, Length_of_snake - 1)
        inp_buff[1] = Length_of_snake - 1

        pg.draw.rect(surf, blue, [x1, y1, 10, 10])

        pg.display.update()

        if x1 == foodx and y1 == foody:
            print("Ate Fppd")
            foodx = round(random.randrange(0, wx - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, wy - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)
        # inp_buff[0] = None

    surf.fill(blue)
    message(surf, font_style, "You Lost", red)
    pg.display.update()
    time.sleep(2)
    pg.quit()
    quit()




app = Flask(__name__)


@app.route("/left")
def left():
    global inp_buff
    inp_buff[0] = "left"
    return "left"


@app.route("/right")
def right():
    global inp_buff
    inp_buff[0] = "right"
    return "right"


@app.route("/down")
def down():
    global inp_buff
    inp_buff[0] = "down"
    return "down"


@app.route("/up")
def up():
    global inp_buff
    inp_buff[0] = "up"
    return "up"


@app.route("/score")
def score():
    global inp_buff

    return str(inp_buff[1])






if __name__ == "__main__":

    Thread(target=game, args=(inp_buff,)).start()
    print("Done")


    app.run(host=config["host"], port=config["port"], debug=config["debug"])
