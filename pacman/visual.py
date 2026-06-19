import pygame
from typing import Any
from mazegenerator.mazegenerator import MazeGenerator

MAZE_OFFSET_X = 25
MAZE_OFFSET_Y = 125


class Visual:
    def __init__(self):
        self.screen_width = 2160
        self.screen_height = 1280
        self.screen = pygame.display.set_mode((self.screen_width,
                                               self.screen_height))

    def draw_stats(self, config: dict[str, Any], current_level: int,
                   colors: dict[str, str]) -> None:

        font = pygame.font.SysFont("arial", 24)
        stats_x = 25
        stats_y = 5

        game_score = 0

        score_text = font.render(f"Score: {game_score}", True, colors["white"])

        lives_text = font.render(
            f"Lives: {config['lives']}", True, colors["white"]
        )

        level_text = font.render(
            f"Level: {current_level + 1}", True, colors["white"]
        )

        time_text = font.render(
            f"Time: {config['level_max_time']}", True, colors["white"]
        )

        self.screen.blit(score_text, (stats_x, stats_y + 20))
        self.screen.blit(lives_text, (stats_x, stats_y + 40))
        self.screen.blit(level_text, (stats_x, stats_y + 60))
        self.screen.blit(time_text, (stats_x, stats_y + 80))

    # DEBUG (to delete)
    def draw_next_button(self, colors: dict[str, Any]) -> pygame.Rect:

        font = pygame.font.SysFont("arial", 24)

        button_width = 120
        button_height = 50

        button_x = self.screen.get_width() - button_width - 20
        button_y = 40

        button_rect = pygame.Rect(button_x, button_y,
                                  button_width, button_height)

        pygame.draw.rect(self.screen, colors["yellow"], button_rect)

        text = font.render("NEXT", True, colors["black"])

        self.screen.blit(
            text,
            (
                button_rect.centerx - text.get_width() // 2,
                button_rect.centery - text.get_height() // 2,
            ),
        )

        return button_rect

    def draw_maze(self, maze: list[list[int]], cell_size: int,
                  colors: dict[str, Any]) -> None:

        # def has_south_and_east_walls(x: int, y: int) -> bool:
        #     return ((maze[y][x] & 4) and (maze[y][x] & 2))

        # def has_south_and_west_walls(x: int, y: int) -> bool:
        #     return ((maze[y][x] & 4) and (maze[y][x] & 8))

        # def has_north_and_east_wall(x: int, y: int) -> bool:
        #     return ((maze[y][x] & 1) and (maze[y][x] & 2))

        # def has_north_and_west_wall(x: int, y: int) -> bool:
        #     return ((maze[y][x] & 1) and (maze[y][x] & 8))

        rows = len(maze)
        cols = len(maze[0])

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):

                px = MAZE_OFFSET_X + x * cell_size
                py = MAZE_OFFSET_Y + y * cell_size

                # top wall
                if cell & 1:
                    pygame.draw.line(
                        self.screen,
                        colors["wall_blue"],
                        (px, py),
                        (px + cell_size, py),
                        5,
                    )

                # left wall
                if cell & 8:
                    pygame.draw.line(
                        self.screen,
                        colors["wall_blue"],
                        (px, py),
                        (px, py + cell_size),
                        5,
                    )

                # right wall (last column)
                if x == (cols - 1) and (cell & 2):
                    pygame.draw.line(
                        self.screen,
                        colors["wall_blue"],
                        (px + cell_size, py),
                        (px + cell_size, py + cell_size),
                        5,
                    )

                # bottom wall (last row)
                if y == rows - 1 and (cell & 4):
                    pygame.draw.line(
                        self.screen,
                        colors["wall_blue"],
                        (px, py + cell_size),
                        (px + cell_size, py + cell_size),
                        5,
                    )

                # if x < cols - 1 and y < cols - 1:
                #     # if there's a part of the maze without walls
                #     if (not has_south_and_east_walls(x, y)
                #         and not has_south_and_west_walls(x + 1, y)
                #         and not has_north_and_east_wall(x, y + 1)
                #             and not has_north_and_west_wall(x + 1, y)):
                #         pygame.draw.line(
                #             screen, colors["wall_blue"],
                #             (px + cell_size, py + cell_size),
                #             (px + cell_size + 5, py + cell_size), 5)

    def main_menu(self, colors: dict[str, Any]) -> None:
        font = pygame.font.SysFont("arial", 48)
        small_font = pygame.font.SysFont("arial", 24)

        running = True

        while running:
            self.screen.fill(colors["black"])

            # create only an image with the text
            title_text = font.render("PAC-MAN", True, colors["yellow"])
            # "true" to have a not-pixelized text
            start_text = small_font.render(
                "Press SPACE to start", True, colors["white"]
            )
            quit_text = small_font.render(
                "Press ESC to quit", True, colors["white"]
            )

            # ".blit()" = put thoses images on screen
            self.screen.blit(
                title_text,
                (
                    # to center the text image (x coord), 150 = y coord
                    self.screen.get_width() // 2 - title_text.get_width() // 2,
                    150,
                ),
            )
            self.screen.blit(
                start_text,
                (self.screen.get_width() // 2 - start_text.get_width() // 2, 300),
            )
            self.screen.blit(
                quit_text,
                (self.screen.get_width() // 2 - quit_text.get_width() // 2, 350),
            )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

    def _find_cell_size(self, width: int, height: int) -> int:

        pygame.init()
        info = pygame.display.Info()

        cell_size = min(
            (info.current_w * 0.7) // width, (info.current_h * 0.7) // height
        )
        return cell_size

    def init_game(self, config: dict[str, Any]) -> None:

        # 1,2,4,8 = north, east, south, west
        colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "yellow": (255, 255, 0),
            "wall_blue": (25, 25, 166),
            "ultramarine": (33, 33, 222),
            "peach": (222, 161, 133),
            "red": (253, 0, 0),
            "green": (0, 255, 0),
        }

        mazes: list[dict[str, Any]] = []
        for index, level in enumerate(config["levels"]):
            mazes.append({})
            level_height = level["height"]
            level_width = level["width"]
            new_level_maze = MazeGenerator(size=(level_height, level_width))
            mazes[index]["maze"] = new_level_maze
            cell_size = self._find_cell_size(level_width, level_height)
            mazes[index]["cell_size"] = cell_size
            mazes[index]["height"] = level_height
            mazes[index]["width"] = level_width

        pygame.init()

        width = mazes[0]["width"] * mazes[0]["cell_size"] + 50
        height = mazes[0]["height"] * mazes[0]["cell_size"] + 150

        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pac-Man")

        self.main_menu(screen, colors)
        current_level = 0

        clock = pygame.time.Clock()  # create an intern timer for the game
        # to limit FPS
        running = True

        while running:
            next_button = self.draw_next_button(screen, colors)

            # get all the events(mouse click, key press, close window etc)
            for event in pygame.event.get():
                # if event = close window
                if event.type == pygame.QUIT:
                    running = False

                # if event = mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if next_button.collidepoint(mouse_pos):
                        current_level += 1

                        if current_level >= len(mazes):
                            current_level = 0

                        width = (
                            mazes[current_level]["width"]
                            * mazes[current_level]["cell_size"]
                            + 50
                        )

                        height = (
                            mazes[current_level]["height"]
                            * mazes[current_level]["cell_size"]
                            + 150
                        )

                        screen = pygame.display.set_mode((width, height))

            # cleaning screen at each frame
            screen.fill(colors["black"])

            self.draw_stats(screen, config, current_level, colors)

            # generating the drawing of the maze at each frame
            self.draw_maze(
                screen,
                mazes[current_level]["maze"].maze,
                mazes[current_level]["cell_size"],
                colors,
            )
            next_button = self.draw_next_button(screen, colors)

            # displays it on the screen. "display" draws on a "hidden" zone,
            # and "flip" copy it to the real screen to make it visible
            pygame.display.flip()
            # max FPS for the game = 60FPS
            clock.tick(60)

        # cleanly close the windows and free window, memory
        # and graphical ressources
        pygame.quit()
