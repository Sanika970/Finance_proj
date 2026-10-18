import pathlib
import sys

import numpy as np
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from engine.network import load_activities, topo_order  # noqa: E402
from engine.simulate import pert_beta_samples, project_duration  # noqa: E402

BENCHMARK = pathlib.Path(__file__).resolve().parents[1] / "data" / "benchmark_6_activity.csv"


def test_benchmark_loads_and_orders():
    acts = load_activities(BENCHMARK)
    order = topo_order(acts)
    assert order.index("A") < order.index("B") < order.index("D") < order.index("F")
    assert len(acts) == 6


def test_cycle_is_detected():
    acts = {
        "X": {"id": "X", "name": "", "o": 1, "m": 2, "p": 3, "preds": ["Y"]},
        "Y": {"id": "Y", "name": "", "o": 1, "m": 2, "p": 3, "preds": ["X"]},
    }
    with pytest.raises(ValueError, match="Cycle"):
        topo_order(acts)


def test_pert_mean_matches_formula():
    rng = np.random.default_rng(0)
    samples = pert_beta_samples(2, 5, 14, 200_000, rng)
    expected = (2 + 4 * 5 + 14) / 6
    assert samples.mean() == pytest.approx(expected, rel=0.01)


def test_deterministic_case_gives_critical_path_length():
    # O = M = P for every activity: the result must equal the longest path (A-B-D = 8).
    acts = {
        "A": {"id": "A", "name": "", "o": 3, "m": 3, "p": 3, "preds": []},
        "B": {"id": "B", "name": "", "o": 4, "m": 4, "p": 4, "preds": ["A"]},
        "C": {"id": "C", "name": "", "o": 2, "m": 2, "p": 2, "preds": ["A"]},
        "D": {"id": "D", "name": "", "o": 1, "m": 1, "p": 1, "preds": ["B", "C"]},
    }
    durations = project_duration(acts, n_iter=100, seed=1)
    assert np.allclose(durations, 3 + 4 + 1)
