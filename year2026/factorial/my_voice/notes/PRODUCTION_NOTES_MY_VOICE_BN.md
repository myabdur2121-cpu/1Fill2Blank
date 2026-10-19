# Factorial — আপনার নিজের কণ্ঠের production note

## Final ফাইল
- `Factorial_1Fill2Blank_MY_VOICE_FINAL.mp4`
- 1920×1080, 30 fps, H.264 + AAC 192 kbps stereo 48 kHz
- দৈর্ঘ্য: 249.60 সেকেন্ড (04:09.6)
- আকার: প্রায় 13 MB
- Loudness: -15.22 LUFS, true peak প্রায় -1.4 dBFS

## যা ব্যবহার করা হয়েছে
- Manim Community (ManimCE) 0.21.0
- Slim LaTeX (`latex_slim.sh`)
- CMU Serif ও Noto Serif Bengali ফন্ট
- আপনার আগের Factorial scene-এর visual design প্রায় অপরিবর্তিত রাখা হয়েছে। শুধু voice sync-এর জন্য micro timing mark/pad যোগ করা হয়েছে এবং ছয়টি path highlight সামান্য দ্রুত করা হয়েছে।

## Voice checking ও take selection
আপনার 39টি Adobe-enhanced WAV এবং raw `My recording 10.m4a`—মোট 40টি রেকর্ডিং একে একে পরীক্ষা করা হয়েছে।

- Voice 9-এ “উত্তর হলো না...” পুরো অংশটি ছিল; আবার raw 10 + voice 11-এ একই অংশ ভাগ করে ছিল। পরের split take (raw 10 + voice 11) ব্যবহার করা হয়েছে। Raw 10-এ হালকা noise-clean ও অন্য ক্লিপের সঙ্গে level মেলানো হয়েছে।
- “তিনজন মানুষকে মোট কতভাবে সাজানো যায়?” প্রশ্নটি voice 13, 15 ও 16-তে তিনবার ছিল। শেষ take, voice 16, ব্যবহার করা হয়েছে।
- Voice 4-কে logo-র আগে ও পরে ব্যবহারের জন্য স্বাভাবিক pause-এ ভাগ করা হয়েছে।
- Voice 18 ও voice 27-কেও স্বাভাবিক pause-এ ভাগ করা হয়েছে, যাতে animation stage ও প্রশ্নের পরের বিরতি ঠিক থাকে।

সব মিলিয়ে final narration-এ 40টি micro voice unit (M01–M40) আছে।

## Gap / pause নীতি
- প্রতিটি রেকর্ডিংয়ের শুরু ও শেষের বাড়তি phone-silence কেটে দেওয়া হয়েছে।
- সাধারণ বাক্যের পরে প্রায় 0.30–0.45 সেকেন্ড বিরতি।
- একই বাক্যের ভাঙা অংশ হলে প্রায় 0.15–0.25 সেকেন্ড।
- প্রশ্নের পরে সাধারণত প্রায় 0.92–1.05 সেকেন্ড; বড় প্রশ্নটি পর্দায় থাকায় সেখানে প্রায় 2.58 সেকেন্ড সময় পাওয়া যায়।
- দৃশ্য বদল বা equation reveal চলার সময় কিছু জায়গায় animation নিজেই একটু বেশি সময় নেয়; সেখানে background music ফাঁক পূরণ করে।

## Music
আগের project-এর `make_music.py` দিয়ে ঠিক final video-র দৈর্ঘ্যের নতুন original background track তৈরি করা হয়েছে:
- preset: background, BPM 72, seed 7
- voice চলার সময় sidechain ducking
- logo ও outro অংশে music-only

## QC
- পুরো MP4 decode পরীক্ষা: OK
- 45 dB-এর নিচে 3 সেকেন্ডের বেশি সম্পূর্ণ নীরবতা নেই
- Final marks অনুযায়ী কোনো speech overlap নেই (একটি জায়গায় শুধু silent handle-এর 0.03 সেকেন্ড file-overlap আছে; আসল কথার মাঝে তখনও প্রায় 0.15 সেকেন্ড ফাঁক আছে)
- 15টি গুরুত্বপূর্ণ timestamp-এর frame চোখে দেখা হয়েছে: opening formula, big `!`, factorial list, logo, football field, বাংলা প্রশ্ন, তিনটি block, Combination Tree, ছয়টি arrangement, `3!`, general `n`, final `n!` equation ও outro ঠিক আছে।

## আনুমানিক timeline
- 00:00 — Opening formulas
- 00:11 — Big `!`
- 00:16 — 1!–20! list
- 00:23 — `n!` formula ও question marks
- 00:37–00:49 — Mid logo (music only)
- 00:49 — Football players
- 01:04 — Position swap question
- 01:27 — “তিনজনকে মোট কতভাবে সাজানো যায়?”
- 01:36 — 3 → 2 → 1 choices
- 02:01 — Combination Tree
- 02:43 — Six paths ও `3!`
- 03:05 — General case `n`
- 03:41 — Final `n!` equation
- 03:52 — Closing line
- 03:59–04:10 — Outro logo (music only)

## একটি repo নোট
আপনার দেওয়া `manim-projects` লিংকটি unauthenticated GitHub থেকে 404 দিয়েছে (private/renamed হতে পারে)। তবে প্রয়োজনীয় Factorial scene ও production উপকরণ `trush` রিপোর ভেতরের কপি এবং আলাদা `1Fill2Blank` রিপোতে পাওয়া গেছে, তাই কাজ আটকায়নি। কোনো GitHub token ব্যবহার করা হয়নি এবং কোনো push করা হয়নি।

### প্রকাশ-পরবর্তী সংযোজন (2026-10-19)

ওপরের অনুচ্ছেদটি production শেষ হওয়ার মুহূর্তের রেকর্ড—তখন পর্যন্ত সত্যিই
কোনো token/push হয়নি। পরে একই দিনে মালিকের অনুমতিতে কাজটি প্রকাশ করা হয়:
এই project `1Fill2Blank` repo-র `main`-এ ওঠে (PR #1, পরে status PR #2) এবং
final MP4 প্রকাশিত হয় GitHub Release `factorial-my-voice-v1`-এ। Reusable
skill/tools এরপর `1Fill2Blank-Tools`-এ পৃথকভাবে version ধরে এগিয়েছে
(v0.2.x)। বর্তমান canonical অবস্থা জানতে এই ফোল্ডারের `README.md` ও
`REBUILD.md` দেখুন। এই সংযোজন শুধু বিভ্রান্তি এড়াতে; production-এর
মূল সিদ্ধান্ত ও রেকর্ড অপরিবর্তিত রাখা হলো।
