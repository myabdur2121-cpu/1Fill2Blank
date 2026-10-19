#!/usr/bin/env python3
"""Prepare clean, trimmed micro-clips from the user's factorial recordings.

Editorial decisions, based on clip-by-clip transcription:
* Voice 9 is an alternate complete take of the same answer as raw recording
  10 + voice 11. The later split take (raw 10 + voice 11) is used.
* Voices 13, 15 and 16 are three takes of the same question. Voice 16,
  the last take, is used.
* Voice 4, voice 18 and voice 27 are split only at long, natural pauses.
"""
from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source_repos/trush_fresh/my_voice_for_factrioal"
ENH = SRC / "adobe_enhance_voice"
OUT = ROOT / "audio_clean"
OUT.mkdir(parents=True, exist_ok=True)

ENH_BY_LABEL = {}
for path in ENH.glob("*.wav"):
    import re

    m = re.search(r"_(\d+)-enhanced", path.name)
    if m:
        ENH_BY_LABEL[int(m.group(1))] = path


def E(label: int) -> Path:
    return ENH_BY_LABEL[label]


RAW10 = SRC / "My recording 10.m4a"

# id, source, explicit range (or None), corrected/intended Bengali text,
# desired silence after the *speech* before the next voice unit, visual note.
UNITS = [
    ("M01", E(1), None, "তুমি হয়তো দেখে থাকবে যে Binomial Theorem, Taylor Series, এমনকি Combinations-এর মতো বিভিন্ন গাণিতিক বিষয়েও Factorial-এর ব্যবহার রয়েছে।", 0.45, "Opening formulas and factorial boxes"),
    ("M02", E(2), None, "কিন্তু তুমি কি কখনো নিজেকে প্রশ্ন করেছ, Factorial জিনিসটা আসলে কী?", 0.95, "Big exclamation mark"),
    ("M03", E(3), None, "কেন আমরা একের পর এক সংখ্যা গুণ করতে থাকি?", 0.75, "1! to 20! list"),
    ("M04", E(4), (None, 13.98), "সাধারণভাবে আমরা জানি, n Factorial সমান 1 into 2 into 3 into … into n। তাই না? কিন্তু প্রশ্ন হচ্ছে, আমরা কেন এভাবে গুণ করি? নিশ্চয়ই এর পেছনে কোনো একটা কারণ আছে।", None, "n! formula and question marks; then mid logo"),
    ("M05", E(4), (14.63, None), "চলো, বিষয়টাকে একটু সহজভাবে বোঝার চেষ্টা করি।", 0.35, "After logo; players appear"),
    ("M06", E(5), None, "ধরো, আমাদের কাছে তিনজন খেলোয়াড় আছে—A, B ও C।", 0.35, "Players A B C"),
    ("M07", E(6), None, "এবং এই তিনজনকে তিনটি ভিন্ন পজিশনে খেলতে হবে—গোলকিপার, ডিফেন্ডার ও স্ট্রাইকার।", 0.55, "Football field and positions"),
    ("M08", E(7), None, "এখন, A যদি গোলকিপার হয় এবং B যদি স্ট্রাইকার হয়,", 0.18, "First swap begins"),
    ("M09", E(8), None, "তাহলে তাদের পজিশন অদলবদল করে দিলে কি টিমের বিন্যাস একই থাকবে?", 1.05, "Swap question"),
    ("M10", RAW10, (0.71, 7.38), "উত্তর হলো না। কারণ খেলোয়াড়দের পজিশন পরিবর্তন করলে টিমের বিন্যাসেও পরিবর্তন ঘটে।", 0.35, "Answer; swaps continue"),
    ("M11", E(11), None, "এবং তার সাথে পারফরম্যান্সও বদলে যায়।", 0.50, "Performance/status bar"),
    ("M12", E(12), None, "তাহলে আমরা একটা প্রশ্ন করতেই পারি:", 0.22, "Players return; question text"),
    ("M13", E(16), None, "তিনজন মানুষকে মোট কতভাবে সাজানো যায়?", 1.10, "Question text hold"),
    ("M14", E(17), None, "চলো, একে একে দেখি।", 0.40, "Move to three blocks"),
    ("M15", E(18), (None, 6.13), "প্রথম পজিশনের জন্য আমাদের তিনটি Choice রয়েছে—A, B ও C।", 0.35, "Arrows to block 1; number 3"),
    ("M16", E(18), (7.05, None), "ধরো, প্রথম পজিশনে A-কে বসালাম।", 0.35, "Place A in block 1"),
    ("M17", E(19), None, "তাহলে দ্বিতীয় পজিশনের জন্য থাকবে দুটি Choice—B ও C। কারণ A ইতিমধ্যেই বসে গেছে।", 0.35, "Arrows to block 2; number 2"),
    ("M18", E(20), None, "এবার দ্বিতীয় পজিশনে B-কে বসালে, তৃতীয় পজিশনের জন্য থাকবে একমাত্র C।", 0.30, "Place B; arrow to block 3; number 1"),
    ("M19", E(21), None, "অর্থাৎ, তৃতীয় পজিশনের জন্য Choice মাত্র একটি।", 0.55, "Place C; completed 3-2-1 blocks"),
    ("M20", E(22), None, "এবার এই পুরো বিষয়টাকে একটা Tree Diagram-এর মাধ্যমে দেখি।", 0.40, "Tree title and root"),
    ("M21", E(23), None, "দেখো, এখানে তিনটি স্তর রয়েছে—প্রথম পজিশন, দ্বিতীয় পজিশন এবং তৃতীয় পজিশন।", 0.35, "Hold on title/root before branches"),
    ("M22", E(24), None, "প্রথম পজিশনে তিনটি Choice থাকায় এর শাখা হবে তিনটি—A, B ও C।", 0.35, "Tree level 1; Position 1; Choice 3"),
    ("M23", E(25), None, "আর প্রত্যেকটি শাখা থেকে দ্বিতীয় পজিশনের জন্য দুটি করে শাখা বের হবে।", 0.30, "Tree level 2; Position 2; Choice 2"),
    ("M24", E(26), None, "অর্থাৎ, প্রথম পজিশনের প্রতিটি Choice-এর জন্য দ্বিতীয় পজিশনে দুটি করে Choice রয়েছে।", 0.40, "Hold on two-level tree"),
    ("M25", E(27), (None, 5.17), "তাহলে প্রথম দুটি পজিশন মিলিয়ে মোট উপায় কত?", 0.95, "Question over 3 x 2 labels"),
    ("M26", E(27), (6.72, None), "তিন গুণ দুই, অর্থাৎ মোট ছয়টি।", 0.40, "Answer over two-level tree"),
    ("M27", E(28), None, "এবার প্রত্যেকটি বিন্যাসের জন্য তৃতীয় পজিশনে একজনই বাকি থাকবে।", 0.22, "Tree level 3 begins"),
    ("M28", E(29), None, "তাই প্রত্যেকটি শাখা থেকে আরেকটি করে শাখা বের হবে।", 0.40, "Tree level 3 labels; Choice 1; equals"),
    ("M29", E(30), None, "অর্থাৎ, মোট সম্পূর্ণ বিন্যাসের সংখ্যা হবে 3 into 2 into 1, সমান 6।", 0.45, "Highlight six paths; result 6"),
    ("M30", E(31), None, "দেখো, তিনজন খেলোয়াড়কে তিনটি ভিন্ন পজিশনে মোট ছয়ভাবে সাজানো সম্ভব।", 0.40, "Completed tree and six arrangements"),
    ("M31", E(32), None, "আর এই গুণফলটাকেই আমরা Factorial-এর সাহায্যে সংক্ষেপে লিখতে পারি: 3 Factorial সমান 3 into 2 into 1, সমান 6।", 0.55, "3! equation assembles"),
    ("M32", E(33), None, "এখন, তিনজনের বদলে n সংখ্যক খেলোয়াড়কে nটি ভিন্ন পজিশনে বসালে কী হবে?", 1.00, "Transition to general n"),
    ("M33", E(34), None, "প্রথম পজিশনের জন্য থাকবে nটি Choice।", 0.30, "General stage n"),
    ("M34", E(35), None, "দ্বিতীয় পজিশনের জন্য থাকবে (n-1)টি Choice।", 0.30, "General stage n-1"),
    ("M35", E(36), None, "তৃতীয় পজিশনের জন্য থাকবে (n-2)টি Choice।", 0.35, "General stage n-2"),
    ("M36", E(37), None, "এভাবে প্রত্যেকটি ধাপে একটি করে কমতে কমতে আসবে (n-3)-তে,", 0.25, "Ellipsis stage"),
    ("M37", E(38), None, "তারপর 3-তে, তারপর 2-তে এবং একেবারে শেষে গিয়ে পৌঁছাবে মাত্র একটি Choice-এ।", 0.40, "General stages 3, 2, 1"),
    ("M38", E(39), None, "অর্থাৎ, ধারাটা যতক্ষণ না 1-এ এসে থামছে, ততক্ষণ চলতেই থাকবে।", 0.45, "Crosses/product complete"),
    ("M39", E(40), None, "তাহলে মোট বিন্যাসের সংখ্যা হবে: n Factorial সমান n into (n-1) into (n-2) into … into 3 into 2 into 1।", 0.60, "Final n! equation assembles and frames"),
    ("M40", E(41), None, "এভাবেই আমরা বুঝতে পারি, Factorial-এর সঙ্গে কোনো কিছু সাজানো বা বিন্যস্ত করার সমস্যার একটি গভীর সম্পর্ক রয়েছে।", None, "Closing over final equation; then outro logo"),
]


