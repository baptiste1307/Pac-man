import pygame

WALL_SPRITES_PATH = "img/wall_sprites"

WALL_SPRITE_NAMES = {
    "wall_empty": 0,
    "end_of_wall_south": 1,
    "end_of_wall_west": 2,
    "wall_corner_south_west": 3,
    "end_of_wall_north": 4,
    "vertical_wall": 5,
    "wall_corner_north_west": 6,
    "vertical_wall_with_right_corner": 7,
    "end_of_wall_east": 8,
    "wall_corner_south_east": 9,
    "horizontal_wall": 10,
    "horizontal_wall_with_up_corner": 11,
    "wall_corner_north_east": 12,
    "vertical_wall_with_left_corner": 13,
    "horizontal_wall_with_bottom_corner": 14,
    "horizontal_and_vertical_wall_crossed": 15,
}

WALL_SPRITE_SIZES = {
    "wall_empty": 0,
    "end_of_wall_south": 1,
    "end_of_wall_west": 2,
    "wall_corner_south_west": 3,
    "end_of_wall_north": 4,
    "vertical_wall": (0.2, 1),
    "wall_corner_north_west": 6,
    "vertical_wall_with_right_corner": 7,
    "end_of_wall_east": 8,
    "wall_corner_south_east": 9,
    "horizontal_wall": (1, 0.2),
    "horizontal_wall_with_up_corner": 11,
    "wall_corner_north_east": 12,
    "vertical_wall_with_left_corner": 13,
    "horizontal_wall_with_bottom_corner": 14,
    "horizontal_and_vertical_wall_crossed": 15,
}


class LoadedSprites:
    def __init__(self):
        for sprite_name, sprite_index in WALL_SPRITE_NAMES.items():
            sprite = pygame.image.load(
                f"{WALL_SPRITES_PATH}/wall_{sprite_index}.png"
            ).convert_alpha()
            setattr(self, sprite_name, sprite)

    # rescale the corresponding wall sprite to perfectly
    # fit current maze, according to its cell size
    def get_sprite(
        self,
        name: str,
        cell_size: int,
        thickness: int,
    ) -> pygame.Surface:

        sprite = getattr(self, name)

        if sprite:
            if name == "horizontal_wall":
                width = int(cell_size)
                height = thickness

            elif name == "vertical_wall":
                height = int(cell_size)
                width = thickness

            return pygame.transform.scale(
                sprite,
                (width, height),
            )

        # if no "name" attribute
        raise TypeError(f"Unsupported sprite name '{name}'.")
