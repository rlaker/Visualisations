from manim import *
import os
import warnings
PI_CREATURE_SCALE_FACTOR = 0.5

BODY_INDEX = 0
LEFT_EYE_INDEX = 1 + 3
RIGHT_EYE_INDEX = 2+ 3
LEFT_PUPIL_INDEX = 4+ 3
RIGHT_PUPIL_INDEX = 6+ 3
MOUTH_INDEX = 3+ 3

PI_CREATURE_DIR = "C:/Users/Ronan/Desktop/Manim/media/mydrawings/"
SVG_DIR = "C:/Users/Ronan/Desktop/Manim/media/stock_svg/"

        
BROWN = '#422f09'

def get_norm(vec):
    return np.linalg.norm(vec)

class SVGTest(Scene):
    def construct(self):
        self.wait()
        pigeon = SVGMobject(SVG_DIR + "pigeon.svg")
        pigeon.shift(4*RIGHT+2*DOWN)
        pigeon.set_fill(WHITE, opacity=1)
        question_mark = Text("?", color = RED)
        question_mark.move_to(pigeon.get_center() + RIGHT)
        question_mark1 = Text("?", color = RED)
        question_mark1.move_to(pigeon.get_center() + UP*1.1+0.2*RIGHT)
        question_mark2 = Text("?", color = RED)
        question_mark2.move_to(pigeon.get_center() + LEFT)
        self.play(FadeIn(pigeon))
        self.play(ApplyMethod(question_mark.rotate, 10*DEGREES, rate_func = rate_functions.wiggle), ApplyMethod(question_mark1.rotate, -10*DEGREES, rate_func = rate_functions.wiggle), ApplyMethod(question_mark2.rotate, 10*DEGREES, rate_func = rate_functions.wiggle,))
        
        
        
        
        self.wait(0.5)
        
        sat = SVGMobject(SVG_DIR + "satellite.svg").scale(0.5)
        sat.shift(4*LEFT+2*UP)
        sat.set_fill(WHITE, opacity=1)
        
        glove1 = SVGMobject(SVG_DIR + "glove.svg").scale(0.3)
        glove1.set_fill("#bd190d", opacity = 1)
        
        glove2 = SVGMobject(SVG_DIR + "glove.svg").scale(0.3)
        glove2.flip()
        glove2.set_fill("#bd190d", opacity = 1)
        glove1.move_to(sat.get_center()+ LEFT+UP)
        glove2.move_to(sat.get_center()+ 0.5*RIGHT+1.2*DOWN)
        
        glove1.rotate(-60*DEGREES)
        glove2.rotate(-30*DEGREES)
        
        
        
        
        self.play(FadeIn(sat))
        self.add(glove2)
        self.add(glove1)
        self.play(ApplyMethod(glove1.shift, 0.5*DOWN+0.2*RIGHT, rate_func = rate_functions.rush_from, run_time=0.5), ApplyMethod(glove2.shift, 0.5*UP+0.1*LEFT, rate_func = rate_functions.rush_from, run_time=0.5))
        self.wait(0.5)

        
        house = SVGMobject(SVG_DIR + "house1.svg").set_fill(BROWN).scale(0.6)
        flag = SVGMobject(SVG_DIR + "canada.svg").scale(0.1)
        flag_pole = Line(house.get_center()+0.3*UP+0.3*RIGHT, house.get_center()+0.7*UP+0.3*RIGHT, color = BROWN)
        pylon = SVGMobject(SVG_DIR + "pylon.svg").set_stroke("#878a88")
        
        window_square = Rectangle(height = 0.2, width = 0.2).set_fill("#fcdd2d", opacity = 1).set_stroke(color = BLACK, width=1)
        window_square_back = Rectangle(height = 0.2, width = 0.2).set_fill(BLACK, opacity = 1).set_stroke(color = BLACK, width=1)
        window_bar_1 = Line(window_square.get_center()+ LEFT*window_square.width/2, window_square.get_center()+ RIGHT*window_square.width/2, color = BLACK, stroke_width = 1)
        window_bar_2 = Line(window_square.get_center()+ UP*window_square.width/2, window_square.get_center()+DOWN*window_square.width/2, color = BLACK, stroke_width = 1)
        window = VGroup(window_square_back, window_square, window_bar_1, window_bar_2)
        window.move_to(house.get_center())
        
        pylon.shift(LEFT*1.2+0.5*UP)
        flag.move_to(house.get_center()+0.6*UP+0.5*RIGHT)
        
        canada_one = VGroup(flag_pole, house, pylon, flag , window)
        canada_one.shift(4*LEFT+2*DOWN)
        
        self.play(FadeIn(canada_one))
        self.wait(1)
        
        #now flicker the light off
        self.play(window_square.animate.set_fill(opacity = 0.5), rate_func = rate_functions.wiggle, run_time = 0.6)
        self.play(window_square.animate.set_fill(opacity = 0.4), rate_func = rate_functions.wiggle, run_time = 0.3)
        self.play(window_square.animate.set_fill(opacity = 0), rate_func = rate_functions.ease_in_out_bounce,run_time = 0.1)
        self.wait()


