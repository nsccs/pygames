import os
from pathlib import Path

import pygame
from pygame.image import load

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class ImageLoader:
    """Class that handles loading image assets for the game."""

    @staticmethod
    def load_sprite(path: str, with_alpha: bool = True) -> pygame.Surface:
        """Load sprite found from path and return the image."""
        loaded_sprite = load(Path(BASE_DIR) / path)
        if with_alpha:
            return loaded_sprite.convert_alpha()
        else:
            return loaded_sprite.convert()