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
        pacman_direction: str | None,
        state: GameState,
    ) -> bool:
        cell = maze[grid_y][grid_x]

        if state.status == "pause":
            return False

        if pacman_direction == "up":
            return not (cell & 1)
        if pacman_direction == "right":
            return not (cell & 2)
        if pacman_direction == "down":
            return not (cell & 4)
        if pacman_direction == "left":
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
            state.pacman_current_frame = (state.pacman_current_frame + 1) % 3
            state.ghost_current_frame = (state.ghost_current_frame + 1) % 2

    def update_wanted_direction(self, state: GameState) -> None:
        keys = pygame.key.get_pressed()

        is_arrow = 0

        if keys[pygame.K_LEFT]:
            state.pacman_wanted_direction = "left"
            is_arrow = 1
        elif keys[pygame.K_RIGHT]:
            state.pacman_wanted_direction = "right"
            is_arrow = 1

        elif keys[pygame.K_UP]:
            state.pacman_wanted_direction = "up"
            is_arrow = 1

        elif keys[pygame.K_DOWN]:
            state.pacman_wanted_direction = "down"
            is_arrow = 1

        if is_arrow == 1 and state.status == "pause":
            state.status = "play"

    def update_pacman_target(self, state: GameState) -> None:
        if state.status != "play" or state.pacman_wanted_direction is None:
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
            state.pacman_wanted_direction,
            state,
        ):
            # the "official" direction is now the wanted direction
            state.pacman_direction = state.pacman_wanted_direction

        elif not self.can_move(
            state.current_maze,
            state.pacman_grid_x,
            state.pacman_grid_y,
            state.pacman_direction,
            state,
        ):
            state.pacman_current_frame = 1
            return

        if state.pacman_direction == "up":
            state.pacman_grid_y -= 1
        elif state.pacman_direction == "right":
            state.pacman_grid_x += 1
        elif state.pacman_direction == "down":
            state.pacman_grid_y += 1
        elif state.pacman_direction == "left":
            state.pacman_grid_x -= 1

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

    def eat_touched_pacgums(self, state: GameState) -> None:
        pacman_size = state.level.cell_size - state.wall_thickness
        pacman_radius = pacman_size / 2
        pacman_center_x = state.pacman_x + pacman_radius
        pacman_center_y = state.pacman_y + pacman_radius
        eaten_pacgums = []

        # add two sets together
        pacgums_and_super_pacgums = state.pacgums | state.super_pacgums

        for x, y in pacgums_and_super_pacgums:
            pacgum_center_x = (
                state.MAZE_OFFSET_X
                + x * state.level.cell_size
                + state.wall_thickness
                + ((state.level.cell_size - state.wall_thickness) // 2)
            )
            pacgum_center_y = (
                state.MAZE_OFFSET_Y
                + y * state.level.cell_size
                + state.wall_thickness
                + ((state.level.cell_size - state.wall_thickness) // 2)
            )

            distance_x = pacgum_center_x - pacman_center_x
            distance_y = pacgum_center_y - pacman_center_y

            if distance_x**2 + distance_y**2 <= pacman_radius**2:
                eaten_pacgums.append((x, y))

        for pacgum in eaten_pacgums:
            if pacgum in state.pacgums:
                state.pacgums.remove(pacgum)
                state.statistics.score += state.config["points_per_pacgum"]
            elif pacgum in state.super_pacgums:
                state.super_pacgums.remove(pacgum)
                state.statistics.score += state.config[
                    "points_per_super_pacgum"
                ]

            self.sound_eat.play()

    def check_ghost_collisions(self, state: GameState) -> None:
        if state.status != "play":
            return

        entity_size = state.level.cell_size - state.wall_thickness
        pacman_rect = pygame.Rect(
            state.pacman_x,
            state.pacman_y,
            entity_size,
            entity_size,
        )

        for ghost in state.ghosts:
            ghost_rect = pygame.Rect(
                ghost.pixel_x,
                ghost.pixel_y,
                entity_size,
                entity_size,
            )

            if pacman_rect.colliderect(ghost_rect):
                self.handle_pacman_hit_by_ghost(state)
                return

    def handle_pacman_hit_by_ghost(self, state: GameState) -> None:
        state.statistics.lives -= 1

        if state.statistics.lives <= 0:
            state.status = "game_over"
            return

        state.set_pacman_start_position()
        state.reset_ghosts_states()
        state.status = "pause"

    def move_ghosts(self, state: GameState) -> None:
        if state.status != "play":
            return

        state.update_ghosts_targets()

        for ghost in [state.blinky, state.pinky, state.inky, state.clyde]:
            if ghost.pixel_x != ghost.pixel_target_x:
                if ghost.pixel_x < ghost.pixel_target_x:
                    ghost.pixel_x = min(
                        ghost.pixel_x + state.ghost_speed,
                        ghost.pixel_target_x,
                    )
                    ghost.direction = "right"

                elif ghost.pixel_x > ghost.pixel_target_x:
                    ghost.pixel_x = max(
                        ghost.pixel_x - state.ghost_speed,
                        ghost.pixel_target_x,
                    )
                    ghost.direction = "left"

            elif ghost.pixel_y != ghost.pixel_target_y:

                if ghost.pixel_y < ghost.pixel_target_y:
                    ghost.pixel_y = min(
                        ghost.pixel_y + state.ghost_speed,
                        ghost.pixel_target_y,
                    )
                    ghost.direction = "down"

                elif ghost.pixel_y > ghost.pixel_target_y:
                    ghost.pixel_y = max(
                        ghost.pixel_y - state.ghost_speed,
                        ghost.pixel_target_y,
                    )
                    ghost.direction = "up"
