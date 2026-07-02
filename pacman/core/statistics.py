#! /usr/bin/env python3

from dataclasses import dataclass
from typing import Any, Dict
import json


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
        self.scores_list: Dict[str, int] = {}

    # def load_score_json(self,
    #                     file_name: str, name: str, score: int):
    #     with open(file_name) as f:
    #         self.scores_list = json.load(f)
    #     if name in self.scores_list.keys():
    #         print("Player Name Already exited.")
    #         return
    #     self.scores_list[name] = score
    #     self.sorted_results = dict(sorted(self.scores_list.items(),
    #                                       key=lambda x: x[1], reverse=True))
    #     with open(file_name, "w") as f:
    #         json.dump(self.sorted_results, f)
