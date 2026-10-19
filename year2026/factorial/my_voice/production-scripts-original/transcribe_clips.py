#!/usr/bin/env python3
"""Transcribe the user's Bengali factorial voice clips clip-by-clip.

The known script is supplied only as a vocabulary prompt. Every source file
is transcribed independently so clip numbering/order can be audited.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel

PROMPT = (
    "বাংলা গণিত ভিডিওর ধারাভাষ্য। শব্দগুলো: Factorial, Binomial Theorem, "
    "Taylor Series, Combinations, Tree Diagram, Choice, গোলকিপার, ডিফেন্ডার, "
    "স্ট্রাইকার, খেলোয়াড় A B C, n factorial, n গুণ (n-1) গুণ (n-2)।"
)


def natural_key(path: Path):
    match = re.search(r"_(\d+)-enhanced", path.stem)
    if match:
        return (int(match.group(1)), path.name.lower())
    nums = [int(x) for x in re.findall(r"\d+", path.stem)]
    return (nums[-1] if nums else 10**9, path.name.lower())


def decode_16k_mono(path: Path) -> np.ndarray:
    """Decode with system FFmpeg, avoiding the installed PyAV API mismatch."""
    cmd = [
        "ffmpeg", "-v", "error", "-nostdin", "-i", str(path),
        "-f", "f32le", "-acodec", "pcm_f32le", "-ac", "1", "-ar", "16000", "-",
    ]
    raw = subprocess.check_output(cmd)
    return np.frombuffer(raw, dtype=np.float32).copy()


def trim_for_asr(audio: np.ndarray, sr: int = 16000) -> tuple[np.ndarray, float, float]:
    """Remove phone start/stop silence while retaining 250 ms handles."""
    frame = int(0.02 * sr)
    if len(audio) <= frame:
        return audio, 0.0, len(audio) / sr
    rms = np.array(
        [np.sqrt(np.mean(audio[i : i + frame] ** 2) + 1e-12) for i in range(0, len(audio) - frame + 1, frame)]
    )
    db = 20 * np.log10(rms + 1e-12)
    idx = np.where(db > -45.0)[0]
    if len(idx) == 0:
        return audio, 0.0, len(audio) / sr
    start = max(0, int(idx[0] * frame - 0.25 * sr))
    end = min(len(audio), int((idx[-1] + 1) * frame + 0.25 * sr))
    return audio[start:end], start / sr, end / sr


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="small")
    ap.add_argument("--out", default="analysis/transcripts_small.json")
    ap.add_argument("--files", nargs="*", help="explicit files; default all enhanced wavs + raw recording 10")
    ap.add_argument("--beam", type=int, default=5)
    args = ap.parse_args()

    root = Path(__file__).resolve().parent
    if args.files:
        files = [Path(x).expanduser().resolve() for x in args.files]
    else:
        enhanced = Path("/home/user/work_factorial_myvoice/source_repos/trush_fresh/my_voice_for_factrioal/adobe_enhance_voice")
        raw10 = Path("/home/user/work_factorial_myvoice/source_repos/trush_fresh/my_voice_for_factrioal/My recording 10.m4a")
        files = sorted(enhanced.glob("*.wav"), key=natural_key)
        # Keep the chronologically sequential raw clip where it belongs.
        insert_at = next((i for i, p in enumerate(files) if natural_key(p)[0] > 10), len(files))
        files.insert(insert_at, raw10)

    started = time.time()
    print(f"Loading faster-whisper model={args.model!r} (CPU int8)...", flush=True)
    model = WhisperModel(
        args.model,
        device="cpu",
        compute_type="int8",
        cpu_threads=2,
        num_workers=1,
        download_root=str(root / "asr_models"),
    )
    print(f"Model ready in {time.time()-started:.1f}s; files={len(files)}", flush=True)

    results = []
    for idx, path in enumerate(files, 1):
        t0 = time.time()
        audio_full = decode_16k_mono(path)
        audio, trim_start, trim_end = trim_for_asr(audio_full)
        segments, info = model.transcribe(
            audio,
            language="bn",
            task="transcribe",
            beam_size=args.beam,
            best_of=5,
            patience=1.0,
            temperature=0.0,
            compression_ratio_threshold=2.4,
            log_prob_threshold=-1.0,
            no_speech_threshold=0.45,
            condition_on_previous_text=False,
            vad_filter=False,
            word_timestamps=False,
            repetition_penalty=1.08,
            no_repeat_ngram_size=3,
        )
        segment_list = []
        for s in segments:
            segment_list.append(
                {
                    "start": round(float(s.start), 3),
                    "end": round(float(s.end), 3),
                    "text": s.text.strip(),
                    "avg_logprob": round(float(s.avg_logprob), 4),
                    "no_speech_prob": round(float(s.no_speech_prob), 4),
                    "words": [
                        {
                            "start": round(float(w.start), 3),
                            "end": round(float(w.end), 3),
                            "word": w.word,
                            "probability": round(float(w.probability), 4),
                        }
                        for w in (s.words or [])
                    ],
                }
            )
        text = " ".join(s["text"] for s in segment_list).strip()
        row = {
            "index": idx,
            "file": str(path),
            "name": path.name,
            "duration_asr": round(float(info.duration), 3),
            "trim_start_s": round(float(trim_start), 3),
            "trim_end_s": round(float(trim_end), 3),
            "language": info.language,
            "language_probability": round(float(info.language_probability), 4),
            "text": text,
            "segments": segment_list,
            "elapsed_s": round(time.time() - t0, 2),
        }
        results.append(row)
        print(f"[{idx:02d}/{len(files)}] {path.name} :: {text}", flush=True)

        out = root / args.out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"DONE {len(results)} files in {time.time()-started:.1f}s -> {root/args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
