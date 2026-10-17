import random

from manim import *

try:
    from .grow_with_bouncing import GrowWithBouncing
except ImportError:
    from grow_with_bouncing import GrowWithBouncing


class FixedArrow(VGroup):
    def __init__(self, start, end, color=YELLOW, tip_size=0.16, stroke_width=5):
        direction = (end - start) / np.linalg.norm(end - start)
        shaft = Line(start, end - direction * tip_size * 0.6, color=color, stroke_width=stroke_width)
        tip = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0)
        tip.scale(tip_size).rotate(np.arctan2(direction[1], direction[0]) - PI / 2)
        tip.move_to(end - direction * tip_size * 0.6)
        super().__init__(shaft, tip)
        self.shaft = shaft

    def get_start(self):
        return self.shaft.get_start()

    def scale(self, scale_factor, scale_tips=False, **kwargs):
        return super().scale(scale_factor, **kwargs)


class FactrioalScene(MovingCameraScene):
    def hook_s1(self):
        # Three groups (Binomial Theorem, Taylor Series, Combinations) and their boxes.
        binom_title = Text("Binomial Theorem", font="CMU Serif", font_size=38, color=WHITE)
        binom_equation = MathTex(r"(a+b)^n = a^n + na^{n-1}b + \frac{n(n-1)}{2!}a^{n-2}b^2 + \cdots",
                                 substrings_to_isolate=["2!"], font_size=45, color=WHITE)
        taylor_title = Text("Taylor Series", font="CMU Serif", font_size=38, color=WHITE)
        taylor_equation = MathTex(r"e^x = 1+x+\frac{x^2}{2!}+\frac{x^3}{3!}+\cdots",
                                  substrings_to_isolate=["2!", "3!"], font_size=45, color=WHITE)
        combination_title = Text("Combinations", font="CMU Serif", font_size=38, color=WHITE)
        combination_equation = MathTex(r"\binom{n}{r}=\frac{n!}{r!(n-r)!}",
                                       substrings_to_isolate=["n!", "r!", "(n-r)!"], font_size=45, color=WHITE)
        group1 = VGroup(binom_title, binom_equation).arrange(DOWN, buff=0.45)
        group2 = VGroup(taylor_title, taylor_equation).arrange(DOWN, buff=0.45)
        group3 = VGroup(combination_title, combination_equation).arrange(DOWN, buff=0.45)
        self.all_elements = VGroup(group1, group2, group3).arrange(DOWN, buff=0.5)
        self.all_elements.move_to(ORIGIN)
        self.rects = VGroup(
            SurroundingRectangle(binom_equation.get_part_by_tex("2!"), buff=0.1),
            SurroundingRectangle(taylor_equation.get_part_by_tex("2!"), buff=0.1),
            SurroundingRectangle(taylor_equation.get_part_by_tex("3!"), buff=0.1),
            SurroundingRectangle(combination_equation.get_part_by_tex("n!"), buff=0.1),
            SurroundingRectangle(combination_equation.get_part_by_tex("r!"), buff=0.1),
            SurroundingRectangle(combination_equation.get_part_by_tex("(n-r)!"), buff=0)
        )

    def hook_s2(self):
        # Big "!", the 1! to 20! list, its camera sizes, and n! for the centre.
        self.factorial_sign = MathTex(r"!", font_size=240, color=WHITE)
        self.total, self.writing_time, self.lag_ratio = 20, 6, 0.4
        self.lines = VGroup()
        for n in range(1, self.total + 1):
            body = r"\times".join(str(i) for i in range(1, n + 1))
            self.lines.add(MathTex(rf"{n}!={body}", font_size=30, color=WHITE))
        self.lines.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        self.lines.to_corner(UL, buff=0.45)
        self.lines.scale(1.35, about_point=self.lines.get_corner(UL))
        target_ul = self.lines.get_corner(UL) + LEFT * 0.35 + UP * 0.35
        self.target_h = max(self.lines.height + 0.7, (self.lines.width + 0.7) * 9 / 16)
        self.target_w = self.target_h * 16 / 9
        self.target_center = target_ul + RIGHT * self.target_w / 2 + DOWN * self.target_h / 2
        self.start_h = max(target_ul[1] - self.lines[1].get_bottom()[1] + 0.35,
                           (self.lines[1].get_right()[0] - target_ul[0] + 0.35) * 9 / 16)
        self.start_w = self.start_h * 16 / 9
        self.start_center = target_ul + RIGHT * self.start_w / 2 + DOWN * self.start_h / 2
        self.max_end = 1 + self.lag_ratio * (self.total - 1)
        self.n_text = MathTex(r"n! = 1 \times 2 \times 3 \times \cdots \times n", font_size=56, color=WHITE)
        self.n_text.move_to(ORIGIN).set_z_index(2)

    def hook_s3(self):
        self.n_box = Rectangle(width=self.n_text.width + 0.7, height=self.n_text.height + 0.6,
                               fill_color="#050A12", fill_opacity=1, stroke_width=0)
        self.n_box.move_to(ORIGIN).set_z_index(1)
        self.questions = VGroup()
        positions = []
        random.seed(3)
        safe_left, safe_right = self.n_text.get_left()[0] - 0.55, self.n_text.get_right()[0] + 0.55
        safe_bottom, safe_top = self.n_text.get_bottom()[1] - 0.55, self.n_text.get_top()[1] + 0.55
        attempts = 0
        while len(self.questions) < 40 and attempts < 300:
            attempts += 1
            pos = np.array([random.uniform(-config.frame_width / 2 + 0.5, config.frame_width / 2 - 0.5),
                            random.uniform(-config.frame_height / 2 + 0.5, config.frame_height / 2 - 0.5), 0])
            if safe_left < pos[0] < safe_right and safe_bottom < pos[1] < safe_top:
                continue
            if any(np.linalg.norm(pos - old) < 0.8 for old in positions):
                continue
            question = Text("?", font="CMU Serif", font_size=random.randint(24, 42), color=YELLOW)
            question.set_opacity(0.5).rotate(random.uniform(-0.6, 0.6)).move_to(pos).set_z_index(0)
            self.questions.add(question)
            positions.append(pos)

    def camera_sync(self, alpha):
        return min(1.0, alpha * self.max_end / self.lag_ratio / (self.total - 1))

    def make_player(self, letter):
        circle = Circle(radius=0.38, color=WHITE, fill_color=WHITE, fill_opacity=1, stroke_width=3)
        name = Text(letter, font="CMU Serif", font_size=36, color=BLACK, weight=BOLD)
        name.move_to(circle.get_center())
        return VGroup(circle, name)

    def make_field(self):
        field = VGroup()
        ground = Rectangle(width=11.4, height=4.8, color=WHITE, stroke_width=3,
                           fill_color="#17573A", fill_opacity=0.9)
        ground.move_to([0, -0.95, 0])
        middle_line = Line(ground.get_top(), ground.get_bottom(), color=WHITE, stroke_width=3)
        center_circle = Circle(radius=0.75, color=WHITE, stroke_width=3).move_to(ground.get_center())
        center_dot = Dot(point=ground.get_center(), radius=0.05, color=WHITE)
        left_box = Rectangle(width=1.6, height=2.4, color=WHITE, stroke_width=3)
        left_box.move_to([ground.get_left()[0] + 0.8, -0.95, 0])
        right_box = Rectangle(width=1.6, height=2.4, color=WHITE, stroke_width=3)
        right_box.move_to([ground.get_right()[0] - 0.8, -0.95, 0])
        field.add(ground, middle_line, center_circle, center_dot, left_box, right_box)
        self.spots = {"GK": np.array([-4.65, -0.95, 0]), "DF": np.array([0, -0.95, 0]),
                      "ST": np.array([4.65, -0.95, 0])}
        for label, spot in self.spots.items():
            text = Text(label, font="CMU Serif", font_size=26, color=WHITE)
            text.move_to(spot + DOWN * 0.95)
            field.add(text)
        return field

    def make_status_bar(self):
        outline = Rectangle(width=6, height=0.3, color=WHITE, stroke_width=3)
        outline.move_to([0, 3.55, 0])
        fill = Rectangle(width=5.84, height=0.18, stroke_width=0,
                         fill_color=WHITE, fill_opacity=1)
        self.bar_left = outline.get_left()[0] + 0.08
        fill.move_to([self.bar_left + 5.84 / 2, 3.55, 0])
        less = self.make_bar_target(0.45)
        return outline, fill, less


    def make_bar_target(self, level):
        target = Rectangle(width=5.84 * level, height=0.18, stroke_width=0,
                           fill_color="#F6A15C", fill_opacity=1)
        target.move_to([self.bar_left + target.width / 2, 3.55, 0])
        return target

    def swap(self, player1, player2):
        path1 = ArcBetweenPoints(player1.get_center(), player2.get_center(), angle=PI / 3)
        path2 = ArcBetweenPoints(player2.get_center(), player1.get_center(), angle=PI / 3)
        self.play(MoveAlongPath(player1, path1), MoveAlongPath(player2, path2), run_time=1.2)

    def make_blocks(self):
        blocks = VGroup()
        for number in ["1", "2", "3"]:
            square = Square(side_length=1.0, color=WHITE, stroke_width=4)
            label = Text(number, font="CMU Serif", font_size=32, color=WHITE)
            label.next_to(square, DOWN, buff=0.2)
            blocks.add(VGroup(square, label))
        blocks.arrange(RIGHT, buff=0.36)
        blocks.move_to(ORIGIN)
        return blocks

    def hook_s5(self):
        self.question_text = Text("তাহলে তিনজনকে মোট কতভাবে সাজানো যায়?",
                                  font="Noto Serif Bengali", font_size=42, color=WHITE)
        self.question_text.move_to([0, -1.3, 0])
        self.blocks = self.make_blocks()
        self.numbers = VGroup()
        for block, digit in zip(self.blocks, ["3", "2", "1"]):
            number = Text(digit, font="CMU Serif", font_size=40, color=YELLOW)
            number.move_to(block[0].get_center())
            self.numbers.add(number)
        tops = [home + UP * config.frame_height / 3 + DOWN * 0.5 for home in self.home]
        block_tops = [block[0].get_top() + UP * 0.12 for block in self.blocks]
        self.arrows1 = VGroup(*[FixedArrow(tops[i], block_tops[0]) for i in range(3)])
        self.arrows2 = VGroup(*[FixedArrow(tops[i], block_tops[1]) for i in [1, 2]])
        self.arrows3 = VGroup(FixedArrow(tops[2], block_tops[2]))

    def hook_s4(self):
        self.players = VGroup(self.make_player("A"), self.make_player("B"), self.make_player("C"))
        self.players.arrange(RIGHT, buff=0.6).set_z_index(5)
        self.home = [player.get_center().copy() for player in self.players]
        self.field = self.make_field()
        self.bar_outline, self.bar_fill, self.bar_less = self.make_status_bar()
        self.bar_targets = [self.make_bar_target(level) for level in [0.30, 0.48, 0.36, 0.55]]


    def make_tree_node(self, letter):
        circle = Circle(radius=0.26, color=WHITE, fill_color=WHITE, fill_opacity=1, stroke_width=2)
        name = Text(letter, font="CMU Serif", font_size=26, color=BLACK, weight=BOLD)
        name.move_to(circle.get_center())
        return VGroup(circle, name)

    def make_label(self, content, pos, color=WHITE, size=24):
        text = Text(content, font="CMU Serif", font_size=size, color=color)
        text.move_to(pos)
        return text

    def hook_s6(self):
        self.tree_title = Text("Combination Tree", font="CMU Serif", font_size=44, color=WHITE)
        players = ["A", "B", "C"]
        self.tree_root = Dot(point=[-6.2, -0.5, 0], radius=0.08, color=YELLOW)
        self.tree_levels = [[], [], []]
        self.tree_edges = [[], [], []]
        self.tree_nodes = {}
        self.edge_of = {}
        self.tree_paths = []

        def add_node(path, letter, pos, depth):
            node = self.make_tree_node(letter)
            node.move_to(pos)
            self.tree_levels[depth].append(node)
            parent_pos = self.tree_root.get_center() if depth == 0 else self.tree_nodes[path[:-1]].get_center()
            if depth == 2:
                edge = Line(parent_pos, pos, color=WHITE, stroke_width=2)
            else:
                bend = abs(pos[0] - parent_pos[0]) * 0.45
                edge = CubicBezier(parent_pos, parent_pos + RIGHT * bend,
                                   pos + LEFT * bend, pos, color=WHITE, stroke_width=2)
            self.tree_edges[depth].append(edge)
            self.tree_nodes[path] = node
            self.edge_of[path] = edge

        for i, first in enumerate(players):
            y1 = (1 - i) * 2.2 - 0.5
            add_node((first,), first, [-4, y1, 0], 0)
            rest = [p for p in players if p != first]
            for step, second in enumerate(rest):
                y2 = y1 + (0.55 if step == 0 else -0.55)
                add_node((first, second), second, [-1.2, y2, 0], 1)
                third = [p for p in rest if p != second][0]
                add_node((first, second, third), third, [1.6, y2, 0], 2)
                self.tree_paths.append((first, second, third))

        self.tree = VGroup(self.tree_root,
                           *[node for level in self.tree_levels for node in level],
                           *[edge for level in self.tree_edges for edge in level])
        self.tree.scale(0.8)
        self.tree.shift(UP * 0.5)
        col_x = [self.tree_levels[d][0].get_center()[0] for d in range(3)]
        pos_y = self.tree.get_bottom()[1] - 0.5
        choice_y = pos_y - 0.48
        self.pos1 = self.make_label("Position 1", [col_x[0], pos_y, 0])
        self.choice3 = self.make_label("Choice: 3", [col_x[0], choice_y, 0], color=YELLOW)
        self.pos2 = self.make_label("Position 2", [col_x[1], pos_y, 0])
        self.choice2 = self.make_label("Choice: 2", [col_x[1], choice_y, 0], color=YELLOW)
        self.cross1 = self.make_label("×", [(col_x[0] + col_x[1]) / 2, choice_y, 0], color=YELLOW, size=30)
        self.pos3 = self.make_label("Position 3", [col_x[2], pos_y, 0])
        self.choice1 = self.make_label("Choice: 1", [col_x[2], choice_y, 0], color=YELLOW)
        self.cross2 = self.make_label("×", [(col_x[1] + col_x[2]) / 2, choice_y, 0], color=YELLOW, size=30)
        self.tree_equal = self.make_label("=", [col_x[2] + 1.15, choice_y, 0], size=30)
        self.tree_result = self.make_label("6", self.tree_equal.get_center() + RIGHT * 0.55, color=YELLOW, size=32)
        self.arrangements = VGroup()
        self.equation = VGroup(*[MathTex(part, font_size=52, color=WHITE)
                                 for part in [r"3!", "=", "1", r"\times", "2", r"\times", "3", "=", "6"]])
        self.equation.arrange(RIGHT, buff=0.18)
        self.equation.move_to([-1.6, 0, 0])
        self.equation_finals = [token.get_center().copy() for token in self.equation]
        centre = self.equation.get_center()
        for k, token in enumerate(self.equation):
            token.move_to(centre + (self.equation_finals[k] - centre) * 1.8 + (UP if k % 2 == 0 else DOWN) * 0.3)

    def highlight_path(self, path):
        path_edges = VGroup(self.edge_of[path[:1]], self.edge_of[path[:2]], self.edge_of[path])
        highlight = path_edges.copy().set_stroke(color=YELLOW, width=5).set_z_index(3)
        leaf = self.tree_nodes[path].get_center()
        copies = VGroup(self.tree_nodes[path[:1]].copy(), self.tree_nodes[path[:2]].copy(), self.tree_nodes[path].copy())
        copies.set_z_index(4)
        targets = [np.array([4.35 + (k - 1) * 0.62, leaf[1], 0]) for k in range(3)]
        arcs = [ArcBetweenPoints(copies[k].get_center(), targets[k], angle=PI / 4) for k in range(3)]
        self.play(Create(highlight), run_time=0.5)
        self.play(*[MoveAlongPath(copies[k], arcs[k]) for k in range(3)], run_time=0.8)
        self.arrangements.add(copies)
        self.wait(0.25)
        self.play(FadeOut(highlight), run_time=0.3)


    def play_choice_stage(self, stage, remaining, blocks, choices):
        top = blocks[stage].get_top() + UP * 0.1
        arrows = VGroup(*[FixedArrow(man.get_bottom() + DOWN * 0.08, top) for man in remaining])
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.1), run_time=1)
        self.play(FadeOut(arrows), run_time=0.4)
        self.play(Write(choices[stage]), run_time=0.5)
        placer = remaining.pop(0)
        self.play(placer.animate.move_to(blocks[stage].get_center()), run_time=0.8)
        self.wait(0.2)

    def hook_s7(self):
        self.men = VGroup(*[self.make_man(letter) for letter in ["A", "B", "C"]],
                          Text("⋯", font="CMU Serif", font_size=36, color=WHITE),
                          *[self.make_man(letter) for letter in ["L", "M", "N"]])
        self.men.arrange(RIGHT, buff=0.42)
        self.men.move_to([0, 1.95, 0])
        self.man_of = {"A": self.men[0], "B": self.men[1], "C": self.men[2],
                       "L": self.men[4], "M": self.men[5], "N": self.men[6]}
        self.all_men = [self.man_of[letter] for letter in ["A", "B", "C", "L", "M", "N"]]
        block_x = [-3.54 + 1.18 * k for k in range(7)]
        self.g_blocks = VGroup()
        for x in block_x:
            square = Square(side_length=0.78, color=WHITE, stroke_width=4)
            square.move_to([x, 0.2, 0])
            self.g_blocks.add(square)
        self.g_choices = VGroup()
        for k, x in enumerate(block_x):
            choice = MathTex(["n", "(n-1)", "(n-2)", r"\cdots", "3", "2", "1"][k], font_size=30, color=YELLOW)
            choice.move_to([x, -0.75, 0])
            self.g_choices.add(choice)
        self.g_crosses = VGroup(*[Text("×", font="CMU Serif", font_size=26, color=YELLOW) for _ in range(6)])
        for k, cross in enumerate(self.g_crosses):
            gap_x = (self.g_choices[k].get_right()[0] + self.g_choices[k + 1].get_left()[0]) / 2
            cross.move_to([gap_x, -0.75, 0])
        self.n_bang_target = MathTex(r"n!", font_size=52, color=WHITE)
        self.n_bang_target.move_to([0, 3.2, 0])
        self.final_eq = MathTex(r"n! = n \times (n-1) \times (n-2) \times \cdots \times 3 \times 2 \times 1",
                                font_size=40, color=WHITE,
                                substrings_to_isolate=["n!", "=", "n", "(n-1)", "(n-2)",
                                                       r"\cdots", "3", "2", "1", r"\times"])
        self.final_eq.set_color(YELLOW)
        self.final_eq.get_part_by_tex("=").set_color(WHITE)
        self.final_eq.get_part_by_tex("n!").set_color(WHITE)
        self.final_eq.move_to([0, -0.2, 0])
        self.final_eq.set_opacity(0)
        self.choice_targets = [self.final_eq.get_part_by_tex(tex).get_center()
                               for tex in ["n", "(n-1)", "(n-2)", r"\cdots", "3", "2", "1"]]
        cross_parts = [self.final_eq.id_to_vgroup_dict[mid]
                       for tex, mid in self.final_eq.matched_strings_and_ids if tex == r"\times"]
        self.cross_targets = [cross_parts[k].get_center() for k in range(6)]
        self.bang_target = self.final_eq.get_part_by_tex("n!").get_center()
        self.bang_scale = self.final_eq.get_part_by_tex("n!").height / self.n_bang_target.height
        self.final_frame = Rectangle(width=self.final_eq.width + 0.35, height=self.final_eq.height + 0.3,
                                     color=WHITE, stroke_width=4)
        self.final_frame.move_to(self.final_eq.get_center())

    def make_man(self, letter, radius=0.3):
        circle = Circle(radius=radius, color=WHITE, fill_color=WHITE, fill_opacity=1, stroke_width=2)
        name = Text(letter, font="CMU Serif", font_size=28, color=BLACK, weight=BOLD)
        name.move_to(circle.get_center())
        return VGroup(circle, name)

    def construct(self):
        self.camera.background_color = "#050A12"
        self.camera.frame.save_state()
        self.hook_s1()
        self.hook_s2()
        self.hook_s3()
        self.hook_s4()
        self.hook_s5()
        self.hook_s6()
        self.hook_s7()
        self.wait(1)
        self.play(LaggedStart(*[FadeIn(i, shift=DOWN) for i in self.all_elements], lag_ratio=1))
        self.wait(1)
        self.play(LaggedStart(*[Create(rect) for rect in self.rects], lag_ratio=0.6))
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.play(GrowWithBouncing(self.factorial_sign, number_of_bounces=3))
        self.wait(0.5)
        self.play(ShrinkToCenter(self.factorial_sign))
        self.play(self.camera.frame.animate.set_width(self.start_w).set_height(self.start_h).move_to(self.start_center), run_time=0.8)
        self.play(LaggedStart(*[Write(line, run_time=1) for line in self.lines],
                              lag_ratio=self.lag_ratio, rate_func=linear, run_time=self.writing_time),
                  self.camera.frame.animate(rate_func=self.camera_sync).set_width(self.target_w).set_height(self.target_h).move_to(self.target_center),
                  run_time=self.writing_time)
        self.wait(0.5)
        self.play(Restore(self.camera.frame, run_time=1), FadeOut(self.lines, run_time=1))
        self.play(Write(self.n_text))
        self.wait(0.3)
        self.play(ApplyWave(self.n_text, amplitude=0.25, run_time=1.5))
        self.wait(0.3)
        self.add(self.n_box)
        self.play(LaggedStart(*[FadeIn(q, scale=0.5, run_time=0.5) for q in self.questions], lag_ratio=0.18))
        self.wait(1)
        self.play(LaggedStart(*[FadeOut(q, run_time=0.4) for q in self.questions], lag_ratio=0.06))
        self.play(FadeOut(self.n_text), FadeOut(self.n_box))
        self.wait(0.5)
        self.play(LaggedStart(*[FadeIn(player, scale=0.5) for player in self.players], lag_ratio=0.3))
        self.wait(0.5)
        self.play(self.players.animate.to_edge(UP, buff=0.7))
        self.play(DrawBorderThenFill(self.field), run_time=2)
        self.wait(0.3)
        self.play(self.players[0].animate.move_to(self.spots["GK"]),
                  self.players[2].animate.move_to(self.spots["DF"]),
                  self.players[1].animate.move_to(self.spots["ST"]), run_time=1.2)
        self.play(Create(self.bar_outline), FadeIn(self.bar_fill))
        self.swap(self.players[0], self.players[1])
        self.wait(1)
        self.play(Transform(self.bar_fill, self.bar_less), run_time=0.8)
        for (first, second), target in zip([(1, 2), (1, 0), (2, 1), (1, 0)], self.bar_targets):
            self.swap(self.players[first], self.players[second])
            self.play(Transform(self.bar_fill, target), run_time=0.5)
            self.wait(0.3)
        self.play(FadeOut(self.field), FadeOut(self.bar_outline), FadeOut(self.bar_fill))
        self.play(*[player.animate.move_to(self.home[i]) for i, player in enumerate(self.players)], run_time=1.2)
        self.wait(0.3)
        self.play(Write(self.question_text))
        self.wait(1)
        self.play(Unwrite(self.question_text))
        self.play(self.players.animate.move_to(UP * config.frame_height / 3), run_time=1)
        self.play(LaggedStart(*[Create(block[0]) for block in self.blocks], lag_ratio=0.3))
        self.play(LaggedStart(*[Write(block[1]) for block in self.blocks], lag_ratio=0.3))
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in self.arrows1], lag_ratio=0.25))
        self.wait(0.3)
        self.play(FadeOut(self.arrows1))
        self.play(Write(self.numbers[0]))
        self.wait(0.3)
        self.play(self.players[0].animate.move_to(self.blocks[0][0].get_center()), run_time=1)
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in self.arrows2], lag_ratio=0.25))
        self.wait(0.3)
        self.play(FadeOut(self.arrows2))
        self.play(Write(self.numbers[1]))
        self.wait(0.3)
        self.play(self.players[1].animate.move_to(self.blocks[1][0].get_center()), run_time=1)
        self.play(GrowArrow(self.arrows3[0]))
        self.wait(0.3)
        self.play(FadeOut(self.arrows3))
        self.play(Write(self.numbers[2]))
        self.wait(0.3)
        self.play(self.players[2].animate.move_to(self.blocks[2][0].get_center()), run_time=1)
        self.wait(1)
        self.play(FadeOut(self.players), FadeOut(self.blocks), *[FadeOut(n) for n in self.numbers])
        self.wait(0.5)
        self.play(Write(self.tree_title))
        self.wait(0.4)
        self.play(self.tree_title.animate.to_edge(UP, buff=0.45), run_time=0.8)
        self.play(FadeIn(self.tree_root, scale=0.5))
        self.play(LaggedStart(*[Create(edge) for edge in self.tree_edges[0]], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(node, scale=0.5) for node in self.tree_levels[0]], lag_ratio=0.15), run_time=1.2)
        self.play(Write(self.pos1))
        self.play(Write(self.choice3))
        self.play(LaggedStart(*[Create(edge) for edge in self.tree_edges[1]], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(node, scale=0.5) for node in self.tree_levels[1]], lag_ratio=0.15), run_time=1.2)
        self.play(Write(self.pos2))
        self.play(Write(self.choice2))
        self.play(Write(self.cross1))
        self.play(LaggedStart(*[Create(edge) for edge in self.tree_edges[2]], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(node, scale=0.5) for node in self.tree_levels[2]], lag_ratio=0.15), run_time=1.2)
        self.play(Write(self.pos3))
        self.play(Write(self.choice1))
        self.play(Write(self.cross2))
        self.play(Write(self.tree_equal))
        for path in self.tree_paths:
            self.highlight_path(path)
        self.play(Write(self.tree_result))
        self.wait(0.5)
        self.add(self.equation)
        self.play(FadeOut(self.tree), FadeOut(self.tree_title), FadeOut(self.pos1), FadeOut(self.choice3), FadeOut(self.cross1),
                  FadeOut(self.pos2), FadeOut(self.choice2), FadeOut(self.cross2), FadeOut(self.pos3), FadeOut(self.choice1),
                  FadeOut(self.tree_equal), FadeOut(self.tree_result),
                  *[token.animate.move_to(self.equation_finals[k]) for k, token in enumerate(self.equation)], run_time=1.4)
        self.wait(0.3)
        self.play(LaggedStartMap(Indicate, self.equation, lag_ratio=0.3))
        self.play(LaggedStart(*[Indicate(row, scale_factor=1.15) for row in self.arrangements], lag_ratio=0.3))
        self.wait(0.5)
        self.play(LaggedStart(*[FadeOut(row) for row in self.arrangements], lag_ratio=0.15),
                  self.equation.animate.move_to(ORIGIN), run_time=1.2)
        self.wait(0.3)
        self.play(Transform(self.equation[0], self.n_bang_target), *[FadeOut(token) for token in self.equation[1:]], run_time=1)
        n_bang = self.equation[0]
        self.play(LaggedStart(*[FadeIn(man, scale=0.5) for man in self.men], lag_ratio=0.1))
        self.wait(0.3)
        self.play(LaggedStart(*[Create(block) for block in self.g_blocks], lag_ratio=0.15))
        self.wait(0.3)
        remaining = list(self.all_men)
        for stage in range(3):
            self.play_choice_stage(stage, remaining, self.g_blocks, self.g_choices)
        self.play(Write(self.g_choices[3]), run_time=0.5)
        self.wait(0.2)
        remaining_final = [self.man_of[letter] for letter in ["L", "M", "N"]]
        for stage in [4, 5, 6]:
            self.play_choice_stage(stage, remaining_final, self.g_blocks, self.g_choices)
        self.play(LaggedStart(*[FadeIn(cross, scale=0.5) for cross in self.g_crosses], lag_ratio=0.12))
        self.wait(0.5)
        self.add(self.final_eq)
        self.play(FadeOut(self.g_blocks), FadeOut(self.men),
                  *[choice.animate.move_to(self.choice_targets[k]) for k, choice in enumerate(self.g_choices)],
                  *[cross.animate.move_to(self.cross_targets[k]) for k, cross in enumerate(self.g_crosses)],
                  n_bang.animate.move_to(self.bang_target).scale(self.bang_scale), run_time=1.3)
        self.play(self.final_eq.animate.set_opacity(1), FadeOut(self.g_choices), FadeOut(self.g_crosses), FadeOut(n_bang), run_time=0.5)
        self.play(ShowPassingFlash(self.final_frame, time_width=0.15), run_time=1.4)
        self.wait(1)