def decode(path: Path, sr: int = 48000) -> np.ndarray:
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-nostdin", "-i", str(path), "-f", "f32le", "-acodec", "pcm_f32le", "-ac", "1", "-ar", str(sr), "-"]
    )
    return np.frombuffer(raw, dtype=np.float32).copy()


def speech_bounds(path: Path, explicit) -> tuple[float, float, float, float]:
    audio = decode(path)
    sr = 48000
    dur = len(audio) / sr
    if path == RAW10:
        speech_start, speech_end = 0.79, 7.28
    else:
        frame = int(0.01 * sr)
        rms = np.array(
            [np.sqrt(np.mean(audio[i : i + frame] ** 2) + 1e-12) for i in range(0, len(audio) - frame + 1, frame)]
        )
        db = 20 * np.log10(rms + 1e-12)

        # Ignore isolated recorder clicks: first find 50 ms of sustained
        # speech above -45 dB, then backtrack at most 120 ms for a soft onset.
        above = db > -45.0
        sustained = np.convolve(above.astype(int), np.ones(5, dtype=int), mode="valid")
        starts = np.where(sustained == 5)[0]
        if len(starts) == 0:
            raise RuntimeError(f"No sustained speech found in {path}")
        first_core = int(starts[0])
        last_core_start = int(starts[-1])
        back = np.where(db[max(0, first_core - 12) : first_core + 1] > -55.0)[0]
        first = max(0, first_core - 12) + int(back[0]) if len(back) else first_core
        last_core_end = last_core_start + 5
        forward_end = min(len(db), last_core_end + 15)
        fwd = np.where(db[last_core_end:forward_end] > -55.0)[0]
        last = last_core_end + int(fwd[-1] + 1) if len(fwd) else last_core_end
        speech_start, speech_end = float(first * 0.01), float(last * 0.01)

    start = max(0.0, speech_start - 0.08)
    end = min(dur, speech_end + 0.10)
    if explicit:
        ex_start, ex_end = explicit
        if ex_start is not None:
            start = float(ex_start)
        if ex_end is not None:
            end = float(ex_end)
    return start, end, speech_start, speech_end


