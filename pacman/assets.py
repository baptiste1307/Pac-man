import pygame

FILES = {
    "vulnerable_ghost": "assets/ghosts/blue_ghost.png",
    "red_ghost": "assets/ghosts/blinky.png",
    "orange_ghost": "assets/ghosts/clyde.png",
    "blue_ghost": "assets/ghosts/inky.png",
    "pink_ghost": "assets/ghosts/pinky.png",
    "dot": "assets/other/dot.png",
    "pacman_down": {
        "opened": "assets/pacman-down/1.png",
        "half_opened": "assets/pacman-down/2.png",
        "closed": "assets/pacman-down/3.png",
    },
    "pacman_left": {
        "opened": "assets/pacman-left/1.png",
        "half_opened": "assets/pacman-left/2.png",
        "closed": "assets/pacman-left/3.png",
    },
    "pacman_right": {
        "opened": "assets/pacman-right/1.png",
        "half_opened": "assets/pacman-right/2.png",
        "closed": "assets/pacman-right/3.png",
    },
    "pacman_up": {
        "opened": "assets/pacman-up/1.png",
        "half_opened": "assets/pacman-up/2.png",
        "closed": "assets/pacman-up/3.png",
    },
}


class LoadedAssets:
    def __init__(self):
        # load every asset
        for name, value in FILES.items():

            if isinstance(value, str):
                setattr(self, name, pygame.image.load(value).convert_alpha())

            elif isinstance(value, dict):
                loaded_dict = {}

                for sub_name, path in value.items():
                    loaded_dict[sub_name] = pygame.image.load(
                        path
                    ).convert_alpha()

                setattr(self, name, loaded_dict)

    # rescale the corresponding asset to perfectly fit current maze, according
    # to its cell size
    def get_image(
        self,
        name: str,
        maze_cell_size: int,
        sub_name: str | None = None,
    ) -> pygame.Surface:

        asset = getattr(self, name)

        asset_size = maze_cell_size - 5
        dot_size = maze_cell_size

        # for pacgums only (small size)
        if isinstance(asset, pygame.Surface) and name == "dot":
            return pygame.transform.scale(asset, (dot_size, dot_size))

        # if asset only has one path
        if isinstance(asset, pygame.Surface):
            return pygame.transform.scale(asset, (asset_size, asset_size))

        # for asset pacman that has sub-pathes
        elif isinstance(asset, dict):

            if sub_name is None:
                raise ValueError(f"Asset '{name}' requires a sub_name.")

            # return all assets (open, half-open and closed)
            elif sub_name == "all":
                return [
                    pygame.transform.scale(asset[p], (asset_size, asset_size))
                    for p in asset
                ]

            # return only one sub_path given by sub_name
            else:
                return pygame.transform.scale(
                    asset[sub_name], (asset_size, asset_size)
                )

        # if no "name" attribute
        raise TypeError(f"Unsupported asset type for '{name}'.")
