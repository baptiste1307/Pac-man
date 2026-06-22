#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Tuple


@dataclass
class GameStats:
    score: int = 0
    lives: int = 3
    level_time_left: int = 60
    game_status: str = "HERO"  # HERO, INSTRUCTION, PLAY, NAME, SCORE
    pacman_pos: Tuple[int, int] = (1, 1)
    # ghosts_pos: List[Tuple[int, int]]
