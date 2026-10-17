from manim import *
from year2026.logo.logo import *
from year2026.logo.logo import Logo1Fill2Blank


class LogoSimpleScene(Scene):
    def construct(self):
        self.camera.background_color = "#050A12"
        logo_simple(self, Logo1Fill2Blank())


class LogoConstructionScene(Scene):
    def construct(self):
        self.camera.background_color = "#050A12"
        logo_construction(self, Logo1Fill2Blank())


class LogoUnfoldScene(Scene):
    def construct(self):
        self.camera.background_color = "#050A12"
        logo_unfold(self, Logo1Fill2Blank())


class LogoSpinGrowScene(Scene):
    def construct(self):
        self.camera.background_color = "#050A12"
        logo_spin_grow(self, Logo1Fill2Blank())


class LogoTextFirstScene(Scene):
    def construct(self):
        self.camera.background_color = "#050A12"
        logo_text_first(self, Logo1Fill2Blank())


class LogoCascadeScene(Scene):
    def construct(self):
        self.camera.background_color = "#050A12"
        logo_cascade(self, Logo1Fill2Blank())


class LogoExplodeAssembleScene(Scene):
    def construct(self):
        self.camera.background_color = "#050A12"
        logo = Logo1Fill2Blank()
        logo.move_to(ORIGIN)
        logo_explode_assemble(self, logo)


class LogoMorphCircleScene(Scene):
    def construct(self):
        self.camera.background_color = "#050A12"
        logo_morph_circle(self, Logo1Fill2Blank())
