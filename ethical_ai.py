"""Evaluate core ethical AI pillars for agent operations."""

from dataclasses import dataclass
from typing import List, Dict, Any
import argparse
import json

@dataclass
class PillarScores:
    fairness: float
    transparency: float
    privacy: float
    accountability: float
    reliability: float

    def overall(self) -> float:
        return (
            self.fairness
            + self.transparency
            + self.privacy
            + self.accountability
            + self.reliability
        ) / 5


def compute_statistical_parity(dataset: List[Dict[str, Any]], group_key: str, prediction_key: str) -> float:
    """Return the absolute statistical parity difference between groups."""
    groups: Dict[Any, Dict[str, int]] = {}
    for row in dataset:
        group = row.get(group_key)
        pred = int(row.get(prediction_key, 0))
        info = groups.setdefault(group, {"positive": 0, "total": 0})
        info["total"] += 1
        if pred:
            info["positive"] += 1
    if len(groups) < 2:
        return 0.0
    rates = [info["positive"] / info["total"] for info in groups.values() if info["total"]]
    return max(rates) - min(rates)


def compute_disparate_impact(dataset: List[Dict[str, Any]], group_key: str, prediction_key: str) -> float:
    """Return the disparate impact ratio between the lowest and highest group rates."""
    groups: Dict[Any, Dict[str, int]] = {}
    for row in dataset:
        group = row.get(group_key)
        pred = int(row.get(prediction_key, 0))
        info = groups.setdefault(group, {"positive": 0, "total": 0})
        info["total"] += 1
        if pred:
            info["positive"] += 1
    if len(groups) < 2:
        return 1.0
    rates = [info["positive"] / info["total"] for info in groups.values() if info["total"]]
    max_rate = max(rates)
    min_rate = min(rates)
    return 1.0 if max_rate == 0 else min_rate / max_rate


def generate_bias_report(dataset: List[Dict[str, Any]], group_key: str = "group", prediction_key: str = "prediction") -> Dict[str, float]:
    """Generate a dictionary with basic fairness metrics."""
    stat_parity = compute_statistical_parity(dataset, group_key, prediction_key)
    disp_impact = compute_disparate_impact(dataset, group_key, prediction_key)
    return {
        "statistical_parity_difference": stat_parity,
        "disparate_impact_ratio": disp_impact,
    }


def export_bias_report(report: Dict[str, float], path: str) -> None:
    """Write the bias report to a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

class EthicalEvaluator:
    def __init__(self, dataset: List[Dict[str, Any]], logs: List[Dict[str, Any]], model: Any):
        self.dataset = dataset
        self.logs = logs
        self.model = model

    def fairness_score(self, group_key: str = "group", prediction_key: str = "prediction") -> float:
        """Return a combined fairness score using statistical parity and disparate impact."""
        parity_diff = compute_statistical_parity(self.dataset, group_key, prediction_key)
        disp_impact = compute_disparate_impact(self.dataset, group_key, prediction_key)

        # Normalize metrics to [0,1] where 1 is best fairness
        parity_score = max(0.0, 1.0 - parity_diff)
        impact_score = min(1.0, disp_impact)
        return (parity_score + impact_score) / 2.0

    def transparency_score(self) -> float:
        return 1.0 if hasattr(self.model, "explain") else 0.5

    def privacy_score(self) -> float:
        personal_keys = {"name", "email", "ssn", "phone"}
        for row in self.dataset:
            if personal_keys.intersection(row.keys()):
                return 0.0
        return 1.0

    def accountability_score(self) -> float:
        return min(len(self.logs) / 10.0, 1.0)

    def reliability_score(self, outcome_key: str = "outcome", prediction_key: str = "prediction") -> float:
        if not self.dataset:
            return 1.0
        diff_sum = 0.0
        for row in self.dataset:
            diff_sum += abs(int(row.get(outcome_key, 0)) - int(row.get(prediction_key, 0)))
        mae = diff_sum / len(self.dataset)
        return max(0.0, 1 - mae)

    def evaluate(self) -> PillarScores:
        fairness = self.fairness_score()
        transparency = self.transparency_score()
        privacy = self.privacy_score()
        accountability = self.accountability_score()
        reliability = self.reliability_score()
        return PillarScores(fairness, transparency, privacy, accountability, reliability)


def load_dataset(path: str) -> List[Dict[str, Any]]:
    """Load a JSON lines dataset."""
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate ethical AI pillars")
    parser.add_argument("--dataset", type=str, help="Path to JSONL dataset")
    parser.add_argument("--bias-report", type=str, default=None, help="Optional path to export fairness metrics")
    args = parser.parse_args()

    if args.dataset:
        data = load_dataset(args.dataset)
    else:
        data = [
            {"group": "A", "outcome": 1, "prediction": 1},
            {"group": "A", "outcome": 0, "prediction": 1},
            {"group": "B", "outcome": 1, "prediction": 0},
            {"group": "B", "outcome": 0, "prediction": 0},
        ]

    logs = [
        {"event": "prediction", "time": "2024-06-09T12:00:00Z"},
        {"event": "prediction", "time": "2024-06-09T12:10:00Z"},
    ]

    class DummyModel:
        def explain(self, item: Any) -> str:
            return "explanation"

    evaluator = EthicalEvaluator(data, logs, DummyModel())
    scores = evaluator.evaluate()
    print(scores)
    print(f"Overall ethical score: {scores.overall():.2f}")

    if args.bias_report:
        report = generate_bias_report(data)
        export_bias_report(report, args.bias_report)
        print(f"Bias report written to {args.bias_report}")

if __name__ == "__main__":
    main()
