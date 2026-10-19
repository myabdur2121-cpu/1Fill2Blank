# Rebuild — Factorial (my_voice)

এই ভিডিওটা আবার বানানোর সঠিক ক্রম। ধরে নেওয়া হয়েছে তিনটি repo পাশাপাশি clone করা আছে:

- `$PROJECTS` = এই repo (`1Fill2Blank`)
- `$TOOLS` = `1Fill2Blank-Tools`
- `$SETUP` = `manim-sandbox-setup`

Voice source থাকে আলাদা `trush` repo-তে: `my_voice_for_factrioal/`
(enhanced WAV তার `adobe_enhance_voice/` subfolder-এ)।

## 0. Environment

```bash
cd $SETUP && bash manimce.sh && bash latex_slim.sh
$SETUP/bin/manim --version   # Manim Community v0.21.0 প্রত্যাশিত
ffmpeg -version | head -1
```

## 1. Production scene generate করা

```bash
cd $PROJECTS/year2026/factorial/my_voice
python3 build_production_scene.py
# তৈরি হবে: ../factorial_myvoice_production.py (653 lines)
```

Generated ফাইল হাতে edit করা যাবে না — বদল লাগলে builder বা base scene বদলে আবার generate করতে হবে।

## 2. Voice units তৈরি

```bash
python3 $TOOLS/tools/prepare_voice_units.py \
  --decisions voice_unit_decisions.json \
  --source-root <trush-clone>/my_voice_for_factrioal \
  --out-dir audio_clean \
  --out-manifest timing/voice_units.json
```

`audio_clean/` generated — Git-এ যাবে না (দেখুন এই ফোল্ডারের `.gitignore`)।

## 3. Pass-1 timing render (no pads)

```bash
cd $PROJECTS
printf '{}' > /tmp/no_pads.json
PYTHONPATH=$PROJECTS VOICE_PAD_FILE=/tmp/no_pads.json \
SCENE_MARKS_FILE=$PROJECTS/year2026/factorial/my_voice/timing/marks_pass1_myvoice.json \
$SETUP/bin/manim render -ql year2026/factorial/factorial_myvoice_production.py FactrioalScene
```

`PYTHONPATH`-এ repo root থাকা জরুরি, নইলে `year2026.logo` import fail করবে।
প্রত্যাশিত natural END ≈ 166.867 s।

## 4. Pads হিসাব

```bash
cd $PROJECTS/year2026/factorial/my_voice
python3 $TOOLS/tools/compute_pads.py timing/marks_pass1_myvoice.json audio_clean timing/pad_myvoice.json \
  --plan project_config.json --voice-units timing/voice_units.json \
  --report timing/pad_report_myvoice.json
```

## 5. Final silent render (1080p30)

```bash
cd $PROJECTS
PYTHONPATH=$PROJECTS \
SCENE_MARKS_FILE=$PROJECTS/year2026/factorial/my_voice/timing/marks_final_myvoice.json \
$SETUP/bin/manim render --format=mp4 --resolution=1920,1080 --fps=30 \
  year2026/factorial/factorial_myvoice_production.py FactrioalScene
```

Pad ফাইল default হিসেবে scene নিজেই `my_voice/timing/pad_myvoice.json` পড়ে।

## 6. Music + mix

```bash
# ঠিক final দৈর্ঘ্যের music (END অনুযায়ী), তারপর duckingসহ mix —
# $TOOLS/tools/make_music.py ও mix_voice_music.py ব্যবহার করো।
# v1 সেটিং: preset=background, BPM 72, seed 7, music voice-এর 11 dB নিচে।
```

## 7. QC

```bash
python3 $TOOLS/tools/qc_video.py <final.mp4> --config project_config.json \
  --marks-final timing/marks_final_myvoice.json --voice-units timing/voice_units.json \
  --contact-sheet contact_sheet.jpg --output qc_report.json
```

v1-এর মাপা ফল: −15.22 LUFS, true peak −1.4 dBTP, END 249.6 s।
Correction এলে timestamp ধরে `voice_unit_decisions.json`/config বদলে ধাপ 2 থেকে আবার করো; final MP4 হাতে edit নয়।
