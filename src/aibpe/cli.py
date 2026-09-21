from __future__ import annotations

import argparse
import json
from pathlib import Path

from .compare import compare_facts
from .events import EventType
from .fingerprint import behavioral_fingerprint
from .intervention import Intervention
from .recorder import Recorder
from .replay import exact_replay
from .runtime import DeterministicAgent
from .store import LocalStore
from .verify import verify_chain

def main() -> None:
    parser = argparse.ArgumentParser(prog="aibpe", description="AI Behavioral Provenance Engine")
    sub = parser.add_subparsers(dest="command", required=True)

    record = sub.add_parser("record-demo")
    record.add_argument("--store", default=".aibpe")
    record.add_argument("--run-id", default="demo")
    record.add_argument("--corpus", default="docs-v1")

    inspect = sub.add_parser("inspect")
    inspect.add_argument("run_id")
    inspect.add_argument("--store", default=".aibpe")

    replay = sub.add_parser("replay")
    replay.add_argument("run_id")
    replay.add_argument("--store", default=".aibpe")

    verify = sub.add_parser("verify")
    verify.add_argument("run_id")
    verify.add_argument("--store", default=".aibpe")

    fp = sub.add_parser("fingerprint")
    fp.add_argument("json_file")

    compare = sub.add_parser("compare-json")
    compare.add_argument("baseline_json")
    compare.add_argument("candidate_json")

    intervene = sub.add_parser("intervene-demo")
    intervene.add_argument("--corpus", default="docs-v2")

    args = parser.parse_args()

    if args.command == "record-demo":
        state = {
            "model": {"name": "demo-llm", "temperature": 0.2},
            "prompt": {"template": "answer-v1"},
            "retrieval": {"corpus": args.corpus},
        }
        rec = Recorder(args.run_id, args.store)
        for key, value in state.items():
            rec.set_component(key, value)
        result = DeterministicAgent().run(state, rec)
        path = rec.save()
        print(json.dumps({"run_id": args.run_id, "path": str(path), "output": result.output}, indent=2))

    elif args.command == "inspect":
        print(json.dumps(list(LocalStore(args.store).read(args.run_id)), indent=2))

    elif args.command == "replay":
        print(json.dumps(exact_replay(args.store, args.run_id), indent=2))

    elif args.command == "verify":
        ok, message = verify_chain(LocalStore(args.store).read(args.run_id))
        print(json.dumps({"ok": ok, "message": message}, indent=2))
        raise SystemExit(0 if ok else 1)

    elif args.command == "fingerprint":
        print(behavioral_fingerprint(json.loads(Path(args.json_file).read_text(encoding="utf-8"))))

    elif args.command == "compare-json":
        left = json.loads(Path(args.baseline_json).read_text(encoding="utf-8"))
        right = json.loads(Path(args.candidate_json).read_text(encoding="utf-8"))
        result = compare_facts(left, right)
        print(json.dumps({
            "baseline_fingerprint": result.baseline_fingerprint,
            "candidate_fingerprint": result.candidate_fingerprint,
            "changed_paths": result.changed_paths,
            "behavior_changed": result.behavior_changed,
        }, indent=2))

    elif args.command == "intervene-demo":
        baseline = {
            "model": {"name": "demo-llm"},
            "prompt": {"template": "answer-v1"},
            "retrieval": {"corpus": "docs-v1"},
        }
        candidate = Intervention("retrieval.corpus", args.corpus).apply(baseline)
        result = compare_facts(baseline, candidate)
        print(json.dumps({
            "intervention": "retrieval.corpus",
            "replacement": args.corpus,
            "changed_paths": result.changed_paths,
            "fingerprints_differ": result.behavior_changed,
        }, indent=2))

if __name__ == "__main__":
    main()
