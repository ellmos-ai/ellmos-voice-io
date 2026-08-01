"""Small inspection CLI; microphone actions stay in the library API."""

from __future__ import annotations

import argparse
import json

from .service import VoiceIO


def main() -> int:
    parser = argparse.ArgumentParser(prog="ellmos-voice-io")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("status", help="Report installed optional engines without starting them.")
    args = parser.parse_args()
    if args.command == "status":
        print(json.dumps(VoiceIO().status().as_dict(), indent=2, sort_keys=True))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
