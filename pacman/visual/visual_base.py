import pygame
from typing import Any, Tuple

from pacman.ui import Button, Colors


class VisualBaseMixin:
    def x(self, value: int) -> int:
        return int(self.screen_width * (value / self.design_width))

    def y(self, value: int) -> int:
        return int(self.screen_height * (value / self.design_height))

    def pos(self, value: Tuple[int, int]) -> Tuple[int, int]:
        return self.x(value[0]), self.y(value[1])

    def size(self, value: Tuple[int, int]) -> Tuple[int, int]:
        return self.x(value[0]), self.y(value[1])

    def rect(
        self, value: Tuple[int, int, int, int]
    ) -> Tuple[int, int, int, int]:
        return (
            self.x(value[0]),
            self.y(value[1]),
            self.x(value[2]),
            self.y(value[3]),
        )

    def radius(self, value: int) -> int:
        return max(
            1,
            int(
                value
                * min(
                    self.screen_width / self.design_width,
                    self.screen_height / self.design_height,
                )
            ),
        )

    def present(self) -> None:
        pygame.display.flip()

    def draw_button(self, button: Button, button_font) -> None:
        mouse = pygame.mouse.get_pos()
        stroke_rect = (
            button.rect_pos_x,
            button.rect_pos_y,
            button.rect_width,
            button.rect_height,
        )
        button_rect = (
            button.rect_pos_x + button.stroke_thickness,
            button.rect_pos_y + button.stroke_thickness,
            button.rect_width - 2 * button.stroke_thickness,
            button.rect_height - 2 * button.stroke_thickness,
        )
        shade_rect = (
            button.rect_pos_x,
            button.rect_pos_y + button.stroke_thickness,
            button.rect_width,
            button.rect_height,
        )

        hovered = pygame.Rect(stroke_rect).collidepoint(mouse)

        button_color = Colors.D_BLUE.value
        stroke_and_text_color = (
            Colors.CYAN.value if hovered else Colors.B_YELLOW.value
        )
        texto = button_font.render(button.text, True, stroke_and_text_color)

        if not hovered:
            pygame.draw.rect(
                self.screen,
                Colors.CYAN.value,
                shade_rect,
                border_radius=self.radius(40),
            )
            pygame.draw.rect(
                self.screen,
                stroke_and_text_color,
                stroke_rect,
                border_radius=self.radius(40),
            )

        elif hovered:
            pygame.draw.rect(
                self.screen,
                stroke_and_text_color,
                stroke_rect,
                border_radius=self.radius(40),
            )

        pygame.draw.rect(
            self.screen,
            button_color,
            button_rect,
            border_radius=self.radius(30),
        )

        if hovered:
            self.screen.blit(
                texto, (button.text_rect[0], button.text_rect[1] + 5)
            )
        elif not hovered:
            self.screen.blit(texto, button.text_rect)

    def draw_text(
        self,
        text: str,
        font: Any,
        color: Tuple[int, int, int],
        pos: Tuple[int, int],
        center=False,
    ) -> None:
        """
        Draw text on the screen.

        Args:
            text: the text content to draw.
            font: the desired text font.
            color: the desired text color.
            pos: the position to draw the text.
            center: if the text is center-positioned (or topleft).
        """
        to_draw_text = font.render(text, True, color)
        scaled_pos = self.pos(pos)
        if center:
            rect = to_draw_text.get_rect(center=scaled_pos)
            self.screen.blit(to_draw_text, rect)
        else:
            self.screen.blit(to_draw_text, scaled_pos)
