#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Any


@dataclass
class Statistics:
    config: dict[str, Any]
    score: int = 0
    lives: int = 3
    game_status: str = "HERO"  # HERO, INSTRUCTION, PLAY, NAME, SCORE
    # ghosts_pos: List[Tuple[int, int]]

    def __post_init__(self):
        self.level_max_time = self.config["level_max_time"]
        self.time_left = self.level_max_time