class EarthTest(Scene):
    def construct(self):
    
        earth = EarthCreature()
        #earth = SVGMobject("C:/Users/Ronan/OneDrive - Imperial College London/PhD/Conferences/FoNS Showcase/Manim/media/mydrawings/EarthCreature_plain.svg")
        print(earth.submobjects)
        earth.look_at(5*UP)
        self.add(earth)
        self.wait()
        self.play(ApplyMethod(earth.look_at, 2*LEFT))
        self.play(Blink(earth), rate_func = rate_functions.there_and_back, run_time = 0.2)
        self.play(ApplyMethod(earth.look_at, 2*RIGHT))
        self.play(ApplyMethod(earth.look_at, 2*DOWN))
        self.wait()
        
        print(earth.mouth.get_path_commands())
        
        self.play(ApplyMethod(earth.change, 'smile'))
        self.wait()
        self.play(ApplyMethod(earth.change, 'frown'))
        self.wait()
        
        
    
class EarthCreature(SVGMobject):
    

    def __init__(self, mode="plain", **kwargs):
        
        self.color = RED
        self.file_name_prefix = "EarthCreature"
        self.stroke_width = 0
        self.stroke_color = BLACK
        self.fill_opacity = 1.0
        #self.height = 3
        self.corner_scale_factor = 0.75
        self.flip_at_start = False
        self.is_looking_direction_purposeful = False
        self.start_corner = None
        # Range of proportions along body where arms are
        self.right_arm_range = [0.55, 0.7]
        self.left_arm_range = [.34, .462]
        self.pupil_to_eye_width_ratio = 0.4
        self.pupil_dot_to_pupil_width_ratio = 0.3
        #digest_config(self, kwargs)
        self.mode = mode
        self.parts_named = False
        
        svg_file = os.path.join(
            PI_CREATURE_DIR,
            "%s_%s.svg" % (self.file_name_prefix,mode)
        )
        print(svg_file)
        SVGMobject.__init__(self, file_name=svg_file, **kwargs)
        

        if self.flip_at_start:
            self.flip()
        print(self.start_corner)
        print(type(self.file_name_prefix))
        if self.start_corner is not None:
            self.to_corner(self.start_corner)

    def align_data(self, mobject):
        # This ensures that after a transform into a different mode,
        # the pi creatures mode will be updated appropriately
        SVGMobject.align_data(self, mobject)
        if isinstance(mobject, EarthCreature):
            self.mode = mobject.get_mode()
        
            
    def name_parts(self):
        self.mouth = self.submobjects[MOUTH_INDEX]
        self.body = self.submobjects[BODY_INDEX]
        left_pupil = VGroup(*[self.submobjects[LEFT_PUPIL_INDEX],
            self.submobjects[LEFT_PUPIL_INDEX+1],])
        right_pupil = VGroup(*[self.submobjects[RIGHT_PUPIL_INDEX],
            self.submobjects[RIGHT_PUPIL_INDEX+1],])
        self.pupils = VGroup(*[left_pupil, right_pupil
        ])
        self.eyes = VGroup(*[
            self.submobjects[LEFT_EYE_INDEX],
            self.submobjects[RIGHT_EYE_INDEX]
        ])
        self.eye_parts = VGroup(self.eyes, self.pupils)
        self.parts_named = True
        
        

    def init_colors(self):
        SVGMobject.init_colors(self)
        if not self.parts_named:
            self.name_parts()
        self.mouth.set_fill(opacity=0)
        self.body.set_fill(self.color, opacity=1)
        self.eyes.set_fill(WHITE, opacity=1)
        self.submobjects[LEFT_PUPIL_INDEX+1].set_fill(WHITE, opacity = 1)
        self.submobjects[LEFT_PUPIL_INDEX+1].set_stroke(opacity = 0)
        self.submobjects[LEFT_PUPIL_INDEX+1].set(height = 3)
        self.submobjects[RIGHT_PUPIL_INDEX+1].set_fill(WHITE, opacity = 1)
        self.submobjects[RIGHT_PUPIL_INDEX+1].set_stroke(opacity = 0)
        self.submobjects[RIGHT_PUPIL_INDEX+1].set(height = 3)
        self.init_pupils()
        return self

    def init_pupils(self):
        pass
    
    #think my pupils are fine
    """
    def init_pupils(self):
        # Instead of what is drawn, make new circles.
        # This is mostly because the paths associated
        # with the eyes in all the drawings got slightly
        # messed up.
        for eye, pupil in zip(self.eyes, self.pupils):
            pupil_r = eye.get_width() / 2
            pupil_r *= self.pupil_to_eye_width_ratio
            dot_r = pupil_r
            dot_r *= self.pupil_dot_to_pupil_width_ratio

            new_pupil = Circle(
                radius=pupil_r,
                color=BLACK,
                fill_opacity=1,
                stroke_width=0,
            )
            dot = Circle(
                radius=dot_r,
                color=WHITE,
                fill_opacity=1,
                stroke_width=0,
            )
            new_pupil.move_to(pupil)
            pupil.become(new_pupil)
            dot.shift(
                new_pupil.get_boundary_point(UL) -
                dot.get_boundary_point(UL)
            )
            pupil.add(dot)
    """
    def copy(self):
        copy_mobject = SVGMobject.copy(self)
        copy_mobject.name_parts()
        return copy_mobject

    def set_color(self, color):
        self.body.set_fill(color)
        self.color = color
        return self

    def change_mode(self, mode):
        new_self = self.__class__(
            mode=mode,
        )
        new_self.match_style(self)
        new_self.match_height(self)
        if self.is_flipped() != new_self.is_flipped():
            new_self.flip()
        
        new_self.shift(self.eyes.get_center() - new_self.eyes.get_center())
        """
        if hasattr(self, "purposeful_looking_direction"):
            new_self.look(self.purposeful_looking_direction)
        """
        self.become(new_self)
        self.mode = mode
        return self

    def get_mode(self):
        return self.mode

    def look(self, direction):
        norm = get_norm(direction)
        if norm == 0:
            return
        direction /= norm
        self.purposeful_looking_direction = direction
        #change this to deal with the pupil having a white dot
        for pupil, eye in zip(self.pupils.split(), self.eyes.split()):
            c = eye.get_center()
            right = eye.get_right() - c
            up = eye.get_top() - c
            vect = direction[0] * right + direction[1] * up
            v_norm = get_norm(vect)
            p_radius = 0.5 * pupil.get_width()
            vect *= (v_norm - 0.75 * p_radius) / v_norm
            pupil.move_to(c + vect)
        self.pupils[1].align_to(self.pupils[0], DOWN)
        return self

    def look_at(self, point_or_mobject):
        if isinstance(point_or_mobject, Mobject):
            point = point_or_mobject.get_center()
        else:
            point = point_or_mobject
        self.look(point - self.eyes.get_center())
        return self

    def change(self, new_mode, look_at_arg=None):
        self.change_mode(new_mode)
        if look_at_arg is not None:
            self.look_at(look_at_arg)
        return self

    def get_looking_direction(self):
        vect = self.pupils.get_center() - self.eyes.get_center()
        return normalize(vect)

    def get_look_at_spot(self):
        return self.eyes.get_center() + self.get_looking_direction()

    def is_flipped(self):
        return self.eyes.submobjects[0].get_center()[0] > \
            self.eyes.submobjects[1].get_center()[0]

    def blink(self):
        eye_parts = self.eye_parts
        eye_bottom_y = eye_parts.get_bottom()[1]
        middle_y = self.get_center()[1]
        eye_parts.apply_function(
            lambda p: [p[0], middle_y, p[2]]
        )
        return self

    def to_corner(self, vect=None, **kwargs):
        if vect is not None:
            SVGMobject.to_corner(self, vect, **kwargs)
        else:
            self.scale(self.corner_scale_factor)
            self.to_corner(DOWN + LEFT, **kwargs)
        return self

    def get_bubble(self, *content, **kwargs):
        bubble_class = kwargs.get("bubble_class", ThoughtBubble)
        bubble = bubble_class(**kwargs)
        if len(content) > 0:
            if isinstance(content[0], str):
                content_mob = TextMobject(*content)
            else:
                content_mob = content[0]
            bubble.add_content(content_mob)
            if "height" not in kwargs and "width" not in kwargs:
                bubble.resize_to_content()
        bubble.pin_to(self)
        self.bubble = bubble
        return bubble

    def make_eye_contact(self, pi_creature):
        self.look_at(pi_creature.eyes)
        pi_creature.look_at(self.eyes)
        return self

    def shrug(self):
        self.change_mode("shruggie")
        top_mouth_point, bottom_mouth_point = [
            self.mouth.points[np.argmax(self.mouth.points[:, 1])],
            self.mouth.points[np.argmin(self.mouth.points[:, 1])]
        ]
        self.look(top_mouth_point - bottom_mouth_point)
        return self

    def get_arm_copies(self):
        body = self.body
        return VGroup(*[
            body.copy().pointwise_become_partial(body, *alpha_range)
            for alpha_range in (self.right_arm_range, self.left_arm_range)
        ])


