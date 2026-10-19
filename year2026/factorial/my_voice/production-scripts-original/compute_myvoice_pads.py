#!/usr/bin/env python3
"""Compute micro-pads from pass-1 Manim marks and cleaned voice units.

The desired gap in voice_units.json is measured between actual speech,
not between file boundaries. Therefore:
required mark interval = clip duration - current tail handle
                         + desired speech gap - next lead handle
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORDER = (
    [f"M{i:02d}" for i in range(1, 5)]
    + ["LOGO_MID"]
    + [f"M{i:02d}" for i in range(5, 41)]
    + ["OUTRO", "END"]
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--marks", default=str(ROOT / "timing/marks_pass1_myvoice.json"))
    ap.add_argument("--out", default=str(ROOT / "timing/pad_myvoice.json"))
    ap.add_argument("--report", default=str(ROOT / "timing/pad_report_myvoice.json"))
    args = ap.parse_args()

    marks = json.loads(Path(args.marks).read_text(encoding="utf-8"))
    missing = [k for k in ORDER if k not in marks]
    if missing:
        raise SystemExit(f"Missing marks: {missing}; got {list(marks)}")
    if any(marks[ORDER[i + 1]] < marks[ORDER[i]] - 1e-6 for i in range(len(ORDER) - 1)):
        raise SystemExit(f"Marks are not monotonic: {marks}")

    manifest = json.loads((ROOT / "timing/voice_units.json").read_text(encoding="utf-8"))
    units = {u["id"]: u for u in manifest["units"]}

    pads: dict[str, float] = {}
    report = []
    print(f"{'unit':6s} {'start':>8s} {'anim':>7s} {'voice':>7s} {'need':>7s} {'pad':>7s} {'gap*':>7s}")
    for i, key in enumerate(ORDER[:-1]):
        next_key = ORDER[i + 1]
        natural = float(marks[next_key] - marks[key])
        if key not in units:
            report.append({"unit": key, "next": next_key, "natural_s": round(natural, 3), "pad_s": 0.0})
            print(f"{key:6s} {marks[key]:8.2f} {natural:7.2f} {'--':>7s} {'--':>7s} {0.0:7.2f} {'--':>7s}")
            continue

        u = units[key]
        duration = float(u["duration_s"])
        tail = float(u["tail_handle_s"])
        if next_key in units:
            desired = float(u["gap_after_speech_s"] if u["gap_after_speech_s"] is not None else 0.45)
            next_lead = float(units[next_key]["lead_handle_s"])
        else:
            # A short, clean beat before a logo/outro mark.
            desired = 0.65
            next_lead = 0.0
        required = duration - tail + desired - next_lead
        pad = max(0.0, required - natural)
        pads[key] = round(pad, 3)
        final_interval = natural + pad
        actual_speech_gap = final_interval - duration + tail + next_lead
        report.append(
            {
                "unit": key,
                "next": next_key,
                "natural_s": round(natural, 3),
                "voice_duration_s": duration,
                "required_interval_s": round(required, 3),
                "pad_s": round(pad, 3),
                "desired_speech_gap_s": desired,
                "predicted_speech_gap_s": round(actual_speech_gap, 3),
                "text": u["text_bn_corrected"],
            }
        )
        print(
            f"{key:6s} {marks[key]:8.2f} {natural:7.2f} {duration:7.2f} "
            f"{required:7.2f} {pad:7.2f} {actual_speech_gap:7.2f}"
        )

    total_pad = sum(pads.values())
    expected = float(marks[ORDER[-1]] + total_pad)
    print(f"Voice total {sum(u['duration_s'] for u in units.values()):.2f}s; pads {total_pad:.2f}s; expected final {expected:.2f}s")
    Path(args.out).write_text(json.dumps(pads, indent=2), encoding="utf-8")
    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("WROTE", args.out)
    print("WROTE", args.report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
