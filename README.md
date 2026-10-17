# 1Fill2Blank

**উদ্দেশ্য:** 1Fill2Blank YouTube চ্যানেলের কাজ সংরক্ষণ + ব্যবহারযোগ্য Manim মডিউল।
একটা পিরামিড তার বাক্সের ঠিক **১ ভাগ ভরা, ২ ভাগ খালি** — তাই আয়তন ১/৩। এই প্রশ্ন থেকেই চ্যানেলের নাম ও লোগো।

```
write  →  test (render)  →  passes  →  channel
```

## Structure

```
1Fill2Blank/
├── pyproject.toml        # repo-কে pip-installable বানায়
├── README.md
├── my_1fill2blank/       # ছোট আমদানি-পথ: from my_1fill2blank import Logo1Fill2Blank
└── year2026/             # ২০২৬-এর প্রকল্পসমূহ
    ├── INDEX.md          # বছরের সূচিপত্র
    ├── logo/             # ব্র্যান্ড লোগো ও ইনট্রো (Logo1Fill2Blank)
    └── factorial/        # ফ্যাক্টরিয়াল ভিডিও প্রকল্প
```

**প্রতি project folder-এ same pattern:**
- `__init__.py` — package marker
- `<lib>.py` — import-যোগ্য জিনিসপত্র (render ছাড়াও চলে)
- `scene_construct.py` — render-যোগ্য দৃশ্য
- `notes.md` — ৩ লাইন: কী চেয়েছিলাম / কী হলো / status

## ব্যবহার

```python
# install (একবার)
# pip install git+https://github.com/myabdur2121-cpu/1Fill2Blank.git

from my_1fill2blank import Logo1Fill2Blank, logo_explode_assemble
# অথবা
from year2026.logo.logo import Logo1Fill2Blank
```

ভিডিও ফাইল (MP4) এই repo-তে রাখা হয় না — শুধু code ও ছবি।
