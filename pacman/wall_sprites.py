import pygame

WALL_SPRITES_PATH = "img/wall_sprites"


class LoadedSprites:
    def __init__(self):
        self.by_mask = {}

        for sprite_index in range(0, 16):
            sprite = pygame.image.load(
                f"{WALL_SPRITES_PATH}/wall_{sprite_index}.png"
            ).convert_alpha()
            self.by_mask[sprite_index] = sprite

    # rescale the corresponding wall sprite to perfectly
    # fit current maze, according to its cell size
    def get_sprite_by_mask(
        self,
        mask_value: int,
        cell_size: int,
        thickness: int,
    ) -> pygame.Surface:

        sprite = self.by_mask.get(mask_value)

        if sprite:
            width, height = self.get_sprite_size(
                mask_value,
                cell_size,
                thickness,
            )

            return pygame.transform.scale(
                sprite,
                (width, height),
            )

        # if no "name" attribute
        raise TypeError(f"Unsupported mask value '{mask_value}'.")

    def get_sprite_size(
        self,
        mask_value: int,
        cell_size: int,
        thickness: int,
    ) -> tuple[int, int]:
        half_cell = cell_size / 2
        half_thickness = thickness / 2

        left = half_cell if mask_value & 8 else half_thickness
        right = half_cell if mask_value & 2 else half_thickness
        top = half_cell if mask_value & 1 else half_thickness
        bottom = half_cell if mask_value & 4 else half_thickness

        return (
            max(1, round(left + right)),
            max(1, round(top + bottom)),
        )
