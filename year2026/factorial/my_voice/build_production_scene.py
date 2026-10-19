#!/usr/bin/env python3
"""Build the own-voice Factorial production scene from the base ManimCE scene.

Only timing/logo synchronisation is added. The visual design and animation
logic of ``factorial_scene.py`` are preserved. Every replacement is anchored
to an exact unique string in the base scene; if the base scene changes, the
builder fails loudly instead of producing a silently wrong scene.

Defaults (when this file lives in ``year2026/factorial/my_voice/``):
    base scene : ../factorial_scene.py
    output     : ../factorial_myvoice_production.py

The generated scene reads pads/marks from ``my_voice/timing/`` beside it,
overridable with the ``VOICE_PAD_FILE`` / ``SCENE_MARKS_FILE`` env vars.

Examples:
    python build_production_scene.py
    python build_production_scene.py --base /path/to/factorial_scene.py \
        --output /path/to/factorial_myvoice_production.py
"""
from __future__ import annotations

import argparse
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
_parser = argparse.ArgumentParser(description="Generate factorial_myvoice_production.py from factorial_scene.py")
_parser.add_argument("--base", type=pathlib.Path, default=HERE.parent / "factorial_scene.py",
                     help="base scene (default: ../factorial_scene.py)")
_parser.add_argument("--output", type=pathlib.Path, default=HERE.parent / "factorial_myvoice_production.py",
                     help="generated scene (default: ../factorial_myvoice_production.py)")
_args = _parser.parse_args()

SRC = _args.base.expanduser()
DST = _args.output.expanduser()
if not SRC.is_file():
    sys.exit(f"base scene not found: {SRC}")
src = SRC.read_text(encoding="utf-8")


def sub(old: str, new: str) -> None:
    global src
    n = src.count(old)
    if n != 1:
        sys.exit(f"ANCHOR FAIL ({n}x): {old[:120]!r}")
    src = src.replace(old, new, 1)


# Imports, pad/mark file handling, logo import.
sub(
    """try:\n    from .grow_with_bouncing import GrowWithBouncing\nexcept ImportError:\n    from grow_with_bouncing import GrowWithBouncing\n""",
    """try:\n    from .grow_with_bouncing import GrowWithBouncing\nexcept ImportError:\n    from grow_with_bouncing import GrowWithBouncing\n\nimport json\nimport os\n\ntry:\n    from year2026.logo.logo import Logo1Fill2Blank, logo_explode_assemble\nexcept ImportError:  # pragma: no cover\n    from my_1fill2blank import Logo1Fill2Blank, logo_explode_assemble\n\n_HERE = os.path.dirname(os.path.abspath(__file__))\n_PAD_FILE = os.environ.get(\"VOICE_PAD_FILE\", os.path.join(_HERE, \"my_voice\", \"timing\", \"pad_myvoice.json\"))\n_MARKS_FILE = os.environ.get(\"SCENE_MARKS_FILE\", os.path.join(_HERE, \"my_voice\", \"timing\", \"marks_myvoice.json\"))\n\n\ndef _load_pads():\n    try:\n        with open(_PAD_FILE, \"r\", encoding=\"utf-8\") as f:\n            data = json.load(f)\n        return data if isinstance(data, dict) else {}\n    except Exception:\n        return {}\n\n\n_VOICE_PADS = _load_pads()\n""",
)

# Helper methods.
sub(
    "    def camera_sync(self, alpha):",
    '''    def _scene_time(self):\n        try:\n            vale = getattr(getattr(self, "renderer", None), "time", None)\n            if vale is not None:\n                return float(vale() if callable(vale) else vale)\n        except Exception:\n            pass\n        try:\n            vale = getattr(self, "time", None)\n            return float(vale() if callable(vale) else vale)\n        except Exception:\n            return 0.0\n\n    def mark(self, name):\n        t = self._scene_time()\n        data = {}\n        if _MARKS_FILE and os.path.exists(_MARKS_FILE):\n            try:\n                with open(_MARKS_FILE, "r", encoding="utf-8") as f:\n                    data = json.load(f)\n            except Exception:\n                data = {}\n        data[name] = t\n        try:\n            folder = os.path.dirname(_MARKS_FILE)\n            if folder:\n                os.makedirs(folder, exist_ok=True)\n            with open(_MARKS_FILE, "w", encoding="utf-8") as f:\n                json.dump(data, f, indent=2)\n        except Exception:\n            pass\n        print(f"[MARK] {name} @ {t:.3f}")\n        try:\n            self.next_section(name)\n        except Exception:\n            pass\n\n    def pad(self, key):\n        try:\n            t = float(_VOICE_PADS.get(key, 0.0))\n        except Exception:\n            t = 0.0\n        if t > 0.02:\n            self.wait(t)\n\n    def show_logo(self, wait_time=2):\n        logo = Logo1Fill2Blank()\n        logo.move_to(ORIGIN)\n        logo_explode_assemble(self, logo, wait_time=wait_time)\n        return logo\n\n    def camera_sync(self, alpha):''',
)

