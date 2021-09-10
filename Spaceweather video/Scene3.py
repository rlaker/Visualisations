from manim import *
import numpy as np
import creature as cpy
from scipy.optimize import fsolve

config.background_color = "#000d1a"


PI_CREATURE_DIR = "C:/Users/Ronan/Desktop/Manim/media/mydrawings/"
SVG_DIR = "C:/Users/Ronan/Desktop/Manim/media/stock_svg/"

global color1
color1 = RED
global color2
color2 = BLUE

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
    


class SpinSolarWind(MovingCameraScene):
    def construct(self):
        def update_dot(mob, dt):
            if self.camera.is_in_frame(mob) == False:
                self.remove(mob)
            else:
                radial = mob.get_center()/np.linalg.norm(mob.get_center())
                mob.shift(radial*dt)
        def rotate_dot(mob,dt):
            mob.rotate(dt*10*DEGREES, about_point = ORIGIN)
        
        sun = create_sun(1)
        
        self.add(sun)
        
        
        #create a grid of points, coloured into 4 quadrants
        dot_arr = []
        no = 20
        
        no_with_arrows = 3
        
        
        for i in np.arange(0,no):
            dots = ring_of_parcels(36, radius = sun.height/2, phi_offset = 0)
            dot_arr.append(dots)
            
            for j in np.arange(0,len(dots)):
                dots[j].add_updater(rotate_dot)
        
        
        lines = []
        lines_fade = []
        for j in np.arange(0, len(dots),12):
            line = Line(ORIGIN, dots[j].get_center(), color=BLACK)
            lines.append(line)
            line.add_updater(rotate_dot)
        
        #have to add separately otherwise they all get grouped togetherc
        
        for dots in dot_arr:
            self.add(*dots)
        #self.add(*lines)
        
        #wait a second then add the updater 
        self.wait(1)#wait_between_parcels
        
        #make it so it starts with blobs that are easy to see, then speeds up to make the full pattern
        wait_parcels_array = np.concatenate((np.ones(no_with_arrows)*1, np.ones(no-no_with_arrows-1)*0.2, np.array([0])))
        
        arrow_arr = []
        
        #loop through and make the points leave the sun
        for i in np.arange(0,no):
            arrows = []
            for j, dot in enumerate(dot_arr[i]):
                dot.clear_updaters()
                dot.add_updater(update_dot)
                
                
                if i < no_with_arrows:
                    center = dot.get_center()
                    radial = center/np.linalg.norm(center)
                    
                    #arrow = Dot(center+radial*0.5, color=WHITE)#
                    arrow = Arrow(start = center, end = center + radial*0.8)
                    arrow.add_updater(update_dot)
                    
                    #print(np.arctan(radial[1]/radial[0])*180/np.pi, np.arctan(arrow.get_center()[1]/arrow.get_center()[0])*180/np.pi)
                    arrows.append(arrow)
                    self.add(arrow)
            #print(len(arrows))
            arrow_arr.append(arrows)               
                
            print(wait_parcels_array[i])
            #if the last one then dont wait
            if i == no -1:
                pass
            else:
                self.wait(wait_parcels_array[i])
        
        
        #freeze the dots in place
        remove_animation = []
        spirals  = []
        create_spirals = []
        remove_spiral_points = []
        for line in lines:
            line.clear_updaters()
        for i in np.arange(0,no):
            for dot in dot_arr[i]: # this is the ring of dots 
                dot.clear_updaters()
                if i < no_with_arrows:
                    #remove the dots with arrows
                    remove_animation.append(FadeOut(dot))
        
        for i in np.arange(0, len(arrow_arr)):
            for arrow in arrow_arr[i]:
                arrow.clear_updaters()
                remove_animation.append(FadeOut(arrow))

        print(len(dot_arr))
        print(len(dot_arr[0]))
        
        create_spirals = []
        remove_spiral_points = []
        for j in np.arange(0, 36):
            path = VMobject(color = dot_arr[0][j].get_color())       
            x_coords = []
            y_coords = []
            for i in np.arange(no_with_arrows, no):#no_with_arrows
                x_coords.append(dot_arr[i][j].get_center()[0])
                y_coords.append(dot_arr[i][j].get_center()[1])
                remove_spiral_points.append(FadeOut(dot_arr[i][j]))
            
            #to make the scaling work need to continue down within the sun
            tuples = list(zip(x_coords, y_coords))
            path.set_points_smoothly([*[np.array([x,y,0]) for x,y in tuples]])
            path.reverse_direction()
            spirals.append(path)
            create_spirals.append(Create(path))
            
        
        
        self.play(*remove_animation)
        
                
        #self.wait(2)
        
        
        
        
        #Have derivation of frozen in theorem whiz down
        title, lines = Frozen_In()
        self.play(Write(title), run_time=1)
        
        myparagraph = VGroup(*lines).arrange(direction=DOWN, aligned_edge=LEFT).scale(0.5)
        myparagraph.shift(8*DOWN)
        self.add(myparagraph)
        self.play(ApplyMethod(myparagraph.shift, 20*UP),ApplyMethod(title.shift, 20*UP), run_time=2)
        self.wait()
        self.remove(myparagraph)
        self.remove(title)
        
        #now create a spiral line for each set of dots
        
        self.play(*remove_spiral_points, *create_spirals)
        self.wait(0.5)
        #now make the spirals rotate then zoom out
        for spiral in spirals:
            spiral.add_updater(rotate_dot)
                
        
        
        self.wait(4)#maybe 4
        
        #cut all spirals, sun rotates too fast for it to work
        self.remove(*spirals)
        
        
        #now set up the orbits
        circle_radius = 3.5
        circle = Circle(radius=circle_radius, color=WHITE, stroke_width = 1)
        circle.move_to(sun)
        
        #set this to the alpha value you want to start at
        #for the circle this is just
        earth_start_angle = 20*np.pi/180
        earth_move_to = sun.get_center() + np.array([-np.cos(earth_start_angle), -np.sin(earth_start_angle), 0])*circle.height/2
        
        self.t_offset_earth = (earth_start_angle + np.pi)/(2*np.pi)
        self.t_offset_sta = (earth_start_angle - (90*np.pi/180) + np.pi)/(2*np.pi)
        
        
        
        
        def update_earth(mob,dt):
            rate=dt*0.1
            
            mob.move_to(circle.point_from_proportion(((self.t_offset_earth + rate))%1))
            self.t_offset_earth += rate
        
        
        
        
        earth_no_eyes = SVGMobject('./media/mydrawings/EarthCreature_no_eyes.svg').scale(0.15)
        earth_no_eyes.move_to(earth_move_to)
        
        ###
        # Now add the spacecraft scene here, because the transition needs to be smooth
        ###
        self.play(self.camera.frame.animate.shift(3.5*LEFT), sun.animate.scale(0.2),FadeIn(earth_no_eyes))
        earth_no_eyes.add_updater(update_earth)
        self.wait(2)
        
        
        
        
        
        
        psp_orbit = Ellipse(width=circle_radius - 0.4, height=circle_radius/2, color=WHITE, stroke_width=1)
        psp_orbit.move_to(sun.get_center())
        angle = 60
        psp_orbit.rotate(-angle*np.pi/180, about_point = sun.get_center())
        psp_orbit.shift(1.1*(np.cos(angle*np.pi/180)*LEFT + 1.1*np.sin(angle*np.pi/180)*UP))
        
        orbiter_orbit = Ellipse(width=5, height=4, color=WHITE, stroke_width=1)
        orbiter_orbit.move_to(sun.get_center())
        angle = 0
        orbiter_orbit.rotate(-angle*np.pi/180, about_point = sun.get_center())
        orbiter_orbit.shift(0.5*(np.cos(angle*np.pi/180)*LEFT + np.sin(angle*np.pi/180)*UP))
        
        bepi_orbit = Ellipse(width=6, height=6, color=WHITE, stroke_width=1)
        bepi_orbit.move_to(sun.get_center())
        angle = 45
        bepi_orbit.rotate(-angle*np.pi/180, about_point = sun.get_center())
        bepi_orbit.shift(0.5*(np.cos(angle*np.pi/180)*RIGHT + np.sin(angle*np.pi/180)*DOWN))
        
        #add orbits to look at them
        #self.add(circle, psp_orbit, orbiter_orbit, bepi_orbit)
        
        
        
        circle_func  = next(circle.get_curve_functions())
        print(circle.get_num_curves())
        print(circle_func(0))
        print(circle_func(1))
        
        
        
        
        psp = SVGMobject(PI_CREATURE_DIR + "psp.svg").scale(0.2)
        psp.set_fill(WHITE)
        psp.set_stroke(opacity = 0)
        
        orbiter = SVGMobject(PI_CREATURE_DIR + "solo.svg").scale(0.4)
        orbiter.set_fill(WHITE)
        orbiter.set_stroke(opacity = 0)
        
        bepi = SVGMobject(PI_CREATURE_DIR + "bepi.svg").scale(0.2)
        bepi.set_fill(WHITE)
        bepi.set_stroke(opacity = 0)
        
        sta = SVGMobject(PI_CREATURE_DIR + "sta.svg").scale(0.25)
        sta.set_fill(WHITE)
        sta.set_stroke(opacity = 0)

        wind = SVGMobject(PI_CREATURE_DIR + "wind.svg").scale(0.3)
        wind.set_fill(WHITE)
        wind.set_stroke(opacity = 0)
        
        def update_wind(mob):
        
            mob.move_to(earth_no_eyes.get_center() + (sun.get_center() - earth_no_eyes.get_center())/10)
        
        
        
        self.t_offset_sta = (0.5*np.pi + np.pi)/(2*np.pi)    
        def update_sta(mob,dt):
            rate=dt*0.1
            
            mob.move_to(circle.point_from_proportion(((self.t_offset_sta + rate))%1))
            self.t_offset_sta += rate
            
        
        self.t_offset_psp = (earth_start_angle + np.pi)/(2*np.pi)    
        
        def update_psp(mob,dt):
            #I also want to rotate PSP so it faces the sun
        
            dist_to_sun = np.linalg.norm(mob.get_center() - sun.get_center())
            psp_rate=dt*0.1*2/(dist_to_sun)
            
            mob.move_to(psp_orbit.point_from_proportion(((self.t_offset_psp + psp_rate))%1))
            
            psp_angle = self.psp_angle
            
            #what should the angle be?
            vec_to_sun = sun.get_center() - mob.get_center()
            angle = np.arctan2(vec_to_sun[0],vec_to_sun[1]) + np.pi
            
            rotate_by = angle - psp_angle
            
            print('')
            print('Should be', angle*180/np.pi)
            print('is', psp_angle*180/np.pi)
            print('Move by', rotate_by*180/np.pi)
            print('')
            
            mob.rotate(-rotate_by)
            self.psp_angle = psp_angle + rotate_by
            
            self.t_offset_psp += psp_rate
        
        
        self.t_offset_orbiter = (earth_start_angle + np.pi)/(2*np.pi)    
        def update_orbiter(mob,dt):
            dist_to_sun = np.linalg.norm(mob.get_center() - sun.get_center())
            orbiter_rate=dt*0.1*1.5/(dist_to_sun)
            
            mob.move_to(orbiter_orbit.point_from_proportion(((self.t_offset_orbiter + orbiter_rate))%1))
            self.t_offset_orbiter += orbiter_rate
            
        
        self.t_offset_bepi = (earth_start_angle + np.pi)/(2*np.pi)            
        def update_bepi(mob,dt):
            dist_to_sun = np.linalg.norm(mob.get_center() - sun.get_center())
            bepi_rate=dt*0.1*1.5/(dist_to_sun)
            
            mob.move_to(bepi_orbit.point_from_proportion(((self.t_offset_bepi + bepi_rate))%1))
            self.t_offset_bepi += bepi_rate
        
            
        #def interpolate_mobject(self, alpha: float) -> None:
        #    point = self.path.point_from_proportion(self.rate_func(alpha))
        #    self.mobject.move_to(point)
        
        
        
        
        heading_position = 9*LEFT+3*UP+sun.get_center()
        
        self.wait()
        
        
        #WIND
        wind.move_to(heading_position)
        wind_text = Text("Wind")
        wind_text.next_to(wind, RIGHT)
        
        self.play(FadeIn(wind), Write(wind_text))
        
        #
        font_size = 0.5
        wind_facts = VGroup(
            Text("Orbits ahead of Earth", size = font_size),
            Text("Provides 45 minute warning\nof space weather events", size = font_size),
            Text("Launched in 1994", size = font_size))
        wind_facts.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        wind_facts.shift(wind_text.get_center()+2*DOWN+RIGHT)
        
        self.play(Write(wind_facts[0]))
        self.play(Write(wind_facts[1]))
        self.wait(1.5)
        
        self.play(Write(wind_facts[2]))
        
        earth_reaction = cpy.EarthCreature("plain")
        earth_reaction.move_to(heading_position+5*DOWN+RIGHT)
        self.wait(2)
        self.play(FadeIn(earth_reaction))
        
        ##add in earth looking side to side with a straight face
        
        self.play(ApplyMethod(earth_reaction.look, LEFT+DOWN), run_time = 0.3)
        self.wait(0.1)
        self.play(ApplyMethod(earth_reaction.look, RIGHT+DOWN), run_time = 0.3)
        self.wait(0.1)
        self.play(ApplyMethod(earth_reaction.look, LEFT+DOWN), run_time = 0.3)
        
        scale_when_move = 0.6
        #extra 0.1 because I have to guess how long the move in animation takes (should be a second)
        earth_in_future = circle.point_from_proportion((self.t_offset_earth+ 0.1*0.9) % 1) 
        wind_move_to = earth_in_future + (sun.get_center() - earth_in_future)/10
        
        self.play(FadeOut(wind_text), wind.animate.move_to(wind_move_to).scale(scale_when_move), FadeOut(wind_facts), FadeOut(earth_reaction))
        wind.add_updater(update_wind)
        
        self.wait()
        
        #STA
        sta.move_to(heading_position)
        sta_text = Text("STEREO-A/B")
        sta_text.next_to(sta, RIGHT)
        
        sta_facts = VGroup(
            Text("Launched in 2006", size = font_size),
            Text("Twin spacecraft to take\nstereoscopic images", size = font_size),
            Text("STEREO-B was lost in 2014", size = font_size),
            )
        sta_facts.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        sta_facts.shift(sta_text.get_center()+2*DOWN)
        
        
        
        self.play(FadeIn(sta), Write(sta_text))
        self.play(Write(sta_facts[0]))
        self.play(Write(sta_facts[1]))
        self.play(Write(sta_facts[2]), Unwrite(sta_text[-2:]))
        
        
        sta_move_to = circle.point_from_proportion(self.t_offset_sta%1)
        
        self.play(FadeOut(sta_text), sta.animate.move_to(sta_move_to).scale(scale_when_move), FadeOut(sta_facts))
        sta.add_updater(update_sta)
        self.wait()
        
        #PSP
        psp.move_to(heading_position)
        psp_text = Text("Parker Solar Probe")
        psp_text.next_to(psp, RIGHT)
        
        psp_facts = VGroup(
            Text("Launched in 2018", size = font_size),
            Text("Fastest man-made object \n(692,000 km/h)", size = font_size),
            Text("Closest spacecraft \n(9 solar radii)", size = font_size))
        psp_facts.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        psp_facts.shift(psp_text.get_center()+2*DOWN+0.8*LEFT)
        
        
        
        self.play(FadeIn(psp), Write(psp_text))
        self.play(Write(psp_facts[0]))
        self.wait()
        self.play(Write(psp_facts[1]))
        self.play(Write(psp_facts[2]))
        self.wait(3)
        
        psp_move_to = psp_orbit.point_from_proportion(self.t_offset_psp)
        
        self.play(FadeOut(psp_text), psp.animate.move_to(psp_move_to).scale(scale_when_move), FadeOut(psp_facts))
        psp_start_rot_pos = sun.get_center() - psp_move_to
        psp_angle = np.arctan2(psp_start_rot_pos[0], psp_start_rot_pos[1])
        self.psp_angle = psp_angle + np.pi -(5*np.pi/180) # this doesnt quite work so add an extra buff
        print("start by rotating by", self.psp_angle*180/np.pi)
        psp.rotate(self.psp_angle)
        psp.add_updater(update_psp)
        
        
        self.wait(2)
        
        
        #Orbiter
        orbiter.move_to(heading_position)
        orbiter_text = Text("Solar Orbiter")
        orbiter_text.next_to(orbiter, RIGHT)
        
        orbiter_facts = VGroup(
            Text("Launched in 2020", size = font_size),
            Text("Has 10 different instruments", size = font_size),
            Text("Will take pictures of the Sun's poles", size = font_size))
        orbiter_facts.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        orbiter_facts.shift(orbiter_text.get_center()+2*DOWN)
        
        mini_solo = SVGMobject(PI_CREATURE_DIR+"solo.svg").scale(0.2)
        mini_solo.set_stroke(width=1)
        tin = SVGMobject(PI_CREATURE_DIR+"tin.svg").scale(1.3)
        tin.move_to(heading_position+5*DOWN+RIGHT)
        mini_solo.move_to(tin.get_center()+0.25*DOWN)
        
        import manimpango
        print(manimpango.list_fonts())
        
        tin_text1 = Text("Solar", font="Lucida Calligraphy", font_size = 16, color=BLACK)
        tin_text2 = Text("Orbiter", font="Lucida Calligraphy", font_size = 16, color=BLACK)
        tin_text = VGroup(tin_text1, tin_text2).arrange(DOWN)
        tin_lower_text1 = Text("Now with", font="Californian FB", font_size = 12, color=BLACK)
        tin_lower_text2 = Text("more instruments!", font="Californian FB", font_size = 12, color=BLACK)
        tin_lower_text = VGroup(tin_lower_text1, tin_lower_text2).arrange(DOWN, buff=0)
        tin_text.move_to(tin.get_center()+0.4*UP)
        tin_lower_text.move_to(tin.get_center()+0.6*DOWN)
        
        solo_tin = VGroup(tin, mini_solo, tin_text, tin_lower_text)
        
        self.play(FadeIn(orbiter), Write(orbiter_text))
        self.play(Write(orbiter_facts[0]))
        self.wait()
        self.play(Write(orbiter_facts[1]), FadeIn(solo_tin), Write(orbiter_facts[2]))
        self.wait(2)
        orbiter_move_to = orbiter_orbit.point_from_proportion(self.t_offset_orbiter)
        self.play(FadeOut(orbiter_text), orbiter.animate.move_to(orbiter_move_to).scale(scale_when_move), FadeOut(orbiter_facts), FadeOut(solo_tin))
        orbiter.add_updater(update_orbiter)
        
        
        
        #BEPI
        bepi.move_to(heading_position)
        bepi_text = Text("BepiColombo")
        bepi_text.next_to(bepi, RIGHT)
        
        bepi_facts = VGroup(
            Text("Will orbit Mercury in 2025", size = font_size),
            Text("Named after Guiseppe Colombo", size = font_size),
            Text("Takes 7 years to get there", size = font_size))
        bepi_facts.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        bepi_facts.shift(bepi_text.get_center()+2*DOWN)
        #bepi_facts.to_edge(LEFT, buff = LARGE_BUFF)
        
        self.play(FadeIn(bepi), Write(bepi_text))
        self.play(Write(bepi_facts[0]))
        self.play(Write(bepi_facts[1]))
        self.play(Write(bepi_facts[2]))
        self.wait()
        
        bepi_move_to = bepi_orbit.point_from_proportion(self.t_offset_bepi)
        
        self.play(FadeOut(bepi_text), bepi.animate.move_to(bepi_move_to).scale(scale_when_move), FadeOut(bepi_facts))
        bepi.add_updater(update_bepi)
        
        
        self.wait(2)
        
        #now draw lines between them all
        connecting_lines = []
        #I tried a loop but it doesn't work
        line = always_redraw(lambda: Line(start = wind.get_center(), end = psp.get_center(), stroke_width = 1))
                #line = Line(start = sc[i].get_center(), end = sc[j].get_center(), stroke_width = 1)
        connecting_lines.append(line)
        
        line = always_redraw(lambda: Line(start = wind.get_center(), end = sta.get_center(), stroke_width = 1))
                #line = Line(start = sc[i].get_center(), end = sc[j].get_center(), stroke_width = 1)
        connecting_lines.append(line)
        
        line = always_redraw(lambda: Line(start = wind.get_center(), end = orbiter.get_center(), stroke_width = 1))
                #line = Line(start = sc[i].get_center(), end = sc[j].get_center(), stroke_width = 1)
        connecting_lines.append(line)
        
        line = always_redraw(lambda: Line(start = wind.get_center(), end = bepi.get_center(), stroke_width = 1))
                #line = Line(start = sc[i].get_center(), end = sc[j].get_center(), stroke_width = 1)
        connecting_lines.append(line)
        
        line = always_redraw(lambda: Line(start = sta.get_center(), end = bepi.get_center(), stroke_width = 1))
                #line = Line(start = sc[i].get_center(), end = sc[j].get_center(), stroke_width = 1)
        connecting_lines.append(line)
        
        line = always_redraw(lambda: Line(start = sta.get_center(), end = orbiter.get_center(), stroke_width = 1))
                #line = Line(start = sc[i].get_center(), end = sc[j].get_center(), stroke_width = 1)
        connecting_lines.append(line)
        
        line = always_redraw(lambda: Line(start = sta.get_center(), end = psp.get_center(), stroke_width = 1))
                #line = Line(start = sc[i].get_center(), end = sc[j].get_center(), stroke_width = 1)
        connecting_lines.append(line)
        
        line = always_redraw(lambda: Line(start = bepi.get_center(), end = orbiter.get_center(), stroke_width = 1))
                #line = Line(start = sc[i].get_center(), end = sc[j].get_center(), stroke_width = 1)
        connecting_lines.append(line)
        
        line = always_redraw(lambda: Line(start = bepi.get_center(), end = psp.get_center(), stroke_width = 1))
                #line = Line(start = sc[i].get_center(), end = sc[j].get_center(), stroke_width = 1)
        connecting_lines.append(line)
        
        for line in connecting_lines:
            self.bring_to_back(line)
        
        print(connecting_lines)
        self.add(*connecting_lines)
        self.wait(5)
        
        
        plane = Axes(
            x_range = (0, 10),
            y_range = (0, 10),
            axis_config={"include_numbers": False},
            y_length = 2,
            x_length = 6,
        ).scale(0.5)
        
        
        plane1 = Axes(
            x_range = (0, 10),
            y_range = (0, 10),
            axis_config={"include_numbers": False},
            y_length = 2,
            x_length = 6,
        ).scale(0.5)
        
        plane2 = Axes(
            x_range = (0, 10),
            y_range = (0, 10),
            axis_config={"include_numbers": False},
            y_length = 2,
            x_length = 6,
        ).scale(0.5)
        
        
        #now do the timeseries
        planes = Group(plane, plane1, plane2).arrange(DOWN)
        planes.shift(8*LEFT+2*UP)
        
        B_arr = np.load("./media/B_arr.npy")
        V_arr = np.load("./media/V_arr.npy")
        N_arr = np.load("./media/N_arr.npy")
        
        
        line_graph = plane.get_line_graph(
            x_values = np.linspace(0,10, B_arr.shape[0]),
            y_values = B_arr,
            line_color=WHITE,
            stroke_width = 4,
        )
        
        line_graph1 = plane1.get_line_graph(
            x_values = np.linspace(0,10, V_arr.shape[0]),
            y_values = (V_arr- 300)/20,
            line_color=WHITE,
            stroke_width = 4,
        )
        
        line_graph2 = plane2.get_line_graph(
            x_values = np.linspace(0,10, N_arr.shape[0]),
            y_values = N_arr/4,
            line_color=WHITE,
            stroke_width = 4,
        )
        label_size = 12
        x_label = Text("Time", font_size = label_size).next_to(plane, RIGHT, buff= 0.2).shift(DOWN*0.5)
        y_label = Text("Magnetic Field", font_size = label_size).next_to(plane, LEFT, buff= 0).shift(RIGHT*0.4).rotate(90*DEGREES)
        grid_labels1 = VGroup(x_label, y_label)
        
        label_size = 12
        x_label = Text("Time", font_size = label_size).next_to(plane1, RIGHT, buff= 0.2).shift(DOWN*0.5)
        y_label = Text("Velocity", font_size = label_size).next_to(plane1, LEFT, buff= 0).shift(RIGHT*0.1).rotate(90*DEGREES)
        grid_labels2 = VGroup(x_label, y_label)
        
        label_size = 12
        x_label = Text("Time", font_size = label_size).next_to(plane2, RIGHT, buff= 0.2).shift(DOWN*0.5)
        y_label = Text("Density", font_size = label_size).next_to(plane2, LEFT, buff= 0).shift(RIGHT*0.1).rotate(90*DEGREES)
        grid_labels3 = VGroup(x_label, y_label)
        
        
        self.add(planes, grid_labels1, grid_labels2, grid_labels3)
        
        self.play(Create(line_graph["line_graph"]),
                    Create(line_graph1["line_graph"]),
                    Create(line_graph2["line_graph"]), run_time = 3, rate_func = rate_functions.linear)

        self.wait(0.5)
        
        #now add the papers
        paper1 = ImageMobject("./media/paper1.png")
        paper2 = ImageMobject("./media/paper2.png")
        
        paper1.shift(7*LEFT+2*DOWN)
        paper2.shift(7*LEFT+3*DOWN)
        
        self.play(FadeIn(paper1))
        self.play(FadeIn(paper2))
        
        self.wait(5)
        #add a big black rectangle to cover the whole screen
        blackout = Rectangle(width=40, height=40)
        blackout.set_fill(color = BLACK, opacity = 1)
        self.add(blackout)
        self.wait()
        


