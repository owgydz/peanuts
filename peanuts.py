#!/usr/bin/env python3

"""
Peanuts Programming Language 
1.0.r_3
"""

import sys
from cli.main import main as cli_main


VERSION = "1.0.r_3"


def print_banner():
    print(f"""
Peanuts v{VERSION}  
A crunchy Python dialect.
Less serious. More nutty.

Type 'peanuts --help' if you're lost.
""")


def handle_version_flag(args):
    if "--version" in args or "-v" in args:
        print(f"Peanuts v{VERSION}, stay crunchy")
        print(f"Copyright 2026 the Peanut authors.")
        print(f"This program uses the Apache license, v2.0. See the LICENSE file in the project root.")
        sys.exit(0)


def handle_help_flag(args):
    if "--help" in args or "-h" in args:
        print_banner()
        print("Commands:")
        print("  peanuts run <file.nut>        → Execute a nut file")
        print("  peanuts build <file.nut>      → Transpile to Python")
        print("  peanuts transpile <file.nut>  → Show generated Python")
        print("  peanuts pkg install <repo>    → Install a nut package")
        print("  peanuts pkg list              → List installed packages")
        print("")
        print("Example:")
        print("  peanuts run examples/hello.nut")
        sys.exit(0)


def main():
    args = sys.argv[1:]

    if not args:
        print_banner()
        return

    handle_version_flag(args)
    handle_help_flag(args)

    try:
        cli_main()
    except Exception as e:
        print(f"Uh oh... the peanut cracked:")
        print(f"   {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()