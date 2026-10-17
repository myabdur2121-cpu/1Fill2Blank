"""মাঝখান থেকে বড় হয়ে স্প্রিংয়ের মতো দুলে থামার নিজস্ব অ্যানিমেশন।

গুরুত্বপূর্ণ নকশা-নীতি (ভবিষ্যতে লেখা বদলালেও যেন ছেদ না পড়ে):
    বড় হওয়ার অংশ আর দোলনের অংশ আলাদা দুটি অ্যানিমেশন নয় — একটি মাত্র
    গতি-রেখা। জোড়ার জায়গায় দুই পাশের *মান* এবং *গতি* হুবহু সমান রাখা হয়,
    অর্থাৎ বস্তু জোড়ায় এসে থামে না, গতি বয়ে গিয়ে দোলনে ঢোকে।
    এই শর্তগুলো animations/test_grow_from_center_bouncy.py দিয়ে পরীক্ষিত;
    লেখা বদলে শর্ত ভাঙলে পরীক্ষায় ধরা পড়বে।
"""

import math

from manim import GrowFromCenter


def _exponent_for_end_slope(slope: float) -> float:
    """ঘাতীয় বাড়ার রেখার ঘাত বের করে, যার শেষ ঢাল হবে slope।

    রেখাটি: s(u) = (e^(m*u) - 1) / (e^m - 1), u চলবে 0 থেকে 1।
    এর শেষ ঢাল m / (1 - e^(-m)) — m বাড়লে ঢাল বাড়ে, তাই দ্বিখণ্ডন
    পদ্ধতিতে যেকোনো ধনাত্মক ঢালের জন্য m পাওয়া যায়। এই রেখা সবসময়
    একদিকে বাড়ে (কখনো উল্টো দিকে যায় না), তাই যেকোনো মাপকাঠিতেই
    বড় হওয়ার অংশ ভাঙবে না।
    """
    if slope <= 0:
        raise ValueError("শেষ ঢাল ধনাত্মক হতে হবে")
    if abs(slope - 1.0) < 1e-12:
        return 0.0
    lo, hi = -60.0, max(60.0, slope * 2.0)

    def end_slope(m: float) -> float:
        if abs(m) < 1e-12:
            return 1.0
        return m / (1.0 - math.exp(-m))

    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if end_slope(mid) < slope:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _growth_then_spring(
    t: float,
    number_of_bounces: int,
    bounce_strength: float,
    resistance: float,
    grow_portion: float,
) -> float:
    """প্রতিটি মুহূর্তে বস্তুর আকারের অনুপাত (0 থেকে শুরু, 1-এ শেষ)।

    জোড়ার জায়গায় ধারাবাহিকতা:
      * মান: বড় হওয়া শেষ হয় ঠিক 1-এ, দোলনও শুরু হয় ঠিক 1 থেকে।
      * গতি: বড় হওয়ার শেষ গতি = দোলনের প্রথম গতি
              (= bounce_strength * দোলনের কৌণিক গতি)।
        ঘাতীয় রেখার ঘাত এই শর্ত মেনেই বেছে নেওয়া হয়।
      * শেষ: দোলন শেষ হয় ঠিক 1-এ এবং শেষ গতি সামান্য, তাই থামাটা হঠাৎ নয়।
    """
    t = min(1.0, max(0.0, float(t)))
    if number_of_bounces <= 0 or bounce_strength <= 0:
        # দোলন ছাড়া: মসৃণভাবে বড় হয়ে 1-এ থামা (দুই প্রান্তেই গতি শূন্য)।
        return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)

    grow_portion = min(0.9, max(0.05, float(grow_portion)))
    spring_length = 1.0 - grow_portion
    omega = 2.0 * math.pi * number_of_bounces / spring_length

    if t <= grow_portion:
        u = t / grow_portion
        # জোড়ায় দোলনের গতি (পুরো সময়ের সাপেক্ষে) থেকে বড় হওয়ার
        # নিজস্ব মাপে (u-এর সাপেক্ষে) শেষ ঢাল বের করা।
        end_slope = bounce_strength * omega * grow_portion
        m = _exponent_for_end_slope(end_slope)
        if abs(m) < 1e-12:
            return u
        return math.expm1(m * u) / math.expm1(m)

    phase = (t - grow_portion) / spring_length
    if phase >= 1.0:
        return 1.0
    envelope = math.exp(-float(resistance) * phase)
    return 1.0 + bounce_strength * envelope * math.sin(2.0 * math.pi * number_of_bounces * phase)


class GrowWithBouncing(GrowFromCenter):
    """বস্তুকে কেন্দ্র থেকে বড় করে, গতি না থামিয়ে দোলনে গিয়ে থামায়।

    Create বা Write-এর বদলে ব্যবহার করা যায়:
        self.play(GrowWithBouncing(mob))
        self.play(GrowWithBouncing(mob, number_of_bounces=4, run_time=1.8))

    মাপকাঠি:
        number_of_bounces: আসল আকারের দুই পাশে কতবার দুলবে (পূর্ণ দোলন)।
            প্রাথমিক মান 3। 0 দিলে দোলন ছাড়া শুধু বড় হবে।
        bounce_strength: প্রথম দোলন আসল আকারের চেয়ে কত অংশ বড় হবে।
            প্রাথমিক মান 0.12, অর্থাৎ শতকরা 12 ভাগ।
        resistance: প্রতিরোধ — দোলন কত দ্রুত ছোট হয়ে আসবে।
        grow_portion: মোট সময়ের কত অংশ শুধু বড় হওয়ায় যাবে, বাকিটা দোলনে।
    """

    def __init__(
        self,
        mobject,
        number_of_bounces: int = 3,
        bounce_strength: float = 0.12,
        resistance: float = 3.0,
        grow_portion: float = 0.4,
        point_color=None,
        **kwargs,
    ):
        if int(number_of_bounces) != number_of_bounces or number_of_bounces < 0:
            raise ValueError("number_of_bounces অবশ্যই 0 বা তার বেশি পূর্ণসংখ্যা হতে হবে")
        if bounce_strength < 0:
            raise ValueError("bounce_strength 0 বা তার বেশি হতে হবে")
        if resistance < 0:
            raise ValueError("resistance 0 বা তার বেশি হতে হবে")
        if not 0.05 <= grow_portion <= 0.9:
            raise ValueError("grow_portion 0.05 থেকে 0.9-এর মধ্যে হতে হবে")
        self.number_of_bounces = int(number_of_bounces)
        self.bounce_strength = float(bounce_strength)
        self.resistance = float(resistance)
        self.grow_portion = float(grow_portion)
        kwargs.setdefault(
            "rate_func",
            lambda t: _growth_then_spring(
                t,
                self.number_of_bounces,
                self.bounce_strength,
                self.resistance,
                self.grow_portion,
            ),
        )
        kwargs.setdefault("run_time", 1.6)
        super().__init__(mobject, point_color=point_color, **kwargs)


# পুরনো নামগুলোও রাখা হলো যাতে আগের লেখা ভবিষ্যতে না ভাঙে।
GrowFromCenterBouncy = GrowWithBouncing
GrowWithbouncing = GrowWithBouncing
