import pygame as pg
from const import *


def message(surf, font_style, msg, color) -> None:
    global wx, wy
    mesg = font_style.render(msg, True, color)
    surf.blit(mesg, [wx / 2, wy / 2])


def our_snake(surf, snake_block, snake_list) -> None:
    for x in snake_list:
        pg.draw.rect(surf, red, [x[0], x[1], snake_block, snake_block])


def print_score(surf, score_font, score) -> None:
    value = score_font.render("Your Score: " + str(score), True, yellow)
    surf.blit(value, [0, 0])
