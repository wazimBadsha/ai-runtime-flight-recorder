import unittest
from aibpe.experiment import run_intervention
from aibpe.intervention import Intervention

class ExperimentTests(unittest.TestCase):
    def test_run_intervention_separates_dependency_and_behavior(self):
        calls = []
        baseline = {"retrieval": {"corpus": "v1"}, "model": {"name": "demo"}}
        intervention = Intervention("retrieval.corpus", "v2")

        def execute(state):
            calls.append(state["retrieval"]["corpus"])
            return "out-" + state["retrieval"]["corpus"]

        result = run_intervention(baseline, intervention, execute)
        self.assertEqual(calls, ["v1", "v2"])
        self.assertTrue(result.dependency_changed)
        self.assertTrue(result.behavior_changed)
        self.assertTrue(result.intervention_supported)
        self.assertEqual(result.changed_paths, ("retrieval.corpus",))

    def test_intervention_without_behavior_change_is_not_supported(self):
        baseline = {"retrieval": {"corpus": "v1"}}
        result = run_intervention(
            baseline,
            Intervention("retrieval.corpus", "v2"),
            lambda _: "same",
        )
        self.assertTrue(result.dependency_changed)
        self.assertFalse(result.behavior_changed)
        self.assertFalse(result.intervention_supported)