# Slightly faster six-path highlighting: timing only, same visual design.
sub(
    """        self.play(Create(highlight), run_time=0.5)\n        self.play(*[MoveAlongPath(copies[k], arcs[k]) for k in range(3)], run_time=0.8)\n        self.arrangements.add(copies)\n        self.wait(0.25)\n        self.play(FadeOut(highlight), run_time=0.3)""",
    """        self.play(Create(highlight), run_time=0.32)\n        self.play(*[MoveAlongPath(copies[k], arcs[k]) for k in range(3)], run_time=0.55)\n        self.arrangements.add(copies)\n        self.wait(0.10)\n        self.play(FadeOut(highlight), run_time=0.18)""",
)

# Start / M01.
sub(
    "        self.hook_s7()\n        self.wait(1)",
    """        self.hook_s7()\n        if _MARKS_FILE and os.path.exists(_MARKS_FILE):\n            try:\n                os.remove(_MARKS_FILE)\n            except Exception:\n                pass\n        self.mark("M01")\n        self.wait(1)""",
)

# M01 -> M02.
sub(
    """        self.wait(2)\n        self.play(*[FadeOut(mob) for mob in self.mobjects])""",
    """        self.wait(2)\n        self.pad("M01")\n        self.mark("M02")\n        self.play(*[FadeOut(mob) for mob in self.mobjects])""",
)

# M02 -> M03, just before the 1!..20! list.
sub(
    """        self.play(self.camera.frame.animate.set_width(self.start_w).set_height(self.start_h).move_to(self.start_center), run_time=0.8)""",
    """        self.play(self.camera.frame.animate.set_width(self.start_w).set_height(self.start_h).move_to(self.start_center), run_time=0.8)\n        self.pad("M02")\n        self.mark("M03")""",
)

# M03 -> M04, before restoring camera and writing n!.
sub(
    """        self.wait(0.5)\n        self.play(Restore(self.camera.frame, run_time=1), FadeOut(self.lines, run_time=1))""",
    """        self.wait(0.5)\n        self.pad("M03")\n        self.mark("M04")\n        self.play(Restore(self.camera.frame, run_time=1), FadeOut(self.lines, run_time=1))""",
)

# M04 -> logo.
sub(
    """        self.play(LaggedStart(*[FadeIn(q, scale=0.5, run_time=0.5) for q in self.questions], lag_ratio=0.18))\n        self.wait(1)""",
    """        self.play(LaggedStart(*[FadeIn(q, scale=0.5, run_time=0.5) for q in self.questions], lag_ratio=0.18))\n        self.wait(1)\n        self.pad("M04")\n        self.mark("LOGO_MID")""",
)

# Mid logo, then M05.
sub(
    """        self.play(FadeOut(self.n_text), FadeOut(self.n_box))\n        self.wait(0.5)\n        self.play(LaggedStart(*[FadeIn(player, scale=0.5) for player in self.players], lag_ratio=0.3))""",
    """        self.play(FadeOut(self.n_text), FadeOut(self.n_box))\n        self.wait(0.5)\n        logo_front = self.show_logo(wait_time=2)\n        self.play(FadeOut(logo_front))\n        self.mark("M05")\n        self.play(LaggedStart(*[FadeIn(player, scale=0.5) for player in self.players], lag_ratio=0.3))""",
)

# M05 -> M06 -> M07.
sub(
    """        self.wait(0.5)\n        self.play(self.players.animate.to_edge(UP, buff=0.7))\n        self.play(DrawBorderThenFill(self.field), run_time=2)""",
    """        self.wait(0.5)\n        self.pad("M05")\n        self.mark("M06")\n        self.play(self.players.animate.to_edge(UP, buff=0.7))\n        self.pad("M06")\n        self.mark("M07")\n        self.play(DrawBorderThenFill(self.field), run_time=2)""",
)

# M07 -> M08 (hold initial line-up) -> M09 (the swap itself).
sub(
    """        self.play(Create(self.bar_outline), FadeIn(self.bar_fill))\n        self.swap(self.players[0], self.players[1])""",
    """        self.play(Create(self.bar_outline), FadeIn(self.bar_fill))\n        self.pad("M07")\n        self.mark("M08")\n        self.pad("M08")\n        self.mark("M09")\n        self.swap(self.players[0], self.players[1])""",
)