def ffprobe_duration(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)], text=True
    )
    return float(json.loads(out)["format"]["duration"])


rows = []
for uid, src, explicit, text, gap_after, visual in UNITS:
    start, end, speech_start, speech_end = speech_bounds(src, explicit)
    duration = end - start
    out = OUT / f"{uid}.wav"
    filters = [
        f"atrim=start={start:.3f}:end={end:.3f}",
        "asetpts=N/SR/TB",
        "highpass=f=65",
    ]
    if src == RAW10:
        # Gentle broadband cleanup for the one unenhanced phone recording.
        filters += ["afftdn=nr=5:nf=-30", "lowpass=f=12500"]
    filters += [
        "afade=t=in:st=0:d=0.008",
        f"afade=t=out:st={max(0.0, duration - 0.012):.3f}:d=0.012",
        "aresample=48000",
    ]
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-nostdin", "-i", str(src),
        "-af", ",".join(filters), "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(out),
    ]
    subprocess.run(cmd, check=True)
    actual = ffprobe_duration(out)
    row = {
        "id": uid,
        "source": str(src),
        "source_name": src.name,
        "trim_start_s": round(start, 3),
        "trim_end_s": round(end, 3),
        "speech_start_s": round(speech_start, 3),
        "speech_end_s": round(speech_end, 3),
        "duration_s": round(actual, 3),
        # Handles retained in the clean file. Mix scheduling subtracts these
        # when enforcing the desired silence between actual speech.
        "lead_handle_s": round(max(0.0, speech_start - start), 3) if not (explicit and explicit[0] is not None) else 0.08,
        "tail_handle_s": round(max(0.0, end - speech_end), 3) if not (explicit and explicit[1] is not None) else 0.10,
        "gap_after_speech_s": gap_after,
        "text_bn_corrected": text,
        "visual": visual,
        "file": str(out),
    }
    # For explicit split points the neighboring speech is across the cut;
    # 0.08s/0.10s handles are the values used when those ranges were chosen.
    if explicit and explicit[0] is not None:
        row["lead_handle_s"] = 0.08
    if explicit and explicit[1] is not None:
        row["tail_handle_s"] = 0.10
    rows.append(row)
    print(f"{uid} {actual:5.2f}s  {src.name} [{start:.2f}-{end:.2f}]  {text[:72]}")

manifest = {
    "purpose": "User's own voice, micro-segmented for ManimCE sync",
    "excluded_alternate_takes": [
        {"file": "factorial_voice_9-enhanced-v2.wav", "reason": "Complete alternate of M10+M11; later split take used"},
        {"file": "factorial_voice_13-enhanced-v2.wav", "reason": "Alternate take of the M13 question"},
        {"file": "factorial_voice_15-enhanced-v2.wav", "reason": "Alternate take of the M13 question"},
    ],
    "units": rows,
    "total_clean_duration_s": round(sum(r["duration_s"] for r in rows), 3),
}
(ROOT / "timing").mkdir(exist_ok=True)
(ROOT / "timing/voice_units.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"TOTAL clean audio: {manifest['total_clean_duration_s']:.2f}s")
print("WROTE", ROOT / "timing/voice_units.json")
