import tempfile
import unittest

from aibpe.artifacts import ContentAddressedStore
from aibpe.provenance import graph_from_events
from aibpe.recorder import Recorder
from aibpe.redaction import redact
from aibpe.runtime import DeterministicAgent
from aibpe.trajectory import compare_trajectories

class AdvancedTests(unittest.TestCase):
    def test_content_addressed_store_is_stable(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = ContentAddressedStore(tmp)
            a = store.put("prompt", {"x": 1})
            b = store.put("prompt", {"x": 1})
            self.assertEqual(a.sha256, b.sha256)
            self.assertEqual(store.get(a.sha256), b'{"x":1}')

    def test_provenance_graph_from_events(self):
        rec = Recorder("r", tempfile.mkdtemp())
        DeterministicAgent().run({"prompt": {"template": "v1"}, "retrieval": {"corpus": "c1"}}, rec)
        graph = graph_from_events([e.to_dict() for e in rec.events])
        self.assertIn("run:r", graph.nodes)
        self.assertGreater(len(tuple(graph.iter_edges())), 0)

    def test_redaction(self):
        out = redact({"key": "api_key=abc123", "plain": "hello"})
        self.assertEqual(out["key"], "[REDACTED]")

    def test_trajectory_similarity(self):
        result = compare_trajectories(["retrieve docs", "answer"], ["retrieve docs", "answer"])
        self.assertEqual(result.similarity, 1.0)
