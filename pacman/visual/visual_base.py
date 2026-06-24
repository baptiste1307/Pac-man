import pygame
from typing import Any, Tuple

from pacman.ui import Button, Colors


class VisualBaseMixin:
    def get_real_mouse_pos(
        self, mouse_pos: Tuple[int, int] | None = None
    ) -> Tuple[int, int]:
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()

        screen_mouse_x, screen_mouse_y = mouse_pos
        scale_x = self.screen_width / self.scaled_width
        scale_y = self.screen_height / self.scaled_height

        real_mouse_x = int(screen_mouse_x * scale_x)
        real_mouse_y = int(screen_mouse_y * scale_y)

        return tuple((real_mouse_x, real_mouse_y))

    def present(self) -> None:
        scaled_surface = pygame.transform.smoothscale(
            self.screen, (self.scaled_width, self.scaled_height)
        )
        self.scaled_screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    def draw_button(self, button: Button, button_font) -> None:
        mouse = self.get_real_mouse_pos()
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
                self.screen, Colors.CYAN.value, shade_rect, border_radius=40
            )
            pygame.draw.rect(
                self.screen,
                stroke_and_text_color,
                stroke_rect,
                border_radius=40,
            )

        elif hovered:
            pygame.draw.rect(
                self.screen,
                stroke_and_text_color,
                stroke_rect,
                border_radius=40,
            )

        pygame.draw.rect(
            self.screen, button_color, button_rect, border_radius=30
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
        if center:
            rect = to_draw_text.get_rect(center=pos)
            self.screen.blit(to_draw_text, rect)
        else:
            self.screen.blit(to_draw_text, pos)
