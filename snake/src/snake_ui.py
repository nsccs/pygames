import pygame as pg

pg.font.init()


def draw_text(
    content: str,
    screen,
    color: tuple[int, int, int],
    position: tuple[int, int],
    font_name: str,
    font_size: int
):
    font = pg.font.SysFont(font_name, font_size)
    score_text = font.render(content, True, color)
    screen.blit(score_text, position)
