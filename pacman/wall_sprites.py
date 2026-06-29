import pygame
from pacman.ui.colors import Colors


class Sprites:

    def __init__(self):
        self.sprite_cache = {}

    def get_sprite_by_mask(
        self,
        mask: int,
        cell_size: int,
        thickness: int,
    ) -> pygame.Surface:

        cache_key = (mask, cell_size, thickness)

        if cache_key not in self.sprite_cache:
            self.sprite_cache[cache_key] = self.draw_wall_sprite(
                mask, cell_size, thickness
            )

        return self.sprite_cache[cache_key]

    def draw_wall_sprite(
        self, mask, cell_size, thickness
    ) -> tuple[pygame.Surface, tuple[int, int]]:
        blue_border_thickness = max(1, int(thickness * 0.15))
        inner_thickness = thickness - (blue_border_thickness * 2)

        surface, (origin_x, origin_y) = self.build_surface(
            mask, cell_size, thickness
        )

        # first blue layer
        self.draw_layer(
            surface,
            origin_x,
            origin_y,
            mask,
            thickness,
            Colors.WALL_BLUE.value,
        )
        if inner_thickness > 0 and inner_thickness < thickness:
            # second black layer, a little less thick
            self.draw_layer(
                surface,
                origin_x,
                origin_y,
                mask,
                inner_thickness,
                Colors.BLACK.value,
            )

        return (surface, (origin_x, origin_y))

    def build_surface(
        self, mask, cell_size, thickness
    ) -> tuple[pygame.Surface, tuple[int, int]]:
        left, right, top, bottom = self.get_sprite_dimensions(
            mask, cell_size, thickness
        )

        width = left + right
        height = top + bottom

        # pygame.SRCALPHA: activates transparency
        # returns the surface and its origin coords
        return (pygame.Surface((width, height), pygame.SRCALPHA), (left, top))

    # return how much the intersection exceeds its central point in
    # each direction
    def get_sprite_dimensions(
        self,
        mask: int,
        cell_size: int,
        thickness: int,
    ) -> tuple[int, int, int, int]:
        half_cell = cell_size // 2
        other_half_cell = cell_size - half_cell
        half_thickness = thickness // 2
        other_half_thickness = thickness - half_thickness

        left = half_cell if mask & 8 else half_thickness
        right = other_half_cell if mask & 2 else other_half_thickness
        top = half_cell if mask & 1 else half_thickness
        bottom = other_half_cell if mask & 4 else other_half_thickness

        return left, right, top, bottom

    def draw_layer(
        self, surface, origin_x, origin_y, mask, thickness, color
    ) -> None:

        half = thickness // 2
        width, height = surface.get_size()

        if mask & 1:
            pygame.draw.rect(
                surface,
                color,
                (origin_x - half, 0, thickness, origin_y),
            )

        if mask & 2:
            pygame.draw.rect(
                surface,
                color,
                (origin_x, origin_y - half, width - origin_x, thickness),
            )

        if mask & 4:
            pygame.draw.rect(
                surface,
                color,
                (origin_x - half, origin_y, thickness, height - origin_y),
            )

        if mask & 8:
            pygame.draw.rect(
                surface, color, (0, origin_y - half, origin_x, thickness)
            )

        # for round edges
        pygame.draw.circle(surface, color, (origin_x, origin_y), half)
