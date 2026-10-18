"""Load the activity network from CSV and check it is valid."""
import csv
from collections import deque

REQUIRED_COLUMNS = ["id", "name", "optimistic", "most_likely", "pessimistic", "predecessors"]


def load_activities(path):
    """Read an activity CSV. Predecessors are separated by semicolons."""
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Missing columns: {missing}")
        rows = list(reader)

    acts = {}
    for r in rows:
        preds = [p.strip() for p in r["predecessors"].split(";") if p.strip()]
        acts[r["id"]] = {
            "id": r["id"],
            "name": r["name"],
            "o": float(r["optimistic"]),
            "m": float(r["most_likely"]),
            "p": float(r["pessimistic"]),
            "preds": preds,
        }
    validate(acts)
    return acts


def validate(acts):
    """Raise ValueError on bad durations, unknown predecessors or loops."""
    for a in acts.values():
        if not (a["o"] <= a["m"] <= a["p"]):
            raise ValueError(f"{a['id']}: need optimistic <= most likely <= pessimistic")
        for p in a["preds"]:
            if p not in acts:
                raise ValueError(f"{a['id']}: unknown predecessor {p}")
    return topo_order(acts)


def topo_order(acts):
    """Return activity ids in an order where predecessors come first."""
    indeg = {k: len(v["preds"]) for k, v in acts.items()}
    succ = {k: [] for k in acts}
    for k, v in acts.items():
        for p in v["preds"]:
            succ[p].append(k)

    queue = deque(sorted(k for k, d in indeg.items() if d == 0))
    order = []
    while queue:
        k = queue.popleft()
        order.append(k)
        for s in sorted(succ[k]):
            indeg[s] -= 1
            if indeg[s] == 0:
                queue.append(s)

    if len(order) != len(acts):
        raise ValueError("Cycle detected in predecessor links")
    return order
