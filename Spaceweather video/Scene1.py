from manim import *
import numpy as np
import creature as cpy
from scipy.optimize import fsolve

config.background_color = "#000d1a"

global color1
color1 = RED
global color2
color2 = BLUE

BROWN = '#422f09'

SVG_DIR = "C:/Users/Ronan/Desktop/Manim/media/stock_svg/"

def create_sun(radius):
    sun = Circle(radius = radius)
    sun.set_fill('#ebbd34', opacity=1.0)
    sun.set_stroke('#ebbd34', opacity = 1.0)
    return sun
    

def ring_of_parcels(n, radius, phi_offset = 0):
    phis = np.linspace(0, 2*np.pi, n, endpoint=False)
    
    offset_phis = phis + phi_offset
    offset_phis[offset_phis>2*np.pi] -= 2*np.pi
    
    xs = radius*np.cos(offset_phis)
    ys = radius*np.sin(offset_phis)
    zs = np.zeros(offset_phis.shape[0])
    points = np.stack((xs, ys, zs), axis=-1)
    dots_ = []
    for point, phi in zip(points, phis):
        if phi <= np.pi/2 or (phi <= 3*np.pi/2 and phi > np.pi):
            color = color1
        else:
            color = color2
        dots_.append(Dot(point = point, color = color))
        
    return dots_
    
rng = np.random.default_rng(459826470)
def random_parcels(number, sun, height, symbols = False):
    
    phis = rng.random(number)*2*np.pi
    
    #want it created inside sun
    radius = sun.height/2.1
    
    xs = radius*np.cos(phis)
    ys = radius*np.sin(phis)
    zs = np.zeros(phis.shape[0])
    points = np.stack((xs, ys, zs), axis=-1)
    dots = []
    for i, point in enumerate(points):
        point += sun.get_center()
        
        color = color1  
        if symbols == True:
            if i % 2 < 1:
                dots.append(Text("+", color=RED,font_size=24).move_to(point))
            else:
                dots.append(Text("-", color=WHITE,font_size=24).move_to(point))
            
        else:
            dots.append(Dot(point = point, color = color, radius = height))
        
    return dots
    
def replenish_parcels(angle, number, sun, height, symbols = False):
    
    phis = rng.random(number)*angle
    phis[int(number/2):] = 2*np.pi - phis[int(number/2):]
    
    #want it created inside sun
    radius = sun.height/2.1
    
    xs = radius*np.cos(phis)
    ys = radius*np.sin(phis)
    zs = np.zeros(phis.shape[0])
    points = np.stack((xs, ys, zs), axis=-1)
    dots = []
    for i, point in enumerate(points):
        point += sun.get_center()
        
        color = color1  
        if symbols == True:
            if i % 2 < 1:
                dots.append(Text("+", color=RED,font_size=24).move_to(point))
            else:
                dots.append(Text("-", color=WHITE,font_size=24).move_to(point))
            
        else:
            dots.append(Dot(point = point, color = color, radius = height))
        
    return dots

def random_stars(no, width=10, height=4):
    stars = []
    rand_x = rng.random(no)
    rand_y = rng.random(no)
    star_colour = "#edd51a"
    for i in np.arange(0, len(rand_x)):
        size = rng.integers(1,4)/50
        star = Star(outer_radius=size)
        star.set_fill(color = star_colour, opacity=1)
        star.set_stroke(color=star_colour, width=0)
        star.shift(rand_x[i]*width*RIGHT+rand_y[i]*height*UP)
        stars += star
        
    return stars

    
