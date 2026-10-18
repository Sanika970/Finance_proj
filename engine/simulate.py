"""Monte Carlo schedule engine: PERT-Beta sampling and a vectorised forward pass."""
import numpy as np

from .network import topo_order


def pert_beta_samples(o, m, p, n, rng):
    """Draw n durations from a PERT-Beta distribution with limits o and p, mode m."""
    if p == o:
        return np.full(n, m, dtype=float)
    alpha = 1 + 4 * (m - o) / (p - o)
    beta = 1 + 4 * (p - m) / (p - o)
    return o + (p - o) * rng.beta(alpha, beta, size=n)


def sample_durations(acts, n_iter=10000, seed=42):
    rng = np.random.default_rng(seed)
    return {k: pert_beta_samples(a["o"], a["m"], a["p"], n_iter, rng) for k, a in acts.items()}


def forward_pass(acts, durations, order):
    """Early finish for every activity, for all iterations at once."""
    n = next(iter(durations.values())).shape[0]
    ef = {}
    for k in order:
        preds = acts[k]["preds"]
        early_start = np.max([ef[p] for p in preds], axis=0) if preds else np.zeros(n)
        ef[k] = early_start + durations[k]
    return ef


def project_duration(acts, n_iter=10000, seed=42):
    """Array of project durations, one per iteration."""
    order = topo_order(acts)
    durations = sample_durations(acts, n_iter, seed)
    ef = forward_pass(acts, durations, order)
    has_successor = {p for a in acts.values() for p in a["preds"]}
    finish_points = [k for k in acts if k not in has_successor]
    return np.max([ef[k] for k in finish_points], axis=0)


def percentiles(values):
    return {
        "P50": float(np.percentile(values, 50)),
        "P80": float(np.percentile(values, 80)),
        "P90": float(np.percentile(values, 90)),
    }
