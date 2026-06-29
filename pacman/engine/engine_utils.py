import pygame
from pacman.core import GameState


class EngineUtils:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.sound_eat = pygame.mixer.Sound("./sounds/sound_eat.mp3")
        self.sound_eat.set_volume(0.4)

    def can_move(
        self,
        maze: list[list[int]],
        grid_x: int,
        grid_y: int,
        direction: str | None,
        state: GameState,
    ) -> bool:
        cell = maze[grid_y][grid_x]

        if state.status == "pause":
            return False

        if direction == "up":
            return not (cell & 1)
        if direction == "right":
            return not (cell & 2)
        if direction == "down":
            return not (cell & 4)
        if direction == "left":
            return not (cell & 8)

        return False

    def next_level(self, state: GameState) -> None:
        state.current_level_index += 1

        if state.current_level_index >= len(state.config["levels"]):
            state.current_level_index = 0

        state.reset_level()

    def update_animation(self, state: GameState, dt: int) -> None:
        if state.status != "play":
            return
        state.animation_timer += dt

        if state.animation_timer >= state.animation_delay:
            state.animation_timer = 0
            state.current_frame = (state.current_frame + 1) % 3

    def update_wanted_direction(self, state: GameState) -> None:
        keys = pygame.key.get_pressed()

        is_arrow = 0

        if keys[pygame.K_LEFT]:
            state.wanted_direction = "left"
            is_arrow = 1
        elif keys[pygame.K_RIGHT]:
            state.wanted_direction = "right"
            is_arrow = 1

        elif keys[pygame.K_UP]:
            state.wanted_direction = "up"
            is_arrow = 1

        elif keys[pygame.K_DOWN]:
            state.wanted_direction = "down"
            is_arrow = 1

        if is_arrow == 1 and state.status == "pause":
            state.status = "play"

    def update_pacman_target(self, state: GameState) -> None:
        if state.status != "play" or state.wanted_direction is None:
            return

        if (
            state.pacman_x != state.target_x
            or state.pacman_y != state.target_y
        ):
            return

        # if pacman can move in the direction the player want
        if self.can_move(
            state.current_maze,
            state.pacman_grid_x,
            state.pacman_grid_y,
            state.wanted_direction,
            state,
        ):
            # the "official" direction is now the wanted direction
            state.direction = state.wanted_direction

        elif not self.can_move(
            state.current_maze,
            state.pacman_grid_x,
            state.pacman_grid_y,
            state.direction,
            state,
        ):
            state.current_frame = 1
            return

        if state.direction == "up":
            state.pacman_grid_y -= 1
        elif state.direction == "right":
            state.pacman_grid_x += 1
        elif state.direction == "down":
            state.pacman_grid_y += 1
        elif state.direction == "left":
            state.pacman_grid_x -= 1

        current_cell = (state.pacman_grid_x, state.pacman_grid_y)

        if current_cell in state.pacgums:
            self.sound_eat.play()
            state.pacgums.remove(current_cell)
            state.statistics.score += state.config["points_per_pacgum"]

        state.update_target_position()

    def move_pacman(self, state: GameState) -> None:
        if state.status != "play":
            return
        if state.pacman_x < state.target_x:
            state.pacman_x = min(
                state.pacman_x + state.pacman_speed,
                state.target_x,
            )
        elif state.pacman_x > state.target_x:
            state.pacman_x = max(
                state.pacman_x - state.pacman_speed,
                state.target_x,
            )

        if state.pacman_y < state.target_y:
            state.pacman_y = min(
                state.pacman_y + state.pacman_speed,
                state.target_y,
            )
        elif state.pacman_y > state.target_y:
            state.pacman_y = max(
                state.pacman_y - state.pacman_speed,
                state.target_y,
            )