# Split the swap loop: M10 gets first two, M11 the last two.
sub(
    """        for (first, second), target in zip([(1, 2), (1, 0), (2, 1), (1, 0)], self.bar_targets):\n            self.swap(self.players[first], self.players[second])\n            self.play(Transform(self.bar_fill, target), run_time=0.5)\n            self.wait(0.3)""",
    """        self.pad("M09")\n        self.mark("M10")\n        for _swap_i, ((first, second), target) in enumerate(zip([(1, 2), (1, 0), (2, 1), (1, 0)], self.bar_targets)):\n            self.swap(self.players[first], self.players[second])\n            self.play(Transform(self.bar_fill, target), run_time=0.5)\n            self.wait(0.3)\n            if _swap_i == 1:\n                self.pad("M10")\n                self.mark("M11")""",
)

# M11 -> M12 -> M13 -> M14.
sub(
    """        self.play(FadeOut(self.field), FadeOut(self.bar_outline), FadeOut(self.bar_fill))""",
    """        self.pad("M11")\n        self.mark("M12")\n        self.play(FadeOut(self.field), FadeOut(self.bar_outline), FadeOut(self.bar_fill))""",
)
sub(
    """        self.wait(0.3)\n        self.play(Write(self.question_text))\n        self.wait(1)\n        self.play(Unwrite(self.question_text))""",
    """        self.wait(0.3)\n        self.pad("M12")\n        self.mark("M13")\n        self.play(Write(self.question_text))\n        self.wait(1)\n        self.pad("M13")\n        self.play(Unwrite(self.question_text))\n        self.mark("M14")""",
)

# M14 ends after blocks and their labels are created.
sub(
    """        self.play(LaggedStart(*[Write(block[1]) for block in self.blocks], lag_ratio=0.3))""",
    """        self.play(LaggedStart(*[Write(block[1]) for block in self.blocks], lag_ratio=0.3))\n        self.pad("M14")\n        self.mark("M15")""",
)

# Three choice stages.
sub(
    """        self.play(Write(self.numbers[0]))\n        self.wait(0.3)\n        self.play(self.players[0].animate.move_to(self.blocks[0][0].get_center()), run_time=1)""",
    """        self.play(Write(self.numbers[0]))\n        self.wait(0.3)\n        self.pad("M15")\n        self.mark("M16")\n        self.play(self.players[0].animate.move_to(self.blocks[0][0].get_center()), run_time=1)\n        self.pad("M16")\n        self.mark("M17")""",
)
sub(
    """        self.play(Write(self.numbers[1]))\n        self.wait(0.3)\n        self.play(self.players[1].animate.move_to(self.blocks[1][0].get_center()), run_time=1)""",
    """        self.play(Write(self.numbers[1]))\n        self.wait(0.3)\n        self.pad("M17")\n        self.mark("M18")\n        self.play(self.players[1].animate.move_to(self.blocks[1][0].get_center()), run_time=1)""",
)
sub(
    """        self.play(Write(self.numbers[2]))\n        self.wait(0.3)\n        self.play(self.players[2].animate.move_to(self.blocks[2][0].get_center()), run_time=1)\n        self.wait(1)""",
    """        self.play(Write(self.numbers[2]))\n        self.wait(0.3)\n        self.pad("M18")\n        self.mark("M19")\n        self.play(self.players[2].animate.move_to(self.blocks[2][0].get_center()), run_time=1)\n        self.wait(1)\n        self.pad("M19")\n        self.mark("M20")""",
)

# Tree title/root; narrate levels while the title settles and root appears,
# then hold the root before building level 1.
sub(
    """        self.play(self.tree_title.animate.to_edge(UP, buff=0.45), run_time=0.8)""",
    """        self.pad("M20")\n        self.mark("M21")\n        self.play(self.tree_title.animate.to_edge(UP, buff=0.45), run_time=0.8)""",
)
sub(
    """        self.play(FadeIn(self.tree_root, scale=0.5))""",
    """        self.play(FadeIn(self.tree_root, scale=0.5))\n        self.pad("M21")\n        self.mark("M22")""",
)

# Tree level 1 -> level 2.
sub(
    """        self.play(Write(self.choice3))""",
    """        self.play(Write(self.choice3))\n        self.pad("M22")\n        self.mark("M23")""",
)

