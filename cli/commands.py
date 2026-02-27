import sys
from .runner import run_file, build_file, transpile_file
from pkg.manager import PackageManager


def handle_command(args):
    if not args:
        print("Peanuts CLI")
        return

    warnings_enabled = "--warnings" in args
    debug = "--debug" in args
    no_color = "--no-color" in args

    # Remove flags from args list
    args = [
        a for a in args
        if a not in ("--warnings", "--debug", "--no-color")
    ]

    from runtime.io import get_io
    io = get_io()

    if debug:
        io.enable_debug()

    if no_color:
        io.disable_colors()

    command = args[0]

    if command == "run":
        run_file(args[1], warnings_enabled)

    elif command == "build":
        output = "build.py"
        if "-o" in args:
            idx = args.index("-o")
            output = args[idx + 1]

        build_file(args[1], output)

    elif command == "transpile":
        transpile_file(args[1])

    elif command == "pkg":
        manager = PackageManager()
        if args[1] == "install":
            manager.install(args[2])
        elif args[1] == "list":
            print(manager.list_installed())
        elif args[1] == "remove":
            manager.remove(args[2])

    else:
        print("Unknown command")