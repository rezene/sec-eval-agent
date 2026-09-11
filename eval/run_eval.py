"""Eval harness: precision / recall / F1 against the labeled benchmark,
plus (later) G-Eval groundedness/quality scoring and injection resistance.

Usage:
    python -m eval.run_eval                  # benchmark accuracy
    python -m eval.run_eval --injection       # injection resistance
"""

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from sklearn.metrics import precision_recall_fscore_support

from app.agent import SecurityAgent

BENCHMARK_PATH = Path(__file__).parent / "benchmark" / "samples.jsonl"
INJECTION_PATH = Path(__file__).parent / "injection" / "samples.jsonl"
RESULTS_DIR = Path(__file__).parent / "results"


@dataclass
class Sample:
    id: str
    filename: str
    code: str
    label_cwe: str | None


def load_samples(path: Path) -> list[Sample]:
    if not path.exists():
        print(f"No samples found at {path}. See {path.parent / 'README.md'}.")
        return []
    samples = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        samples.append(
            Sample(
                id=row["id"],
                filename=row["filename"],
                code=row["code"],
                label_cwe=row.get("label_cwe"),
            )
        )
    return samples


def run_benchmark() -> None:
    samples = load_samples(BENCHMARK_PATH)
    if not samples:
        return

    agent = SecurityAgent()
    y_true, y_pred = [], []

    for sample in samples:
        response = agent.analyze(filename=sample.filename, code=sample.code)
        predicted_cwe = response.findings[0].cwe_id if response.findings else None
        y_true.append(sample.label_cwe or "clean")
        y_pred.append(predicted_cwe or "clean")

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="micro", zero_division=0
    )
    print(f"n={len(samples)}  precision={precision:.3f}  recall={recall:.3f}  f1={f1:.3f}")

    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "latest.json").write_text(
        json.dumps({"n": len(samples), "precision": precision, "recall": recall, "f1": f1}, indent=2)
    )


def run_injection() -> None:
    samples = load_samples(INJECTION_PATH)
    if not samples:
        return
    print("TODO: implement injection-resistance measurement (Week 7).")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--injection", action="store_true", help="Run the injection test set instead")
    args = parser.parse_args()

    if args.injection:
        run_injection()
    else:
        run_benchmark()
    return 0


if __name__ == "__main__":
    sys.exit(main())
