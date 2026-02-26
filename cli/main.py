import sys
from .commands import handle_command


def main():
    handle_command(sys.argv[1:])


if __name__ == "__main__":
    main()