def Frozen_In():
    title = Text('Frozen-In Theorem')
    #it says paragraph is a VGroup of lines

    lines = []
    lines.append(Tex('In a perfectly conducting fluid, magnetic field lines move with the fluid.\nThe field lines are frozen in to the plasma'))
    lines.append(Tex(r"Using Gauss's divergence theorem and $\mathbf{\nabla} \cdot \mathbf{B} = 0$"))
    lines.append(Tex(r"$0 = \int_V \mathbf{\nabla} \cdot \mathbf{B} dV = \int_S \mathbf{B} \cdot dS $, for any closed surface, S"))
    lines.append(Tex(r'The magnetic flux, $\Phi$, through a closed curve C around an open surface $S_{1}$:'))
    
    lines.append(MathTex(r'\Phi = \int_{S_{1}} \mathbf{B}(\mathbf{r},t) \cdot dS'))
    lines.append(Tex(r"As curve C moves with time, $\delta t$, it becomes $C^{\prime}$."))
    
    lines.append(Tex("Wait, you've actually paused to check the maths?!"))
    
    
    lines.append(Tex(r"This creates a volume between the curves C and $C^{\prime}$ with the sides."))
    lines.append(Tex(r"So the flux through this closed surface at time $t+\delta t$:"))
    lines.append(MathTex(r"0 = \int_{top} \mathbf{B}(\mathbf{r},t+\delta t)\cdot dS + \int_{bottom} \mathbf{B}(\mathbf{r},t+\delta t)\cdot dS +\int_{side} \mathbf{B}(\mathbf{r},t+\delta t)\cdot dS "))
    lines.append(MathTex(r"0 = \int_{C^{\prime}} \mathbf{B}(\mathbf{r},t+\delta t)\cdot dS - \int_{C} \mathbf{B}(\mathbf{r},t+\delta t)\cdot dS +\int_{side} \mathbf{B}(\mathbf{r},t+\delta t)\cdot dS "))
    lines.append(Tex(r"Using $dS=dl\times \mathbf{\hat{n}}\delta t$:"))
    lines.append(MathTex(r"0 = \int_{C^{\prime}} \mathbf{B}(\mathbf{r},t+\delta t)\cdot dS - \int_{C} \mathbf{B}(\mathbf{r},t+\delta t)\cdot dS +\int_{side} \mathbf{B}(\mathbf{r},t+\delta t)\cdot \mathbf{dl}\times \mathbf{\hat{n}}\delta t"))
    lines.append(Tex(r"Therefore:"))
    lines.append(MathTex(r"\int_{C^{\prime}} \mathbf{B}(\mathbf{r},t+\delta t)\cdot dS = \int_{C} \mathbf{B}(\mathbf{r},t+\delta t)\cdot dS +\int_{side} \mathbf{B}(\mathbf{r},t+\delta t)\cdot \mathbf{dl}\times \mathbf{\hat{n}}\delta t"))
    lines.append(Tex("Nearly there I promise"))
    lines.append(Tex(r"The change in magnetic flux is:"))
    lines.append(MathTex(r"\delta \Phi = \int_{C^{\prime}} \mathbf{B}(\mathbf{r},t+\delta t)\cdot dS - \int_{C} \mathbf{B}(\mathbf{r},t)\cdot dS"))
    lines.append(MathTex(r"\delta \Phi = \int_{C}  \mathbf{B}(\mathbf{r},t+\delta t)\cdot dS - \int_{C} \mathbf{B}(\mathbf{r},t)\cdot  dS - \delta t \int_{C}\mathbf{B}(\mathbf{r},t+\delta t)\cdot \mathbf{dl} \times \mathbf{v}"))
    lines.append(MathTex(r"\delta \Phi = \delta t \int_{C} \frac{\partial \mathbf{B}}{\partial t} \cdot dS - \delta t \int_{C} \mathbf{v} \times \mathbf{B} \cdot \mathbf{dl}, \delta t \rightarrow 0"))
    
    lines.append(Tex(r"Subsituting the induction equation: "))
    lines.append(MathTex(r"\frac{\partial \mathbf{B}}{\partial t}  = \nabla \times (\mathbf{v}\times \mathbf{B})"))
    lines.append(Tex(r"We have:"))
    lines.append(MathTex(r"\frac{d\Phi}{dt} =  \int_{C} \nabla \times (\mathbf{v}\times \mathbf{B}) \cdot dS -  \int_{C} \mathbf{v} \times \mathbf{B} \cdot \mathbf{dl}"))
    lines.append(Tex(r"Finally, using Stoke's theorem"))
    lines.append(MathTex(r"\frac{d\Phi}{dt} = \int_{C} \mathbf{v} \times \mathbf{B} \cdot \mathbf{dl} -  \int_{C} \mathbf{v} \times \mathbf{B} \cdot \mathbf{dl}"))
    lines.append(Tex(r"Therefore, $\Phi$ does not change in time, so:"))
    lines.append(MathTex(r"\frac{d\Phi}{dt} = 0"))
    lines.append(Tex(r"We arrive at the conclusion that the magnetic fields lines are frozen into the plasma."))
    lines.append(MathTex(r"\frac{d\Phi}{dt} = \frac{d}{dt}\left [ \int_{C} \mathbf{B}\cdot dS \right ] = 0"))
    
    return title, lines
    
        
