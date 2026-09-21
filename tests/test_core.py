import tempfile
import unittest
from pathlib import Path

from aibpe.compare import compare_facts
from aibpe.events import Event, EventType
from aibpe.fingerprint import behavioral_fingerprint
from aibpe.intervention import Intervention, diff_paths
from aibpe.store import LocalStore
from aibpe.verify import verify_chain


class CoreTests(unittest.TestCase):
    def test_fingerprint_ignores_transport_volatility(self):
        a = {"model": {"name": "demo", "request_id": "one"}}
        b = {"model": {"name": "demo", "request_id": "two"}}
        self.assertEqual(behavioral_fingerprint(a), behavioral_fingerprint(b))

    def test_intervention_isolated_change(self):
        facts = {"retrieval": {"corpus": "v2"}, "model": {"name": "demo"}}
        changed = Intervention("retrieval.corpus", "v3").apply(facts)
        self.assertEqual(changed["retrieval"]["corpus"], "v3")
        self.assertEqual(facts["retrieval"]["corpus"], "v2")

    def test_compare_reports_nested_change(self):
        a = {"retrieval": {"corpus": "v2"}, "model": {"name": "demo"}}
        b = {"retrieval": {"corpus": "v3"}, "model": {"name": "demo"}}
        result = compare_facts(a, b)
        self.assertTrue(result.behavior_changed)
        self.assertEqual(result.changed_paths, ("retrieval.corpus",))

    def test_event_chain_verifies(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalStore(tmp)
            store.append(Event("r1", 1, EventType.RUN_STARTED, {"x": 1}))
            store.append(Event("r1", 2, EventType.RUN_COMPLETED, {"ok": True}))
            events = tuple(store.read("r1"))
            ok, message = verify_chain(events)
            self.assertTrue(ok, message)

    def test_diff_paths_detects_add_remove(self):
        self.assertEqual(diff_paths({"a": 1}, {"a": 1, "b": 2}), ["b"])


if __name__ == "__main__":
    unittest.main()
