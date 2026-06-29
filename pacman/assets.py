import pygame

GHOSTS = {
    "vulnerable_ghost": "vulnerable",
    "red_ghost": "blinky",
    "orange_ghost": "clyde",
    "blue_ghost": "inky",
    "pink_ghost": "pinky",
}

LEGACY_GHOST_FILES = {
    "vulnerable_ghost": "assets/ghosts/blue_ghost.png",
    "red_ghost": "assets/ghosts/blinky.png",
    "orange_ghost": "assets/ghosts/clyde.png",
    "blue_ghost": "assets/ghosts/inky.png",
    "pink_ghost": "assets/ghosts/pinky.png",
}

ANIMATED_GHOST_FILES = {
    f"{name}_{direction}": {
        f"frame_{frame}": f"assets/ghosts/{folder}/{direction}/{frame}.png"
        for frame in range(1, 3)
    }
    for name, folder in GHOSTS.items()
    for direction in ("up", "down", "left", "right")
}

PACMAN_FILES = {
    f"pacman_{direction}": {
        "opened": f"assets/pacman-{direction}/1.png",
        "half_opened": f"assets/pacman-{direction}/2.png",
        "closed": f"assets/pacman-{direction}/3.png",
    }
    for direction in ("down", "left", "right", "up")
}

FILES = {
    **LEGACY_GHOST_FILES,
    **ANIMATED_GHOST_FILES,
    "dot": "assets/other/dot.png",
    **PACMAN_FILES,
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
        cell_size: int,
        thickness: int | None = None,
        sub_name: str | None = None,
    ) -> pygame.Surface:

        asset = getattr(self, name)

        dot_size = max(1, int(cell_size * 0.8))

        # for pacman and ghosts
        if thickness:
            asset_size = max(1, int(cell_size - thickness))

        # for pacgums only (small size)
        if isinstance(asset, pygame.Surface) and name == "dot":
            return pygame.transform.scale(asset, (dot_size, dot_size))

        # if asset only has one path
        elif isinstance(asset, pygame.Surface):
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
