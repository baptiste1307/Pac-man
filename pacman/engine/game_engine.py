#! /usr/bin/env python3

import pygame
from pacman.core import GameState
from pacman.visual import GameVisual
from .engine_utils import EngineUtils
from typing import Any


class GameEngine:
    def __init__(self):
        self.dragging = False

    def handle_events(
        self, game: GameVisual, state: GameState, utils: EngineUtils
    ) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                next_button_rect = pygame.Rect(game.next_level_button.rect)
                if next_button_rect.collidepoint(mouse_pos):
                    utils.next_level(state)

                if pygame.Rect(game.play_back_button.rect).collidepoint(
                    mouse_pos
                ):
                    state.current_level_index = 0
                    state.reset_level()
                    game.main_menu()

                if game.track_rect.collidepoint(mouse_pos):
                    self.dragging = True

            if event.type == pygame.VIDEORESIZE:
                game.resize(event.w, event.h)
                state.refresh_layout()

            if event.type == pygame.MOUSEMOTION and self.dragging:
                mx, my = event.pos
                if mx <= game.knob_x_right and mx >= game.knob_x_left:
                    game.volume = 1 - (game.knob_x_right - mx) / (
                        game.knob_x_right - game.knob_x_left
                    )
                    pygame.mixer.music.set_volume(game.volume)
                    game.knob_x = mx
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

        return True

    def render(
        self,
        game: GameVisual,
        state: GameState,
    ) -> None:

        game.draw_maze(state)
        game.draw_pacman(state)
        game.draw_pacgums(state)
        game.draw_ghosts(state)
        if state.status == "game_over":
            game.draw_game_over()
        game.present()

    def init_game(self, config: dict[str, Any]) -> bool:
        game = GameVisual()
        game.main_menu()

        pygame.init()
        pygame.display.set_caption("Pac-Man")

        state = GameState(config=config, game=game)

        utils = EngineUtils()
        clock = pygame.time.Clock()
        running = True

        while running:
            dt = clock.tick(60)
            # state.level_timer += dt
            running = self.handle_events(game, state, utils)

            if state.status != "game_over":
                # when 1 sec passed
                state.level_timer += dt
                if state.level_timer >= 1000:
                    state.level_timer = 0
                    state.statistics.time_left -= 1
                    if state.statistics.time_left <= 0:
                        # lose a life
                        state.statistics.lives -= 1
                        # reset timer
                        state.statistics.time_left = (
                            state.statistics.level_max_time
                        )
                        # reset the same level if pacman still have lives
                        if state.statistics.lives > 0:
                            state.reset_level()
                        # if lives <= 0: handle game over
                        elif state.statistics.lives <= 0:
                            state.status = "game_over"

                utils.update_animation(state, dt)
                utils.update_wanted_direction(state)
                utils.update_pacman_target(state)
                utils.move_pacman(state)

            game.draw_play(state)
            utils.update_animation(state, dt)
            utils.update_wanted_direction(state)
            utils.update_pacman_target(state)
            utils.move_pacman(state)
            utils.eat_touched_pacgums(state)
            utils.move_ghosts(state)
            utils.check_ghost_collisions(state)

            self.render(game, state)

        game.main_menu()

        pygame.quit()
