import os
from pathlib import Path

import pygame
from pygame.image import load

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class ImageLoader:
    """Class that handles loading image assets for the game."""

    # __slots__ = 'base_dir'
    #
    # def __init__(self) -> None:
    #     """Init Image Loader with path to root of this game."""
    #     self.base_dir = Path(BASE_DIR)
    @staticmethod
    def load_sprite(path: str, with_alpha: bool = True) -> pygame.Surface:
        """Load sprite found from path and return the image."""
        loaded_sprite = load(Path(BASE_DIR) / path)
        if with_alpha:
            return loaded_sprite.convert_alpha()
        else:
            return loaded_sprite.convert()