class Introduction(MovingCameraScene):
    def construct(self):
        def update_dot_random(mob, dt):
            radial_direction = mob.get_center() - sun.get_center()
            radial = radial_direction/np.linalg.norm(radial_direction)
            
            #if it hits earth loop in back
            dist_to_earth = mob.get_center() - earth.get_center()
            if np.linalg.norm(dist_to_earth) < earth.height/2:
                mob.shift(sun.get_center()+radial*0.1)
                #mob.set_fill(color = GREEN)
            #if it goes out of frame then loop in back
            #if self.camera.is_in_frame(mob) == False:
            if abs(np.linalg.norm(radial_direction)) > 12: 
                mob.move_to(sun.get_center()+radial*0.1)
                #mob.set_fill(color = BLUE)
            
            
            mob.shift(radial*dt*tracker.get_value()*6/800)
            
        def update_dot_random_earth(mob, dt):
            radial_direction = mob.get_center() - sun.get_center()
            radial = radial_direction/np.linalg.norm(radial_direction)
            
            #if it hits earth loop in back
            y_value = mob.get_center()[1]
            #if less than the max value of the bowshock
            if abs(y_value) < abs(bow_func(0)[1]):
                t_value = fsolve(func_to_solve, 0, args = (y_value))
                x_value = bow_func(t_value)[0]
                if (mob.get_center()[0] >= x_value) and (mob.get_center()[0] < earth.get_center()[0]):
                    #direction to next point in bow shock
                    if y_value > 0:
                        next_bow_point = bow_func(t_value - dt)
                    else:
                        next_bow_point = bow_func(t_value + dt)
                    next_bow_direction = next_bow_point - mob.get_center()
                    next_bow_norm = next_bow_direction/(np.linalg.norm(next_bow_direction))
                    mob.shift(next_bow_norm*dt*tracker.get_value()/800)
                else:
                    mob.shift(radial*dt*tracker.get_value()*6/800)
            else:
                mob.shift(radial*dt*tracker.get_value()*6/800)
            #if it goes out of frame then loop in back
            #if self.camera.is_in_frame(mob) == False:
            if abs(np.linalg.norm(radial_direction)) > 12:
                #need to put them back to the state before they were deflected
                #but need to add an extra random angle on
                extra_angle = ((rng.random() * 2) - 1)*np.pi/4 #between -1 and 1 
                radial_angle = np.arctan2(radial[1], radial[0])
                resulting_angle  = radial_angle + extra_angle
                vector_to_add = 0.1*np.array([np.cos(resulting_angle), np.sin(resulting_angle), 0])

                
                mob.move_to(sun.get_center()+vector_to_add)
            
        def twinkle_stars(mob,dt):
        
            height = mob.height
            random_add = rng.random()/200
            max_height = 0.15
            min_height = 0.01
            
            height_if_add  = height + random_add
            height_if_minus  = height - random_add
            
            if height_if_minus  < min_height:
                height = height_if_add
            elif height_if_add  > max_height:
                height = height_if_minus
            else:
                flip_coin = rng.random()
                if flip_coin > 0.5:
                    height = height_if_add
                else:
                    height = height_if_minus
                    
            mob.set(height = height)
            
            mob.set_fill(opacity = height/max_height)
            
        def points_from_angle(angle, earth, sign = 1):
            start = earth.get_center() + earth.height*np.array([-np.cos(angle)*sign,np.sin(angle),0])/2
            end = earth.get_center() + earth.height*np.array([-np.cos(angle)*sign,-np.sin(angle),0])/2
            return start, end
            
        self.camera.frame.save_state()
        
        width = 2
        square = Square(width, color=BROWN)
        triangle = Triangle(color=BROWN).scale(width/2).align_to(square, direction=UP)
        house = SVGMobject(SVG_DIR+"house1.svg").scale(2)#SVGMobject(SVG_DIR+"house.svg").scale(2)#VGroup(square,triangle).arrange(UP)
        house.set_fill(BROWN, opacity=1)
        grass = SVGMobject(SVG_DIR+"grass.svg").set_fill("#3b8a0e", opacity = 1).shift(2*DOWN+5*LEFT).scale(0.8)
        house = Group(house, grass)
        house.shift(DOWN)
        self.add(house)
        
        
        
        
        stars = Group(*random_stars(100))
        stars.shift(3*RIGHT)
        for star in stars:
            star.add_updater(twinkle_stars)
        self.add(stars)
        
            
        earth = cpy.EarthCreature("smile").scale(0.6)
        earth.shift(2*RIGHT + 2*DOWN)
        earth.look_at(stars)
        self.add(earth)
        
        telescope = SVGMobject(SVG_DIR+"telescope.svg")
        telescope.set_fill(WHITE)
        
        telescope.next_to(earth, RIGHT)
        self.add(telescope)
        
        
        self.camera.frame.shift(6.5*RIGHT)
        self.wait()#1
        self.play(cpy.Blink(earth), rate_func = rate_functions.there_and_back, run_time = 0.2)#1.2
        self.wait(2.5)#4.2
        self.play(cpy.Blink(earth), rate_func = rate_functions.there_and_back, run_time = 0.2)
        #4.4s
        
        sun = create_sun(1)
        sun.shift(3.5*LEFT+DOWN)
        self.add(sun)
        #5.4
        
        #[6.8]
        self.play(self.camera.frame.animate.shift(7*LEFT+0.5*DOWN).set_width(9), ApplyMethod(earth.look_at, sun))
        #6.4
        self.play(cpy.Blink(earth), rate_func = rate_functions.there_and_back, run_time = 0.2)
        self.wait(1.5)
        
        #fadeout house and stars
        self.remove(stars)
        self.play(FadeOut(house), FadeOut(telescope), Restore(self.camera.frame), sun.animate.move_to(5*LEFT).scale(1.5), 
        earth.animate.move_to(2.5*RIGHT).scale(0.6), run_time = 0.7)
        
        
        self.add_foreground_mobjects(sun, earth)


        tracker = ValueTracker(300)
        dot_height = 0.03
        
        final_dots = []
        
        original_dots = []
        
        print("")
        print("")
        print("")
        print("add dots")
        print("")
        print("")
        print("")
        
        #total number needs to be 25 +4
        turn_on_dots_idx = 10
        #make the original dots
        for i in np.arange(0,20): #used to be 25 but takes too long to say positive
            #print(i)
            dots = random_parcels(rng.integers(low=10, high = 20), sun, height = dot_height)
            original_dots += dots
            if i == 2 or i == 9 or i == 15:
                self.play(cpy.Blink(earth), rate_func = rate_functions.there_and_back, run_time = 0.2)
            #make them appear on the screen
            if i>= turn_on_dots_idx:
                for dot in original_dots:
                    dot.set_fill(opacity = 1)
            dot_creation = []
            for dot in dots:
                dot.add_updater(update_dot_random)
                #make them invisible to start with
                if i < turn_on_dots_idx:
                    dot.set_fill(opacity = 0)
            self.add(*dots)
            
            self.wait(rng.integers(low = 1, high = 6)*0.1)
        
        
        
        self.camera.frame.save_state()
        
        
        
        final_dots = original_dots.copy()
        
        #transform to plus and minus
        #which just adds a plus on top of old dots
        transformed_dots = []
        for dot in original_dots:
            
            if rng.random() > 0.5:
                new_dot = Text("+", color=RED,font_size=24).move_to(dot.get_center())
                
                
            else:
                new_dot = Text("-", color=WHITE,font_size=24).move_to(dot.get_center())
                
            new_dot.add_updater(update_dot_random)
            self.add(new_dot)
            transformed_dots.append(new_dot)
        
        #generates new symbols to come out the sun
        new_symbols = []
        for i in np.arange(0,6):
            #print("make new symbols", i)
            dots = random_parcels(rng.integers(low=10, high = 20), sun, height = dot_height, symbols = True)
            new_symbols += dots
            #make them appear on the screen
            dot_creation = []
            for dot in dots:
                dot.add_updater(update_dot_random)
            self.add(*dots)
            if i < 10:
                self.wait(rng.integers(low = 1, high = 6)*0.1)
            else:
                pass
        
        
        
        
        
        self.play(cpy.Blink(earth), rate_func = rate_functions.there_and_back, run_time = 0.2)
        
        print("")
        print("")
        print("")
        print("density")
        print("")
        print("")
        print("")
        #show density is low
        square = Square(side_length = 0.2).move_to(LEFT*3)
        
        big_square = Square(side_length = 1).move_to(DOWN*3)
        big_square.set_fill(config.background_color, opacity=1)
        
        line1 = always_redraw(lambda: Line(square.get_corner(LEFT+DOWN), big_square.get_corner(LEFT+DOWN)))
        line2 = always_redraw(lambda: Line(square.get_corner(LEFT+UP), big_square.get_corner(LEFT+UP)))
        line3 = always_redraw(lambda: Line(square.get_corner(RIGHT+DOWN), big_square.get_corner(RIGHT+DOWN)))
        line4 = always_redraw(lambda: Line(square.get_corner(RIGHT+UP), big_square.get_corner(RIGHT+UP)))
        self.add_foreground_mobjects(big_square)
        
        self.bring_to_front(big_square)
        
        br = Brace(big_square, RIGHT, sharpness=1)
        t = Text(f"1cm").next_to(br,RIGHT)
        runtime = 0.8
        self.play(DrawBorderThenFill(square, run_time=runtime), DrawBorderThenFill(big_square, run_time=runtime), DrawBorderThenFill(t, run_time=runtime),DrawBorderThenFill(br, run_time=runtime))
        self.play(FadeIn(line1,run_time = runtime), FadeIn(line2,run_time = runtime),FadeIn(line3,run_time = runtime),FadeIn(line4,run_time = runtime))
        square.add_updater(update_dot_random)
        
        offset_x = [0.3,-0.3,0.2,0,0.35]
        offset_y = [-0.3,0.2,0.35,-0.2,0]
        plusses = []
        minusses = []
        plusses_out = []
        minusses_out = []
        #now add in five protons and 5 electrons
        for i in np.arange(0,5):
            point = big_square.get_center() + np.array([offset_x[i], offset_y[i],0])
            plus = Text("+", color=RED,font_size=24).move_to(point)
            self.add_foreground_mobjects(plus)
            plusses.append(FadeIn(plus))
            plusses_out.append(FadeOut(plus))
            buffer = LEFT*0.1 + 0.1*DOWN
            minus = Text("-", color=WHITE,font_size=24).move_to(point + buffer)
            self.add_foreground_mobjects(minus)
            minusses.append(FadeIn(minus))
            minusses_out.append(FadeOut(minus))
            
        self.wait(1.2)
        
        runtime = 0.2
        self.play(*plusses_out, *minusses_out)
        self.remove(square, big_square,t,br,line1,line2,line3,line4)
        
        
        #then remove the symbols over the original dots
        for new_dot in transformed_dots:
            
            self.remove(new_dot)
        #turn the original symbols to dots
        for symbol in new_symbols:
            print("turn symbol to dot", i)
            dot = Dot(point = symbol.get_center(), color = color1, radius = dot_height)
            dot.add_updater(update_dot_random)
            self.add(dot)
            self.remove(symbol)
            final_dots += dot
        
        
        #This gets me to 19 seconds
        
        print("")
        print("")
        print("")
        print("speed")
        print("")
        print("")
        print("")
        #Change the speed with speedometer
        
        #
        self.wait(1)
        #
        
        def set_speedometer_angle(speed, radius):
            angle = (30 + (speed-400)/3)*np.pi/180
            x = -radius*np.cos(angle)
            y = radius*np.sin(angle)
            
            return np.array([x,y,0])
        
        
        #take out the arrow and just have the number vary like a counter
        
        

        speed_label = Integer(300).scale(1.5)
        speed_label.shift(2*LEFT)
        speed_label.add_updater(lambda m: m.set_value(tracker.get_value()))
        units = always_redraw(lambda: Text("km/s", font_size = 60).next_to(speed_label, RIGHT))
        
        self.play(FadeIn(speed_label), FadeIn(units), run_time = 0.5)
        self.wait(0.5)
        self.play(tracker.animate.set_value(800))
        self.wait(0.5)
        self.play(FadeOut(speed_label), FadeOut(units), run_time = 0.5)
        self.play(tracker.animate.set_value(400))
        
        #self.wait(1)
        #this whole bit lasts 5 seconds
        
        
        #news headline bit
        news = ImageMobject("./media/news.png")
        news.shift(DOWN*6 + LEFT)
        self.add_foreground_mobjects(news)
        self.play(news.animate.shift(6*UP))
        self.wait(3)
        
        
        #make a magnetosphere out of lines
        start, end = points_from_angle(45*DEGREES, earth)
        test_arc = CubicBezier(start, start + LEFT/4, end +LEFT/4,end)
        
        start1, end1 = points_from_angle(60*DEGREES, earth)
        test_arc1 = CubicBezier(start1, start1+0.5*LEFT+0.2*UP, end1+0.5*LEFT+0.2*DOWN, end1)
        
        start = earth.get_center()+UP
        end = earth.get_center()+DOWN
        bowshock = CubicBezier(start, start+LEFT+0.5*DOWN, end+LEFT+0.5*UP, end)
        
        start, end = points_from_angle(60*DEGREES, earth, -1)
        back_arc_points = [start, start + 0.5*RIGHT + 0.3*UP, earth.get_center()+3*RIGHT+0.2*UP]
        back_arc = VMobject()
        back_arc.set_points_smoothly(back_arc_points)
        
        back_arc_points = [end, end + 0.5*RIGHT + 0.3*DOWN, earth.get_center()+3*RIGHT+0.2*DOWN]
        back_arc1 = VMobject()
        back_arc1.set_points_smoothly(back_arc_points)
        
        start, end = points_from_angle(45*DEGREES, earth, -1)
        closed_back_arc_points = [start, start + 0.3*RIGHT + 0.1*UP, earth.get_center() + RIGHT, end + 0.3*RIGHT + 0.1*DOWN, end]
        closed_back_arc = VMobject()
        closed_back_arc.set_points_smoothly(closed_back_arc_points)
        #work out how to make the particles defect around this line
        bowshock_gen = bowshock.get_curve_functions()
        bow_func = next(bowshock_gen)
        
        y_var = 0.3
        #for this y value find the x value on the line
        #so I solve 
        self.play(news.animate.shift(6*DOWN), Create(test_arc), Create(test_arc1), Create(bowshock), Create(back_arc), Create(back_arc1), Create(closed_back_arc))
        
        self.add_foreground_mobjects(*final_dots)
        self.add_foreground_mobjects(sun, earth)
        
        
        def func_to_solve(t, y_value):
            return bow_func(t)[1] - y_value
        
        
        
        #change the updater
        for dot in final_dots:
            dot.clear_updaters()
            dot.add_updater(update_dot_random_earth)
        
        self.remove(news)
        
        
        #create more dots to hit earth
        for i in np.arange(0,3): # 15
            dots = replenish_parcels(20*np.pi/180,rng.integers(low=5, high = 10), sun, height = dot_height)
            final_dots += dots
            #make them appear on the screen
            dot_creation = []
            for dot in dots:
                dot.add_updater(update_dot_random_earth)
            self.add(*dots)
            self.wait(rng.integers(low = 1, high = 6)*0.1)

        self.play(self.camera.frame.animate.move_to(earth).set_width(earth.width*10))
        
        self.wait(3)
        #add in the aurora bit here
        #make two rings and have their opacity be random between 0.8 and 1
        
        self.aurora_brightness = 0.8
        def update_aurora(mob):
            
            random_add = rng.random()/20
            max_opacity = 1
            min_opacity = 0.6
            
            opacity_if_add  = self.aurora_brightness + random_add
            opacity_if_minus  = self.aurora_brightness - random_add
            
            if opacity_if_minus  < min_opacity:
                opacity = opacity_if_add
            elif opacity_if_add  > max_opacity:
                opacity = opacity_if_minus
            else:
                flip_coin = rng.random()
                if flip_coin > 0.5:
                    opacity = opacity_if_add
                else:
                    opacity = opacity_if_minus
                    
            self.aurora_brightness = opacity
                    
            mob.set_stroke(width = opacity*8, opacity = opacity)

            
            
            
        aurora_colour = "#41ff3b"
        northern = ArcBetweenPoints(start=points_from_angle(75*DEGREES, earth)[0], end=points_from_angle(55*DEGREES, earth, -1)[0], stroke_color=aurora_colour, stroke_width  = 3)
        southern = ArcBetweenPoints(end=points_from_angle(75*DEGREES, earth)[1], start=points_from_angle(55*DEGREES, earth, -1)[1], stroke_color=aurora_colour, stroke_width  = 3)
        northern.add_updater(update_aurora)
        southern.add_updater(update_aurora)
        self.add_foreground_mobjects(southern)
        self.add_foreground_mobjects(northern)
        
        
        
        self.wait(2)
        self.play(ApplyMethod(earth.change, 'smile'))
        self.wait(1.5)
        self.play(ApplyMethod(earth.change, 'frown'))
        self.play(cpy.Blink(earth), rate_func = rate_functions.there_and_back, run_time = 0.2)
        self.wait(1)
        
        
        sat = SVGMobject(SVG_DIR + "satellite.svg").scale(0.2)
        sat.move_to(earth.get_center()+2*LEFT+1*UP)
        sat.set_fill(WHITE, opacity=1)
        
        glove1 = SVGMobject(SVG_DIR + "glove.svg").scale(0.1)
        glove1.set_fill("#bd190d", opacity = 1)
        #2 is on the bottom
        glove2 = SVGMobject(SVG_DIR + "glove.svg").scale(0.1)
        glove2.flip()
        glove2.set_fill("#bd190d", opacity = 1)
        glove1.move_to(sat.get_center()+ 0.5*LEFT+0.5*UP)
        glove2.move_to(sat.get_center()+ 0.3*RIGHT+0.6*DOWN)
        
        glove1.rotate(-60*DEGREES)
        glove2.rotate(-30*DEGREES)

        self.play(FadeIn(sat), ApplyMethod(earth.look_at,sat))
        self.play(cpy.Blink(earth), rate_func = rate_functions.there_and_back, run_time = 0.2)
        self.add(glove2)
        self.add(glove1)
        self.play(ApplyMethod(glove1.shift, 0.25*DOWN+0.2*RIGHT, rate_func = rate_functions.rush_from, run_time=0.5), ApplyMethod(glove2.shift, 0.3*UP+0.15*LEFT, rate_func = rate_functions.rush_from, run_time=0.5))
        self.wait(0.5)
        
        #the power grid
        house = SVGMobject(SVG_DIR + "house1.svg").set_fill(BROWN).scale(0.3)
        flag = SVGMobject(SVG_DIR + "canada.svg").scale(0.05)
        
        pylon = SVGMobject(SVG_DIR + "pylon.svg").set_stroke("#878a88").scale(0.5)
        
        window_square = Rectangle(height = 0.1, width = 0.1).set_fill("#fcdd2d", opacity = 1).set_stroke(color = BLACK, width=1)
        window_square_back = Rectangle(height = 0.1, width = 0.1).set_fill(BLACK, opacity = 1).set_stroke(color = BLACK, width=1)
        window_bar_1 = Line(window_square.get_center()+ LEFT*window_square.width/2, window_square.get_center()+ RIGHT*window_square.width/2, color = BLACK, stroke_width = 1)
        window_bar_2 = Line(window_square.get_center()+ UP*window_square.width/2, window_square.get_center()+DOWN*window_square.width/2, color = BLACK, stroke_width = 1)
        window = VGroup(window_square_back, window_square, window_bar_1, window_bar_2)
        window.move_to(house.get_center())
        
        pylon.shift(LEFT*0.8+0.3*UP)
        flag.move_to(house.get_center()+0.3*UP+0.25*RIGHT)
        flag_pole = Line(flag.get_center()+LEFT*flag.width/2+0.16*DOWN, flag.get_center()+UP*flag.height/2+LEFT*flag.width/2, color = BROWN, stroke_width = 2)
        
        
        canada_one = VGroup(flag_pole, house, pylon, flag , window)
        canada_one.move_to(earth.get_center()+2*LEFT+1.1*DOWN)
        
        self.play(FadeIn(canada_one), ApplyMethod(earth.look_at,canada_one))
        
        
        #now flicker the light off
        self.play(window_square.animate.set_fill(opacity = 0.5), rate_func = rate_functions.wiggle, run_time = 0.6)
        self.play(window_square.animate.set_fill(opacity = 0.4), rate_func = rate_functions.wiggle, run_time = 0.3)
        self.play(window_square.animate.set_fill(opacity = 0), rate_func = rate_functions.ease_in_out_bounce,run_time = 0.1)
        self.wait()
        
        
        
        
        #Add in shapes to represent the pigeon
        
        pigeon = SVGMobject(SVG_DIR + "pigeon.svg").scale(0.5)
        pigeon.move_to(earth.get_center() + 1.3*DOWN+2*RIGHT)
        pigeon.set_fill(WHITE, opacity=1)
        question_mark = Text("?", color = RED, font_size = 20)
        question_mark.move_to(pigeon.get_center() + 0.5*RIGHT)
        question_mark1 = Text("?", color = RED, font_size = 20)
        question_mark1.move_to(pigeon.get_center() + UP*0.5+0.1*RIGHT)
        question_mark2 = Text("?", color = RED, font_size = 20)
        question_mark2.move_to(pigeon.get_center() + 0.5*LEFT)
        self.play(FadeIn(pigeon), ApplyMethod(earth.look_at,pigeon))
        self.play(ApplyMethod(question_mark.rotate, 10*DEGREES, rate_func = rate_functions.wiggle), ApplyMethod(question_mark1.rotate, -10*DEGREES, rate_func = rate_functions.wiggle), ApplyMethod(question_mark2.rotate, 10*DEGREES, rate_func = rate_functions.wiggle,))
        
        
        
        self.wait()
        self.play(ApplyMethod(earth.look_at, sun))
        self.wait()
        
        #now make the transition to the next scene
        #so zoom out 
        self.play(Restore(self.camera.frame))
        self.wait(5)
        
        #now zoom into the sun for the next scene
        #do it quite quick
        self.play(self.camera.frame.animate.move_to(sun), sun.animate.scale((2/3)),
        Uncreate(test_arc), Uncreate(test_arc1), Uncreate(bowshock), Uncreate(back_arc), Uncreate(back_arc1), Uncreate(closed_back_arc),
        FadeOut(northern), FadeOut(southern), FadeOut(pigeon), FadeOut(question_mark), FadeOut(question_mark1), FadeOut(question_mark2),
        FadeOut(canada_one), FadeOut(sat),FadeOut(glove1),FadeOut(glove2), FadeOut(earth),*[FadeOut(mob) for mob in final_dots])
        #self.remove(*final_dots)
        
        