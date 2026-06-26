import sys
from pacman.config import Parser
from pacman.engine import GameEngine
from pacman.errors import format_exception_error


def main() -> None:
    try:
        engine = GameEngine()
        parser = Parser()
        parser.parser_main(sys.argv)
        config = parser.__dict__
        engine.init_game(config)

    except Exception as e:
        print(format_exception_error(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
