#!/usr/bin/env python3

"""
Peanuts Programming Language
1.0.2_r4
"""

import sys
from cli.main import main as cli_main


VERSION = "1.0_r3"


def print_banner():
    print(f"""
Peanuts v{VERSION}
A crunchy Python dialect.
Less serious. More nutty.

Type 'peanuts --help' if you're lost.
""")


def handle_version_flag(args):
    if "--version" in args or "-v" in args:
        print(f"Peanuts v{VERSION}, stay crunchy.")
        print("Copyright 2026 the Peanut authors.")
        print("Licensed under Apache License v2.0.")
        sys.exit(0)


def handle_help_flag(args):
    if "--help" in args or "-h" in args:
        print_banner()
        print("Commands:")
        print("  peanuts run <file.nut> [--warnings] [--debug] [--no-color]")
        print("  peanuts build <file.nut> [-o output.py]")
        print("  peanuts transpile <file.nut>")
        print("  peanuts pkg install <repo>")
        print("  peanuts pkg list")
        print("")
        print("Flags:")
        print("  --warnings   Enable static warnings")
        print("  --debug      Show debug execution timing")
        print("  --no-color   Disable colored output")
        print("  -o <file>    Output file for build command")
        print("")
        print("Example:")
        print("  peanuts run examples/hello.nut --warnings")
        sys.exit(0)


def main():
    args = sys.argv[1:]

    if not args:
        print_banner()
        return

    handle_version_flag(args)
    handle_help_flag(args)

    try:
        cli_main(args)

    except Exception as e:
        print("\n🥜 Fatal CLI Error")
        print(f"  {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()