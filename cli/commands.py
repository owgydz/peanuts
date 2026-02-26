import sys
from .runner import run_file, build_file, transpile_file
from pkg.manager import PackageManager


def handle_command(args):
    if not args:
        print("Peanuts CLI")
        print("Usage:")
        print("  peanuts run file.nut")
        print("  peanuts build file.nut")
        print("  peanuts transpile file.nut")
        print("  peanuts pkg install owner/repo")
        print("  peanuts pkg list")
        return

    command = args[0]

    try:
        if command == "run":
            run_file(args[1])

        elif command == "build":
            filepath = args[1]
            build_file(filepath)

        elif command == "transpile":
            transpile_file(args[1])

        elif command == "pkg":
            manager = PackageManager()

            if args[1] == "install":
                manager.install(args[2])

            elif args[1] == "list":
                print(manager.list_installed())

            else:
                print("Unknown pkg command")

        else:
            print("Unknown command")

    except IndexError:
        print("Missing required arguments.")