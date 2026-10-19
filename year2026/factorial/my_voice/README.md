# Factorial — নিজের কণ্ঠে (my_voice, v1)

Status: ✅ v1 সম্পূর্ণ ও GitHub-এ প্রকাশিত (owner review-তে পছন্দ হয়েছে)। Final ভিডিও: [Release `factorial-my-voice-v1`](https://github.com/myabdur2121-cpu/1Fill2Blank/releases/tag/factorial-my-voice-v1)।

## ফল

- Final: `Factorial_1Fill2Blank_MY_VOICE_FINAL.mp4` — 1920×1080, 30 fps, 04:09.6 (Release-এ যাবে: tag `factorial-my-voice-v1`)
- Voice: নিজের রেকর্ড করা clips থেকে 40টি micro-unit (M01…M40), মোট cleaned speech প্রায় 200 s
- QC: −15.22 LUFS, true peak ≈ −1.4 dBFS, full decode OK, 3 s-এর বেশি silence নেই

## এই ফোল্ডারে যা থাকবে

| জিনিস | ব্যাখ্যা |
|---|---|
| `project_config.json` | skill version pinসহ পুরো project সেটিং |
| `voice_unit_decisions.json` | কোন take, কোথায় split, কত gap — `prepare_voice_units.py`-এর ইনপুট সিদ্ধান্ত |
| `timing/voice_units.json` | তৈরি units-এর portable manifest (source path voice folder-এর relative) |
| `timing/` অন্যান্য | pass-1/final marks, pads + report, sync plan, speech-gap audit |
| `build_production_scene.py` | base scene থেকে production scene generate করার portable builder |
| `../factorial_myvoice_production.py` | generated production scene (হাতে edit নয়; builder দিয়ে আবার তৈরি হয়) |
| `REBUILD.md` | ধাপে ধাপে আবার বানানোর নির্দেশ |
| `notes/PRODUCTION_NOTES_MY_VOICE_BN.md` | বাংলায় বিস্তারিত production নোট |
| `production-scripts-original/` | v1-এর সময়কার original scriptগুলো হুবহু (ঐতিহাসিক reference) |

## আবার বানাতে হলে

বিস্তারিত কমান্ডসহ নির্দেশ আছে [`REBUILD.md`](REBUILD.md)-তে। সংক্ষেপে:
setup যাচাই → `build_production_scene.py` দিয়ে scene generate → decisions থেকে voice units → pass-1 marks → pads → 1080p30 silent render → music/mix → QC।
Render-এর সময় repo root-কে `PYTHONPATH`-এ রাখতে হবে।

## জানা বিষয়

- বাদ দেওয়া take: enhanced 9 (raw 10 + enhanced 11 দিয়ে প্রতিস্থাপিত), প্রশ্নের take 13 ও 15 (16 নেওয়া হয়েছে)।
- Reproducibility যাচাই (2026-10-19): fresh clone-এর base scene থেকে scene regenerate করে no-pad smoke render-এ 43টি marks আগের pass-1-এর সঙ্গে হুবহু মিলেছে (END 166.867 s); GitHub-এর enhanced source দিয়ে manifest dry-run-এ সব numeric মান হুবহু মিলেছে।
