from manim import *
import numpy as np

GREEN = "#1D9E75"


class Logo1Fill2Blank(VGroup):
    def __init__(self, radius=1.5, font_size=72, color=GREEN, **kwargs):
        super().__init__(**kwargs)
        self.logo_radius = radius

        sector_filled = Sector(
            radius=radius, start_angle=PI/6, angle=2*PI/3,
        ).set_fill(color=color, opacity=1).set_stroke(color=WHITE, width=2)

        sector_blank1 = Sector(
            radius=radius, start_angle=PI/6 + 2*PI/3, angle=2*PI/3,
        ).set_fill(opacity=0).set_stroke(color=WHITE, width=2)

        sector_blank2 = Sector(
            radius=radius, start_angle=PI/6 + 4*PI/3, angle=2*PI/3,
        ).set_fill(opacity=0).set_stroke(color=WHITE, width=2)

        self.sectors = VGroup(sector_filled, sector_blank1, sector_blank2)
        self.label = Text("1fill2blank", font="CMU Serif", font_size=font_size)
        self.label.next_to(self.sectors, DOWN, buff=0.35)

        self.add(self.sectors, self.label)


# ━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. Simple
# ━━━━━━━━━━━━━━━━━━━━━━━━━
def logo_simple(scene, logo, wait_time=3):
    scene.play(
        Create(logo.sectors, lag_ratio=0.4, rate_func=smooth),
        run_time=3
    )
    scene.play(Write(logo.label, rate_func=smooth), run_time=1.5)
    scene.wait(wait_time)


# ━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. Construction
# Circle → lines → sectors
# ━━━━━━━━━━━━━━━━━━━━━━━━━
def logo_construction(scene, logo, wait_time=3):
    radius = logo.logo_radius
    circle = Circle(radius=radius).set_stroke(color=WHITE, width=2)
    angles = [PI/6, PI/6 + 2*PI/3, PI/6 + 4*PI/3]
    lines = VGroup(*[
        Line(ORIGIN, radius * np.array([np.cos(a), np.sin(a), 0]))
        .set_stroke(color=WHITE, width=1.5)
        for a in angles
    ])
    scene.play(Create(circle, rate_func=smooth), run_time=1.5)
    scene.wait(0.2)
    scene.play(
        LaggedStart(*[Create(l) for l in lines], lag_ratio=0.5),
        run_time=2
    )
    scene.wait(0.4)
    scene.play(
        FadeOut(circle),
        FadeOut(lines),
        FadeIn(logo.sectors),
        run_time=0.8
    )
    scene.wait(0.3)
    scene.play(Write(logo.label, rate_func=smooth), run_time=1.5)
    scene.wait(wait_time)


# ━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. Unfold
# Sectors একটার পর একটা center থেকে বের হয়
# ━━━━━━━━━━━━━━━━━━━━━━━━━
def logo_unfold(scene, logo, wait_time=3):
    scene.play(
        LaggedStart(
            *[GrowFromCenter(s, rate_func=smooth) for s in logo.sectors],
            lag_ratio=0.6
        ),
        run_time=3
    )
    scene.wait(0.2)
    scene.play(Write(logo.label, rate_func=smooth), run_time=1.5)
    scene.wait(wait_time)


# ━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. Spin Grow
# ঘুরতে ঘুরতে বড় হয়
# ━━━━━━━━━━━━━━━━━━━━━━━━━
def logo_spin_grow(scene, logo, wait_time=3):
    scene.play(GrowFromCenter(logo.sectors, rate_func=smooth), run_time=1.2)
    scene.play(Rotate(logo.sectors, angle=2*PI, rate_func=smooth), run_time=1.3)
    scene.wait(0.2)
    scene.play(Write(logo.label, rate_func=smooth), run_time=1.5)
    scene.wait(wait_time)


# ━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. Text First
# আগে text, তারপর logo উপরে আসে
# ━━━━━━━━━━━━━━━━━━━━━━━━━
def logo_text_first(scene, logo, wait_time=3):
    temp_label = logo.label.copy().move_to(ORIGIN)
    scene.play(Write(temp_label, rate_func=smooth), run_time=2)
    scene.wait(0.4)
    scene.play(
        ReplacementTransform(temp_label, logo.label),
        GrowFromCenter(logo.sectors, rate_func=smooth),
        run_time=2
    )
    scene.wait(wait_time)


# ━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. Cascade
# Blank গুলো আগে, filled শেষে
# ━━━━━━━━━━━━━━━━━━━━━━━━━
def logo_cascade(scene, logo, wait_time=3):
    scene.play(
        LaggedStart(
            FadeIn(logo.sectors[1], shift=DOWN * 0.3),
            FadeIn(logo.sectors[2], shift=DOWN * 0.3),
            FadeIn(logo.sectors[0], shift=UP * 0.3),
            lag_ratio=0.5
        ),
        run_time=2.5
    )
    scene.wait(0.2)
    scene.play(Write(logo.label, rate_func=smooth), run_time=1.5)
    scene.wait(wait_time)


# ━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. Explode Assemble (fixed)
# Sectors আলাদা হয়ে আসে, তারপর জোড়া লাগে
# ━━━━━━━━━━━━━━━━━━━━━━━━━
def logo_explode_assemble(scene, logo, wait_time=3):
    sectors = [logo.sectors[0], logo.sectors[1], logo.sectors[2]]
    offsets = [
        0.42 * UP,
        0.42 * np.array([np.cos(7*PI/6), np.sin(7*PI/6), 0]),
        0.42 * np.array([np.cos(11*PI/6), np.sin(11*PI/6), 0]),
    ]

    for s, o in zip(sectors, offsets):
        s.shift(o)

    # Draw separated
    scene.play(
        LaggedStart(
            DrawBorderThenFill(sectors[0]),
            Create(sectors[1]),
            Create(sectors[2]),
            lag_ratio=0.4,
        ),
        run_time=3.0
    )
    scene.wait(0.5)

    # Assemble smoothly — no bounce
    scene.play(
        *[s.animate.shift(-o) for s, o in zip(sectors, offsets)],
        rate_func=smooth,
        run_time=1.2
    )
    scene.wait(0.3)

    # Write name
    scene.play(Write(logo.label, rate_func=smooth), run_time=1.5)
    scene.wait(wait_time)


# ━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. Morph Circle
# পুরো circle → 1/3 logo তে রূপান্তর
# ━━━━━━━━━━━━━━━━━━━━━━━━━
def logo_morph_circle(scene, logo, wait_time=3):
    full_circle = Circle(radius=logo.logo_radius).set_fill(
        color=GREEN, opacity=1
    ).set_stroke(color=WHITE, width=2)

    scene.play(GrowFromCenter(full_circle, rate_func=smooth), run_time=1.5)
    scene.wait(0.4)
    scene.play(
        FadeOut(full_circle),
        FadeIn(logo.sectors),
        run_time=1.5
    )
    scene.wait(0.3)
    scene.play(Write(logo.label, rate_func=smooth), run_time=1.5)
    scene.wait(wait_time)
