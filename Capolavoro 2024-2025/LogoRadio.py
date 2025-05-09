from manim import *
import random

class LogoRadio(Scene):
    def construct(self):
        self.renderer.camera.frame_rate = 120
        self.camera.background_color = "#FFF5E1"

        dell_erba = Text(
            "DELL'ERBA",
            font_size=30,
            font="Aerospace Bold",
        ).set_color("#FF0000").shift(UP * 0.8 + LEFT * 0.9 + RIGHT * 0.1)  # Spostato verso sinistra di pochissimo

        voice = Text(
            "VOICE",
            font_size=74,
            font="Aerospace Bold",
            weight=BOLD
        ).set_color("#FF0000").next_to(dell_erba, DOWN, buff=0.2).shift(LEFT * 0.7 + RIGHT * 1.2)  # Spostato verso destra
        shadow = voice.copy().set_color("#FF4C4C").shift(RIGHT * 0.04 + UP * 0.04)
        shadow2 = voice.copy().set_color("#FF9999").shift(RIGHT * 0.08 + UP * 0.08)

        line_positions = [-1.8, -1.2, -0.6, 0, 0.6, 1.2, 1.8]
        final_heights = [2.5, 1.8, 2.5 / 3 + 0.5, 2.5 / 3 - 0.5, 1.5, 1.0, 0.5]

        stroke_w = 19  # larghezza linea
        radius_match = 0.095  # raggio cerchio

        lines = []
        caps_top = []
        caps_bottom = []

        # Calcolare la larghezza di "VOICE"
        voice_width = voice.width

        # Creare linee con la simmetria nelle altezze
        for i, x in enumerate(line_positions):
            # Se è la sesta linea, aumentiamo la sua lunghezza basandoci sulla larghezza di "VOICE"
            if i == 5:  # sesta linea
                height = voice_width * 0.8  # Impostiamo la lunghezza della sesta linea un po' più lunga di "VOICE"
            else:
                height = final_heights[i]
            
            line = Line(
                start=[x, -2.5, 0],
                end=[x, height, 0],
                color="#D3B0E0",
                stroke_width=stroke_w
            )
            cap_top = Dot(point=[x, height, 0], radius=radius_match, color="#D3B0E0")
            cap_bottom = Dot(point=[x, -2.5, 0], radius=radius_match, color="#D3B0E0")
            lines.append(line)
            caps_top.append(cap_top)
            caps_bottom.append(cap_bottom)

        self.add(*lines, *caps_top, *caps_bottom)

        wave_animations = []
        for i, line in enumerate(lines):
            # Simmetria nell'animazione: la parte superiore e inferiore si muovono allo stesso modo
            new_y = random.uniform(0.5, 1.5) * final_heights[i] * 0.5
            wave_animations.append(line.animate.put_start_and_end_on(
                [line_positions[i], -new_y, 0],
                [line_positions[i], new_y, 0]
            ).set_rate_func(there_and_back))
            wave_animations.append(caps_top[i].animate.move_to([line_positions[i], new_y, 0]).set_rate_func(there_and_back))
            wave_animations.append(caps_bottom[i].animate.move_to([line_positions[i], -new_y, 0]).set_rate_func(there_and_back))

        self.play(*wave_animations, run_time=0.8)

        # Fare in modo che la parte superiore e inferiore delle linee si muovano simmetricamente
        self.play(*[
            line.animate.put_start_and_end_on([x, 0, 0], [x, 0, 0])
            for x, line in zip(line_positions, lines)
        ] + [
            cap_top.animate.move_to([x, 0, 0]) for x, cap_top in zip(line_positions, caps_top)
        ] + [
            cap_bottom.animate.move_to([x, 0, 0]) for x, cap_bottom in zip(line_positions, caps_bottom)
        ], run_time=0.8)

        # Animazione simmetrica di espansione delle linee
        self.play(*[
            line.animate.put_start_and_end_on([x, -final_heights[i], 0], [x, final_heights[i], 0])
            for i, (x, line) in enumerate(zip(line_positions, lines))
        ] + [
            caps_top[i].animate.move_to([x, final_heights[i], 0])
            for i, x in enumerate(line_positions)
        ] + [
            caps_bottom[i].animate.move_to([x, -final_heights[i], 0])
            for i, x in enumerate(line_positions)
        ], run_time=1.2)

        self.play(Write(dell_erba), Write(shadow2), Write(shadow), Write(voice), run_time=1.6)
        self.wait(0.8)

        for _ in range(2):
            self.play(
                voice.animate.scale(1.1).shift(UP * 0.1), 
                shadow.animate.shift(UP * 0.1), 
                shadow2.animate.shift(UP * 0.1), 
                run_time=0.4
            )
            self.play(
                voice.animate.scale(0.9).shift(DOWN * 0.1), 
                shadow.animate.shift(DOWN * 0.1), 
                shadow2.animate.shift(DOWN * 0.1), 
                run_time=0.4
            )

        self.play(FadeOut(dell_erba), run_time=0.8)
        self.play(FadeOut(shadow2), FadeOut(shadow), FadeOut(voice), run_time=0.24)

        for scale in [0.5, 0.75, 0]:
            self.play(*[
                line.animate.put_start_and_end_on(
                    [x, -final_heights[i] * scale, 0],
                    [x, final_heights[i] * scale, 0]
                )
                for i, (x, line) in enumerate(zip(line_positions, lines))
            ] + [
                caps_top[i].animate.move_to([x, final_heights[i] * scale, 0])
                for i, x in enumerate(line_positions)
            ] + [
                caps_bottom[i].animate.move_to([x, -final_heights[i] * scale, 0])
                for i, x in enumerate(line_positions)
            ], run_time=0.24)

        self.play(*[FadeOut(m) for m in lines + caps_top + caps_bottom], run_time=0.28)
        self.wait(0.4)
        self.play(FadeOut(*self.mobjects), run_time=0.5)
