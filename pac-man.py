import sys
import argparse
from pathlib import Path
from pacman.parsing import Parser
from pacman.visual import Visual


def main() -> None:
    try:
        visual = Visual()
        parser = Parser()
        parser.parser_main(sys.argv)
        # print(parser.lives)

        # args: argparse.Namespace = parse_input(sys.argv)
        # config_file_path = Path(args.config_file)
        # config = load_json_with_comments(config_file_path)
        # check_json(config_file_path, config)

        # debug
        # print("\n".join(f"{key}: {value}" for key, value in config.items()))
        config = parser.__dict__
        visual.init_game(config)


    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