def get_all_pi_creature_modes():
    result = []
    prefix = "%s_" % PiCreature.CONFIG["file_name_prefix"]
    suffix = ".svg"
    for file in os.listdir(PI_CREATURE_DIR):
        if file.startswith(prefix) and file.endswith(suffix):
            result.append(
                file[len(prefix):-len(suffix)]
            )
    return result


class Alex(EarthCreature):
    pass  # Nothing more than an alternative name





class Eyes(VMobject):
    CONFIG = {
        "height": 0.3,
        "thing_to_look_at": None,
        "mode": "plain",
    }

    def __init__(self, body, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.body = body
        eyes = self.create_eyes()
        self.become(eyes, copy_submobjects=False)

    def create_eyes(self, mode=None, thing_to_look_at=None):
        if mode is None:
            mode = self.mode
        if thing_to_look_at is None:
            thing_to_look_at = self.thing_to_look_at
        self.thing_to_look_at = thing_to_look_at
        self.mode = mode
        looking_direction = None

        pi = PiCreature(mode=mode)
        eyes = VGroup(pi.eyes, pi.pupils)
        if self.submobjects:
            eyes.match_height(self)
            eyes.move_to(self, DOWN)
            looking_direction = self[1].get_center() - self[0].get_center()
        else:
            eyes.set_height(self.height)
            eyes.move_to(self.body.get_top(), DOWN)

        height = eyes.get_height()
        if thing_to_look_at is not None:
            pi.look_at(thing_to_look_at)
        elif looking_direction is not None:
            pi.look(looking_direction)
        eyes.set_height(height)

        return eyes

    def change_mode(self, mode, thing_to_look_at=None):
        new_eyes = self.create_eyes(
            mode=mode,
            thing_to_look_at=thing_to_look_at
        )
        self.become(new_eyes, copy_submobjects=False)
        return self

    def look_at(self, thing_to_look_at):
        self.change_mode(
            self.mode,
            thing_to_look_at=thing_to_look_at
        )
        return self

    def blink(self, **kwargs):  # TODO, change Blink
        bottom_y = self.get_bottom()[1]
        
        for submob in self:
            submob.apply_function(
                lambda p: [p[0], middle_y, p[2]]
            )
        return self
"""
class PiCreatureBubbleIntroduction(AnimationGroup):
    CONFIG = {
        "target_mode": "speaking",
        "bubble_class": SpeechBubble,
        "change_mode_kwargs": {},
        "bubble_creation_class": ShowCreation,
        "bubble_creation_kwargs": {},
        "bubble_kwargs": {},
        "content_introduction_class": Write,
        "content_introduction_kwargs": {},
        "look_at_arg": None,
    }

    def __init__(self, pi_creature, *content, **kwargs):
        digest_config(self, kwargs)
        bubble = pi_creature.get_bubble(
            *content,
            bubble_class=self.bubble_class,
            **self.bubble_kwargs
        )
        Group(bubble, bubble.content).shift_onto_screen()

        pi_creature.generate_target()
        pi_creature.target.change_mode(self.target_mode)
        if self.look_at_arg is not None:
            pi_creature.target.look_at(self.look_at_arg)

        change_mode = MoveToTarget(pi_creature, **self.change_mode_kwargs)
        bubble_creation = self.bubble_creation_class(
            bubble, **self.bubble_creation_kwargs
        )
        content_introduction = self.content_introduction_class(
            bubble.content, **self.content_introduction_kwargs
        )
        AnimationGroup.__init__(
            self, change_mode, bubble_creation, content_introduction,
            **kwargs
        )

class EarthCreatureSays(PiCreatureBubbleIntroduction):
    CONFIG = {
        "target_mode": "speaking",
        "bubble_class": SpeechBubble,
    }
"""
class Blink(ApplyMethod):

    def __init__(self, pi_creature, **kwargs):
        ApplyMethod.__init__(self, pi_creature.blink, **kwargs)