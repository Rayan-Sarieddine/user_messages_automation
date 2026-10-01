"""CLI utility: run the pipeline over the 5 assessment samples and write the
structured output records to output.json (deliverable 4.2)."""

import json
import sys
from pathlib import Path

from arcvault_ai import run_triage
from samples import SAMPLE_INPUTS


def main() -> None:
    records = []
    for sample in SAMPLE_INPUTS:
        record = run_triage(sample["message"], sample["source"])
        records.append(record.model_dump(mode="json"))
        print(f"[{record.category.value}] -> {record.routing_queue.value} "
              f"(escalated={record.escalation_flag}, confidence={record.confidence:.2f})")

    out_path = Path(__file__).parent / "output.json"
    out_path.write_text(json.dumps(records, indent=2))
    print(f"\nWrote {len(records)} records to {out_path}")


if __name__ == "__main__":
    sys.exit(main())
