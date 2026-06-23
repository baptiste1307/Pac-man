import pygame
from pacman.core import GameState


class EngineUtils:
    def can_move(
        self,
        maze: list[list[int]],
        grid_x: int,
        grid_y: int,
        direction: str,
    ) -> bool:
        cell = maze[grid_y][grid_x]

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
        state.current_level += 1

        if state.current_level >= len(state.levels):
            state.current_level = 0

        state.reset_level()

    def update_direction(self, state: GameState) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            state.direction = "left"
        elif keys[pygame.K_RIGHT]:
            state.direction = "right"
        elif keys[pygame.K_UP]:
            state.direction = "up"
        elif keys[pygame.K_DOWN]:
            state.direction = "down"

    def update_animation(self, state: GameState, dt: int) -> None:
        state.animation_timer += dt

        if state.animation_timer >= state.animation_delay:
            state.animation_timer = 0
            state.current_frame = (state.current_frame + 1) % 3

    def update_pacman_target(self, state: GameState) -> None:
        if (
            state.pacman_x != state.target_x
            or state.pacman_y != state.target_y
        ):
            return

        if not self.can_move(
            state.current_maze,
            state.pacman_grid_x,
            state.pacman_grid_y,
            state.direction,
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
            state.pacgums.remove(current_cell)
            state.statistics.score += state.config["points_per_pacgum"]

        state.update_target_position()

    def move_pacman(self, state: GameState) -> None:
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
