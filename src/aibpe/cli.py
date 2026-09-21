from __future__ import annotations

import argparse
import json
from pathlib import Path

from .events import Event, EventType
from .fingerprint import behavioral_fingerprint
from .store import LocalStore


def main() -> None:
    parser = argparse.ArgumentParser(prog="aibpe")
    sub = parser.add_subparsers(dest="command", required=True)

    record = sub.add_parser("record")
    record.add_argument("--store", default=".aibpe")
    record.add_argument("--run-id", default="demo")
    record.add_argument("--payload", default='{"model":"demo","prompt":"hello"}')

    inspect = sub.add_parser("inspect")
    inspect.add_argument("run_id")
    inspect.add_argument("--store", default=".aibpe")

    fp = sub.add_parser("fingerprint")
    fp.add_argument("json_file")

    args = parser.parse_args()

    if args.command == "record":
        store = LocalStore(args.store)
        store.append(
            Event(
                run_id=args.run_id,
                sequence=1,
                event_type=EventType.RUN_STARTED,
                payload=json.loads(args.payload),
            )
        )
        print(f"recorded {args.run_id}")

    elif args.command == "inspect":
        store = LocalStore(args.store)
        print(json.dumps(list(store.read(args.run_id)), indent=2))

    elif args.command == "fingerprint":
        print(behavioral_fingerprint(json.loads(Path(args.json_file).read_text(encoding="utf-8"))))


if __name__ == "__main__":
    main()