# After level 2, stay on the two-level tree for M24-M26.
sub(
    """        self.play(Write(self.cross1))""",
    """        self.play(Write(self.cross1))\n        self.pad("M23")\n        self.mark("M24")\n        self.pad("M24")\n        self.mark("M25")\n        self.pad("M25")\n        self.mark("M26")\n        self.pad("M26")\n        self.mark("M27")""",
)

# Level 3 labels.
sub(
    """        self.play(Write(self.pos3))\n        self.play(Write(self.choice1))""",
    """        self.play(Write(self.pos3))\n        self.pad("M27")\n        self.mark("M28")\n        self.play(Write(self.choice1))""",
)
sub(
    """        self.play(Write(self.tree_equal))""",
    """        self.play(Write(self.tree_equal))\n        self.pad("M28")\n        self.mark("M29")""",
)

# Six paths / result; hold complete tree for M30 before equation assembly.
sub(
    """        self.play(Write(self.tree_result))\n        self.wait(0.5)""",
    """        self.play(Write(self.tree_result))\n        self.wait(0.5)\n        self.pad("M29")\n        self.mark("M30")\n        self.pad("M30")\n        self.mark("M31")""",
)

# General-n transition.
sub(
    """        self.play(LaggedStart(*[Indicate(row, scale_factor=1.15) for row in self.arrangements], lag_ratio=0.3))\n        self.wait(0.5)""",
    """        self.play(LaggedStart(*[Indicate(row, scale_factor=1.15) for row in self.arrangements], lag_ratio=0.3))\n        self.wait(0.5)\n        self.pad("M31")\n        self.mark("M32")""",
)

# Unroll general choice stages so every spoken stage can start its own action.
sub(
    """        remaining = list(self.all_men)\n        for stage in range(3):\n            self.play_choice_stage(stage, remaining, self.g_blocks, self.g_choices)\n        self.play(Write(self.g_choices[3]), run_time=0.5)\n        self.wait(0.2)\n        remaining_final = [self.man_of[letter] for letter in ["L", "M", "N"]]\n        for stage in [4, 5, 6]:\n            self.play_choice_stage(stage, remaining_final, self.g_blocks, self.g_choices)""",
    """        self.pad("M32")\n        self.mark("M33")\n        remaining = list(self.all_men)\n        self.play_choice_stage(0, remaining, self.g_blocks, self.g_choices)\n        self.pad("M33")\n        self.mark("M34")\n        self.play_choice_stage(1, remaining, self.g_blocks, self.g_choices)\n        self.pad("M34")\n        self.mark("M35")\n        self.play_choice_stage(2, remaining, self.g_blocks, self.g_choices)\n        self.pad("M35")\n        self.mark("M36")\n        self.play(Write(self.g_choices[3]), run_time=0.5)\n        self.wait(0.2)\n        self.pad("M36")\n        self.mark("M37")\n        remaining_final = [self.man_of[letter] for letter in ["L", "M", "N"]]\n        for stage in [4, 5, 6]:\n            self.play_choice_stage(stage, remaining_final, self.g_blocks, self.g_choices)\n        self.pad("M37")\n        self.mark("M38")""",
)

# Product crosses, final equation, closing, outro.
sub(
    """        self.play(LaggedStart(*[FadeIn(cross, scale=0.5) for cross in self.g_crosses], lag_ratio=0.12))\n        self.wait(0.5)""",
    """        self.play(LaggedStart(*[FadeIn(cross, scale=0.5) for cross in self.g_crosses], lag_ratio=0.12))\n        self.wait(0.5)\n        self.pad("M38")\n        self.mark("M39")\n        self.wait(2.2)""",
)
sub(
    """        self.play(ShowPassingFlash(self.final_frame, time_width=0.15), run_time=1.4)\n        self.wait(1)""",
    """        self.play(ShowPassingFlash(self.final_frame, time_width=0.15), run_time=1.4)\n        self.wait(1)\n        self.pad("M39")\n        self.mark("M40")\n        self.pad("M40")\n        self.mark("OUTRO")\n        self.play(FadeOut(self.final_eq))\n        self.show_logo(wait_time=3)\n        self.mark("END")""",
)

HEADER = (
    "# GENERATED by my_voice/build_production_scene.py from factorial_scene.py.\n"
    "# Do not edit by hand: change the base scene or the builder, then regenerate.\n"
    "# Pads/marks default to my_voice/timing/ beside this file "
    "(env: VOICE_PAD_FILE / SCENE_MARKS_FILE).\n"
)
DST.parent.mkdir(parents=True, exist_ok=True)
DST.write_text(HEADER + src, encoding="utf-8")
print("WROTE", DST, len((HEADER + src).splitlines()), "lines")
