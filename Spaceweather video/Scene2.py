from manim import *
import numpy as np
import creature as cpy
from scipy.optimize import fsolve

config.background_color = "#000d1a"

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
        
class Pfss(MovingCameraScene):
    def construct(self):
        sun = create_sun(1)
        self.add(sun)
        creation = []
        
        #rectangle
        north = Rectangle(color=RED, fill_opacity=1 ,height = sun.height/4, width = sun.height/4)
        south = Rectangle(color=BLUE, fill_opacity=1,height = sun.height/4, width = sun.height/4)
        
        magnet_shape = Group(north, south).arrange(DOWN, buff=0)
        N = Text("N", color = BLACK).scale(0.5)
        N.move_to(north.get_center())
        S = Text("S", color = BLACK).scale(0.5)
        S.move_to(south.get_center())
        magnet = Group(magnet_shape, N, S)
        self.play(FadeIn(magnet))
        
        
        tip_length = 0.1
        #have to do this manually so I know which line is which
        
        #for each line it should be made of two lines, that split in the center
        
        dipole_dic = {}
        
        for n in np.arange(0, 6):
            
            fline = np.load(f"./flines/dipole_{n}.npy")
            
            points = []
            points_mir = []
            for k in np.arange(0, fline.shape[0]):
                points.append(fline[k])
                points_mir.append(fline[k]*np.array([-1,1,0]))
                
            
                
            half_idx = int(fline.shape[0]/2)
            
            #need the full thing for the creation animation
            dipole = TipableVMobject()
            dipole.set_points_smoothly(points)
            tip = dipole.create_tip(tip_length = tip_length,at_start = False)
            dipole.add_tip(tip)
            dipole_mir = TipableVMobject()
            dipole_mir.set_points_smoothly(points_mir)
            tip = dipole_mir.create_tip(tip_length = tip_length,at_start = False)
            dipole_mir.add_tip(tip)
            
            if n <4:
                dipole_1 = TipableVMobject()
                dipole_1.set_points_smoothly(points[:half_idx+1])
                dipole_2 = TipableVMobject()
                dipole_2.set_points_smoothly(points[half_idx:])
                
                dipole_1_mir = TipableVMobject()
                dipole_1_mir.set_points_smoothly(points_mir[:half_idx+1])
                dipole_2_mir = TipableVMobject()
                dipole_2_mir.set_points_smoothly(points_mir[half_idx:])
                dipole_dic[f'dipole_{n}_1'] = dipole_1
                dipole_dic[f'dipole_{n}_2'] = dipole_2
                dipole_dic[f'dipole_{n}_1_mir'] = dipole_1_mir
                dipole_dic[f'dipole_{n}_2_mir'] = dipole_2_mir
            
            dipole_dic[f'dipole_{n}'] = dipole
            dipole_dic[f'dipole_{n}_mir'] = dipole_mir
            creation.append(Create(dipole))
            creation.append(Create(dipole_mir))
            
        #create the straight lines
        dipole_up = TipableVMobject()
        dipole_up.set_points_smoothly([sun.get_center()+UP*sun.height/2,sun.get_center()+UP*sun.height/2+UP])
        dipole_up.add_tip(tip_length = tip_length,at_start = False)
        
        dipole_down = TipableVMobject()
        dipole_down.set_points_smoothly([sun.get_center()+DOWN*sun.height/2+DOWN,sun.get_center()+DOWN*sun.height/2])
        dipole_down.add_tip(tip_length = tip_length,at_start = False)
        
        creation.append(Create(dipole_up))
        creation.append(Create(dipole_down))
        
        
        self.play(*creation)
        
        fline_dic = {}
        for p in np.arange(1, 14):
            if p <= 4 and p >0:
                print(f'fline_{p}')
                #this line points inwards so need to flip the start and end
                fline = np.load(f"./flines/fline_{p}.npy")
                points = []
                points_mir = []
                for k in np.arange(0, fline.shape[0]):
                    points.append(fline[k])
                    points_mir.append(fline[k]*np.array([-1,1,0]))
                fline_bottom = TipableVMobject()
                #this one is on the bottom so need to flip start and end
                fline_bottom.set_points_smoothly(points[::-1])
                fline_bottom_mir = TipableVMobject()
                fline_bottom_mir.set_points_smoothly(points_mir[::-1])
                fline_dic[f'fline_{p}'] = fline_bottom
                fline_dic[f'fline_{p}_mir'] = fline_bottom_mir
            elif p != 7:
                print(f'fline_{p}')
                #this should point outwards
                if p == 13:
                    #Load the bottom special one
                    fline = np.load(f"./flines/fline_special_0.npy")
                    points = []
                    points_mir = []
                    points_refl = []
                    points_refl_mir = []
                    for k in np.arange(0, fline.shape[0], 2):
                        points.append(fline[k])
                        points_mir.append(fline[k]*np.array([-1,1,0]))
                        
                        points_refl.append(fline[k]*np.array([1,-1,0]))
                        points_refl_mir.append(fline[k]*np.array([-1,-1,0]))
                        
                    points.append(fline[-1])
                    points_mir.append(fline[-1]*np.array([-1,1,0]))
                    
                    points_refl.append(fline[-1]*np.array([1,-1,0]))
                    points_refl_mir.append(fline[-1]*np.array([-1,-1,0]))
                    
                    fline_top = TipableVMobject()
                    fline_top.set_points_smoothly(points[::-1])
                    fline_top_mir = TipableVMobject()
                    fline_top_mir.set_points_smoothly(points_mir[::-1])
                    
                    fline_dic[f'fline_{p}'] = fline_top
                    fline_dic[f'fline_{p}_mir'] = fline_top_mir
                    
                    fline_top_refl = TipableVMobject()
                    fline_top_refl.set_points_smoothly(points_refl)
                    fline_top_refl_mir = TipableVMobject()
                    fline_top_refl_mir.set_points_smoothly(points_refl_mir)
                    
                    fline_dic[f'fline_{p+1}'] = fline_top_refl
                    fline_dic[f'fline_{p+1}_mir'] = fline_top_refl_mir
                    """
                    #take out this indent
                    elif p ==14:
                        #Load the top special one
                        fline = np.load(f"./flines/fline_special_1.npy")
                        points = []
                        points_mir = []
                        for k in np.arange(0, fline.shape[0]):
                            points.append(fline[k])
                            points_mir.append(fline[k]*np.array([-1,1,0]))
                        
                        fline_top = TipableVMobject()
                        fline_top.set_points_smoothly(points)
                        fline_top_mir = TipableVMobject()
                        fline_top_mir.set_points_smoothly(points_mir)
                        
                        fline_dic[f'fline_{p}'] = fline_top
                        fline_dic[f'fline_{p}_mir'] = fline_top_mir
                    """
                else:
                    #make a reflefction in x to get perfect symmetry
                    fline = np.load(f"./flines/fline_{p}.npy")
                    points = []
                    points_mir = []
                    
                    for k in np.arange(0, fline.shape[0]):
                        points.append(fline[k])
                        points_mir.append(fline[k]*np.array([-1,1,0]))
                    
                        
                        
                    fline_top = TipableVMobject()
                    fline_top.set_points_smoothly(points)
                    fline_top_mir = TipableVMobject()
                    fline_top_mir.set_points_smoothly(points_mir)
                    
                    
                    
                    fline_dic[f'fline_{p}'] = fline_top
                    fline_dic[f'fline_{p}_mir'] = fline_top_mir
                    
                    

                
        
        
        
        fline_up = TipableVMobject()
        fline_up.set_points_smoothly([sun.get_center()+UP*sun.height/2,sun.get_center()+UP*sun.height/2+2.3*UP])
        
        
        fline_down = TipableVMobject()
        fline_down.set_points_smoothly([sun.get_center()+DOWN*sun.height/2+2.1*DOWN, sun.get_center()+DOWN*sun.height/2])
        

        
        self.wait(2)
        
        for n in np.arange(0,4):
            self.remove(dipole_dic[f'dipole_{n}'], dipole_dic[f'dipole_{n}_mir'])
            self.add(dipole_dic[f'dipole_{n}_1'], dipole_dic[f'dipole_{n}_2'], dipole_dic[f'dipole_{n}_1_mir'], dipole_dic[f'dipole_{n}_2_mir'])
        #self.remove(dipole_dic[f'dipole_6_1'], dipole_dic[f'dipole_6_1_mir'])
        dipole_dic['dipole_4'].pop_tips()
        dipole_dic['dipole_5'].pop_tips()
        dipole_dic['dipole_4_mir'].pop_tips()
        dipole_dic['dipole_5_mir'].pop_tips()
        dipole_up.pop_tips()
        dipole_down.pop_tips()
        
        transforms = []
        
        for trans_no in np.arange(0, 4):
        
            #first loop top into 8
            transforms.append(CounterclockwiseTransform(dipole_dic[f'dipole_{trans_no}_1'], fline_dic[f'fline_{trans_no+8}']))
            #first loop bottom into 1
            transforms.append(ClockwiseTransform(dipole_dic[f'dipole_{trans_no}_2'], fline_dic[f'fline_{trans_no+1}']))
            #first loop top mirror into mirror 8
            transforms.append(ClockwiseTransform(dipole_dic[f'dipole_{trans_no}_1_mir'], fline_dic[f'fline_{trans_no+8}_mir']))
            transforms.append(CounterclockwiseTransform(dipole_dic[f'dipole_{trans_no}_2_mir'], fline_dic[f'fline_{trans_no+1}_mir']))
        
        
        
        transforms.append(FadeIn(fline_dic['fline_13']))
        transforms.append(FadeIn(fline_dic['fline_14']))
        transforms.append(FadeIn(fline_dic['fline_13_mir']))
        transforms.append(FadeIn(fline_dic['fline_14_mir']))
        
        
        #fline_dic['fline_14'].reverse_direction()
        #fline_dic['fline_14_mir'].reverse_direction()
        
        transforms.append(Transform(dipole_dic['dipole_4'], fline_dic[f'fline_5']))
        transforms.append(Transform(dipole_dic['dipole_5'], fline_dic[f'fline_6']))
        transforms.append(Transform(dipole_dic['dipole_4_mir'], fline_dic[f'fline_5_mir']))
        transforms.append(Transform(dipole_dic['dipole_5_mir'], fline_dic[f'fline_6_mir']))
        transforms.append(Transform(dipole_up, fline_up))
        transforms.append(Transform(dipole_down, fline_down))
        
        self.play(*transforms, FadeOut(magnet))
        
        #add tips on
        for trans_no in np.arange(0, 4):
            #dont know why but these two points need to have arrows flipped
            if trans_no < 2:
                at_start = False
                tip = dipole_dic[f'dipole_{trans_no}_1'].create_tip(tip_length = tip_length,at_start = False)
                dipole_dic[f'dipole_{trans_no}_1'].reset_endpoints_based_on_tip(tip, at_start)
                dipole_dic[f'dipole_{trans_no}_1'].asign_tip_attr(tip, at_start)
                tip.rotate(np.pi, about_point = dipole_dic[f'dipole_{trans_no}_1'].get_end())
                dipole_dic[f'dipole_{trans_no}_1'].add(tip)
                
                tip = dipole_dic[f'dipole_{trans_no}_1_mir'].create_tip(tip_length =tip_length,at_start = False)
                dipole_dic[f'dipole_{trans_no}_1_mir'].reset_endpoints_based_on_tip(tip, at_start)
                dipole_dic[f'dipole_{trans_no}_1_mir'].asign_tip_attr(tip, at_start)
                tip.rotate(np.pi, about_point = dipole_dic[f'dipole_{trans_no}_1_mir'].get_end())
                dipole_dic[f'dipole_{trans_no}_1_mir'].add(tip)
                
            else:
                dipole_dic[f'dipole_{trans_no}_1'].add_tip(tip_length = tip_length,at_start = False)
                dipole_dic[f'dipole_{trans_no}_1_mir'].add_tip(tip_length = tip_length,at_start = False)
                
            dipole_dic[f'dipole_{trans_no}_2'].add_tip(tip_length = tip_length,at_start = False)
            dipole_dic[f'dipole_{trans_no}_2_mir'].add_tip(tip_length = tip_length,at_start = False)
        
        
        fline_dic[f'fline_13'].add_tip(tip_length = tip_length,at_start = False)
        fline_dic[f'fline_13_mir'].add_tip(tip_length = tip_length,at_start = False)
        
        #tip wrong way round but cant tell if I dont add the tip
        #fline_dic[f'fline_14'].reverse_direction()
        #fline_dic[f'fline_14_mir'].reverse_direction()
        #fline_dic[f'fline_14'].add_tip(tip_length = tip_length,at_start = False)
        #fline_dic[f'fline_14_mir'].add_tip(tip_length = tip_length,at_start = False)
        
        dipole_dic[f'dipole_4'].add_tip(tip_length = tip_length,at_start = False)
        dipole_dic[f'dipole_5'].add_tip(tip_length = tip_length,at_start = False)
        dipole_dic[f'dipole_4_mir'].add_tip(tip_length = tip_length,at_start = False)
        dipole_dic[f'dipole_5_mir'].add_tip(tip_length = tip_length,at_start = False)
        dipole_up.add_tip(tip_length = tip_length,at_start = False)
        dipole_down.add_tip(tip_length = tip_length,at_start = False)
        
        self.wait(1)
        
        
        
        
        away = Text("Away", color = color1).move_to(5*RIGHT+2*UP)
        towards = Text("Towards", color = color2).move_to(5*RIGHT+2*DOWN)
        closed = Text("Closed", color = WHITE).move_to(5*LEFT)
        self.play(Write(towards, reverse=False), Write(away, reverse=False), Write(closed, reverse=False))
        
        
        
        #Turn positive RED
                
        
        colour_time = 0.5
        self.play(fline_dic[f'fline_13'].animate.set_stroke(RED), fline_dic[f'fline_13'].get_tip().animate.set_fill(RED),fline_dic[f'fline_13_mir'].animate.set_stroke(RED), fline_dic[f'fline_13_mir'].get_tip().animate.set_fill(RED),fline_dic[f'fline_14'].animate.set_stroke(BLUE),fline_dic[f'fline_14_mir'].animate.set_stroke(BLUE), run_time=colour_time)
        for n in np.arange(3, -1, -1):
            
            self.play(dipole_dic[f'dipole_{n}_1'].animate.set_stroke(RED), dipole_dic[f'dipole_{n}_1'].get_tip().animate.set_fill(RED),dipole_dic[f'dipole_{n}_1_mir'].animate.set_stroke(RED), dipole_dic[f'dipole_{n}_1_mir'].get_tip().animate.set_fill(RED), dipole_dic[f'dipole_{n}_2'].animate.set_stroke(BLUE), dipole_dic[f'dipole_{n}_2'].get_tip().animate.set_fill(BLUE),dipole_dic[f'dipole_{n}_2_mir'].animate.set_stroke(BLUE), dipole_dic[f'dipole_{n}_2_mir'].get_tip().animate.set_fill(BLUE), run_time=colour_time)
        
        up_tip = dipole_up.get_tip()
        down_tip = dipole_down.get_tip()
        self.play(dipole_up.animate.set_stroke(RED), up_tip.animate.set_fill(RED),dipole_down.animate.set_stroke(BLUE), down_tip.animate.set_fill(BLUE), run_time=colour_time)
        
        
        
        self.wait()
        
        
        
        #remove the tips
        radial_lines = []
        for n in np.arange(0,4):
            dipole_dic[f'dipole_{n}_1'].pop_tips()
            dipole_dic[f'dipole_{n}_1_mir'].pop_tips()
            dipole_dic[f'dipole_{n}_2_mir'].pop_tips()
            dipole_dic[f'dipole_{n}_2'].pop_tips()
        
            radial_to_ss = dipole_dic[f'dipole_{n}_1'].get_end() - sun.get_center()
            radial_line = Line(dipole_dic[f'dipole_{n}_1'].get_end(),215*radial_to_ss, color=RED)

            radial_lines += radial_line
            
            radial_to_ss = dipole_dic[f'dipole_{n}_1_mir'].get_end() - sun.get_center()
            radial_line = Line(dipole_dic[f'dipole_{n}_1_mir'].get_end(),215*radial_to_ss, color=RED)

            radial_lines += radial_line
            
            radial_to_ss = dipole_dic[f'dipole_{n}_2'].get_start() - sun.get_center()
            radial_line = Line(dipole_dic[f'dipole_{n}_2'].get_start(),215*radial_to_ss, color=BLUE)

            radial_lines += radial_line
            
            radial_to_ss = dipole_dic[f'dipole_{n}_2_mir'].get_start() - sun.get_center()
            radial_line = Line(dipole_dic[f'dipole_{n}_2_mir'].get_start(),215*radial_to_ss, color = BLUE)
            radial_lines += radial_line
        #dipole_dic[f'dipole_4'].pop_tips()
        #dipole_dic[f'dipole_4_mir'].pop_tips()
        #dipole_dic[f'dipole_5_mir'].pop_tips()
        #dipole_dic[f'dipole_5'].pop_tips()
        fline_dic[f'fline_13'].pop_tips()
        fline_dic[f'fline_13_mir'].pop_tips()
        dipole_up.pop_tips()
        dipole_down.pop_tips()
        radial_to_ss = dipole_up.get_end() - sun.get_center()
        radial_line = Line(dipole_up.get_end(),215*radial_to_ss, color = RED)
        radial_lines += radial_line
        
        radial_to_ss = dipole_down.get_start() - sun.get_center()
        radial_line = Line(dipole_down.get_start(),215*radial_to_ss, color = BLUE)
        radial_lines += radial_line
        
        radial_to_ss = fline_dic['fline_14'].get_start() - sun.get_center()
        radial_line = Line(fline_dic['fline_14'].get_start(),215*radial_to_ss, color = BLUE)
        radial_lines += radial_line
        radial_to_ss = fline_dic['fline_14_mir'].get_start() - sun.get_center()
        radial_line = Line(fline_dic['fline_14_mir'].get_start(),215*radial_to_ss, color = BLUE)
        radial_lines += radial_line
        
        radial_to_ss = fline_dic['fline_13'].get_end() - sun.get_center()
        radial_line = Line(fline_dic['fline_13'].get_end(),215*radial_to_ss, color = RED)
        radial_lines += radial_line
        radial_to_ss = fline_dic['fline_13_mir'].get_end() - sun.get_center()
        radial_line = Line(fline_dic['fline_13_mir'].get_end(),215*radial_to_ss, color = RED)
        radial_lines += radial_line
        
        add_radial = []
        for radial_line in radial_lines:
            add_radial.append(FadeIn(radial_line))
        
        
        
        
        
        
        
        
        
        
        #now add in solar wind parcels at the base
        pos_dots_create = []
        pos_dots_out = []
        pos_dots = []
        pos_move = []
        for n in np.arange(3, -1, -1):
            dot = Dot(point = dipole_dic[f'dipole_{n}_1'].get_start(), color = RED)
            pos_dots_create.append(FadeIn(dot))
            pos_dots_out.append(FadeOut(dot))
            pos_move.append(MoveAlongPath(dot, dipole_dic[f'dipole_{n}_1']))
            pos_dots += dot
            dot = Dot(point = dipole_dic[f'dipole_{n}_1_mir'].get_start(), color = RED)
            pos_dots_create.append(FadeIn(dot))
            pos_dots_out.append(FadeOut(dot))
            pos_move.append(MoveAlongPath(dot, dipole_dic[f'dipole_{n}_1_mir']))
            pos_dots += dot
            
        dot = Dot(point = dipole_up.get_start(), color = RED)
        pos_dots_create.append(FadeIn(dot))
        pos_dots_out.append(FadeOut(dot))
        pos_move.append(MoveAlongPath(dot, dipole_up))
        pos_dots += dot
        dot = Dot(point = fline_dic['fline_13'].get_start(), color = RED)
        pos_dots_create.append(FadeIn(dot))
        pos_dots_out.append(FadeOut(dot))
        pos_move.append(MoveAlongPath(dot, fline_dic['fline_13']))
        pos_dots += dot
        dot = Dot(point = fline_dic['fline_13_mir'].get_start(), color = RED)
        pos_move.append(MoveAlongPath(dot, fline_dic['fline_13_mir']))
        pos_dots_create.append(FadeIn(dot))
        pos_dots_out.append(FadeOut(dot))
        pos_dots += dot
        
        neg_dots_create = []
        neg_dots_out = []
        neg_dots = []
        neg_move = []
        for n in np.arange(3, -1, -1):
            dot = Dot(point = dipole_dic[f'dipole_{n}_2'].get_end(), color = BLUE)
            neg_dots_create.append(FadeIn(dot))
            neg_dots_out.append(FadeOut(dot))
            path_for_move = VMobject()
            path_for_move.set_points(dipole_dic[f'dipole_{n}_2'].get_points()[::-1])
            neg_move.append(MoveAlongPath(dot, path_for_move))
            neg_dots += dot
            
            dot = Dot(point = dipole_dic[f'dipole_{n}_2_mir'].get_end(), color = BLUE)
            neg_dots_create.append(FadeIn(dot))
            neg_dots_out.append(FadeOut(dot))
            path_for_move = VMobject()
            path_for_move.set_points(dipole_dic[f'dipole_{n}_2_mir'].get_points()[::-1])
            neg_move.append(MoveAlongPath(dot, path_for_move))
            neg_dots += dot
            
        dot = Dot(point = dipole_down.get_end(), color = BLUE)
        neg_dots_create.append(FadeIn(dot))
        neg_dots_out.append(FadeOut(dot))
        path_for_move = VMobject()
        path_for_move.set_points(dipole_down.get_points()[::-1])
        neg_move.append(MoveAlongPath(dot, path_for_move))
        neg_dots += dot
        
        dot = Dot(point = fline_dic['fline_14'].get_end(), color = BLUE)
        neg_dots_create.append(FadeIn(dot))
        neg_dots_out.append(FadeOut(dot))
        path_for_move = VMobject()
        path_for_move.set_points(fline_dic['fline_14'].get_points()[::-1])
        neg_move.append(MoveAlongPath(dot, path_for_move))
        neg_dots += dot
        
        dot = Dot(point = fline_dic['fline_14_mir'].get_end(), color = BLUE)
        neg_dots_create.append(FadeIn(dot))
        neg_dots_out.append(FadeOut(dot))
        path_for_move = VMobject()
        path_for_move.set_points(fline_dic['fline_14_mir'].get_points()[::-1])
        neg_move.append(MoveAlongPath(dot, path_for_move))
        neg_dots += dot
        
        #fade out the text and make the field lines extend all the way out
        self.play(Unwrite(towards, reverse=False), Unwrite(away, reverse=False), Unwrite(closed, reverse=False),*add_radial,
        *neg_dots_create, *pos_dots_create)
        self.wait(0.5)
        
        self.play(*pos_move, *neg_move)
        #self.wait(1)
        
        
        #Shift to see how far away earth is
        earth = cpy.EarthCreature(mode= 'smile').scale(0.3)
        earth.look_at(sun)
        
        earth_arrow = TipableVMobject()
        earth_arrow.set_points_smoothly([sun.get_center()+RIGHT*sun.height/2, sun.get_center()+215*RIGHT])
        earth_text = Text("Earth is 215 solar radii away", should_center = True).scale(20)
        earth_text.move_to(earth_arrow.get_center())
        self.add(earth_text)
        earth.shift(215*RIGHT)
        self.add_foreground_mobjects(earth)
        
        self.camera.frame.save_state()
        self.wait(0.5)
        self.play(Create(earth_arrow), self.camera.frame.animate.move_to(215*RIGHT))
        self.wait(0.2)
        self.play(cpy.Blink(earth), rate_func = rate_functions.there_and_back, run_time = 0.2)
        self.wait(0.2)
        self.play(self.camera.frame.animate.move_to(107*RIGHT).set(width = 215*1.5))
        self.wait(0.5)
        self.remove(earth_arrow)
        
        
        remove_radial = []
        for radial_line in radial_lines:
            remove_radial.append(FadeOut(radial_line))
        self.play(*remove_radial, self.camera.frame.animate.set(height = 5*sun.height).move_to(sun.get_center()+4*RIGHT+1.6*UP))
        #move the camera to the side

        
        
        
        #make dots on hemisphere
        #need to be 6 high in both hemispheres
        sun_mini = create_sun(1)
        sun_side = Group()
        spacing = np.floor(100*sun.height/(2*7))/100
        for i in np.arange(0,7):
            d = (spacing)*(i+1)
            chord_length = 2*np.sqrt((sun.height/2)**2 - d**2)
            no_horizontal = chord_length // spacing
            
            print(no_horizontal)
            for j in np.arange(-no_horizontal//2, 1+no_horizontal//2):
                if i == 0:
                    dot = Dot(point = sun.get_center() +(spacing)*(j)*RIGHT, color = RED)
                    sun_side.add(dot)
                dot = Dot(point = sun.get_center() +(spacing)*(j)*RIGHT + d*UP, color = RED)
                sun_side.add(dot)
                dot = Dot(point = sun.get_center() +(spacing)*(j)*RIGHT + d*DOWN, color = BLUE)
                sun_side.add(dot)
            
        
        
        
        
        side_earth = cpy.EarthCreature("smile").scale(0.3)
        side_earth.move_to(sun.get_center() + 5*RIGHT)
        side_earth.look_at(sun)
        sun_side.move_to(side_earth.get_center()+2*RIGHT)
        sun_mini.move_to(sun_side.get_center())
        
       
        top_earth = cpy.EarthCreature("smile").scale(0.3)
        top_earth.move_to(sun.get_center() + 5*UP)
        top_earth.look_at(sun)
        
        
        
        sun_mini1 = create_sun(1)
        
        sun_top = Group()
        spacing = np.floor(100*sun.height/(2*7))/100
        for i in np.arange(0,7):
            d = (spacing)*(i+1)
            chord_length = 2*np.sqrt((sun.height/2)**2 - d**2)
            no_horizontal = chord_length // spacing
            
            print(no_horizontal)
            for j in np.arange(-no_horizontal//2, 1+no_horizontal//2):
                if i == 0:
                    dot = Dot(point = sun.get_center() +(spacing)*(j)*RIGHT, color = RED)
                    sun_top.add(dot)
                
                dot = Dot(point = sun.get_center() +(spacing)*(j)*RIGHT + d*UP, color = RED)
                sun_top.add(dot)
                dot = Dot(point = sun.get_center() +(spacing)*(j)*RIGHT + d*DOWN, color = RED)
                sun_top.add(dot)
        
        sun_top.move_to(top_earth.get_center()+2*RIGHT)
        sun_mini1.move_to(sun_top.get_center())
        
        self.play(FadeIn(side_earth), FadeIn(sun_mini), FadeIn(sun_side), FadeIn(top_earth),
        FadeIn(sun_mini1), FadeIn(sun_top))
        self.play(cpy.Blink(side_earth), rate_func = rate_functions.there_and_back, run_time = 0.2)
        
        self.wait(1.8)
        self.play(cpy.Blink(side_earth), rate_func = rate_functions.there_and_back, run_time = 0.2)
        self.wait(0.8)
        self.play(cpy.Blink(side_earth), rate_func = rate_functions.there_and_back, run_time = 0.2)
        self.wait()
        
        corona= ImageMobject("./media/corona_image.png")
        corona.scale(1.2)
        corona.move_to(sun.get_center())
        self.bring_to_back(corona)
        
        remove_lines = []
        for n in np.arange(0,4):
            remove_lines.append(FadeOut(dipole_dic[f'dipole_{n}_1']))
            remove_lines.append(FadeOut(dipole_dic[f'dipole_{n}_1_mir']))
            remove_lines.append(FadeOut(dipole_dic[f'dipole_{n}_2']))
            remove_lines.append(FadeOut(dipole_dic[f'dipole_{n}_2_mir']))
        remove_lines.append(FadeOut(fline_dic[f'fline_13']))
        remove_lines.append(FadeOut(fline_dic[f'fline_14']))
        remove_lines.append(FadeOut(fline_dic[f'fline_13_mir']))
        remove_lines.append(FadeOut(fline_dic[f'fline_14_mir']))
        remove_lines.append(FadeOut(dipole_up))
        remove_lines.append(FadeOut(dipole_down))
        self.play(FadeIn(corona))
        
        self.wait()
        
        self.play(*remove_lines,
        *pos_dots_out, *neg_dots_out, FadeOut(sun_side), FadeOut(sun_top),FadeOut(dipole_dic[f'dipole_4']), FadeOut(dipole_dic[f'dipole_4_mir']), FadeOut(dipole_dic[f'dipole_5_mir']), FadeOut(dipole_dic[f'dipole_5']),FadeOut(sun))
        self.play(cpy.Blink(top_earth), rate_func = rate_functions.there_and_back, run_time = 0.2)
        
        
        #add top again
        sun_side_warped = Group()
        sun_side_warped_keep = Group()
        spacing = np.floor(100*sun.height/(2*7))/100
        for i in np.arange(0,7):
            d = (spacing)*(i+1)
            chord_length = 2*np.sqrt((sun.height/2)**2 - d**2)
            no_horizontal = chord_length // spacing
            
            
            
            
            for j in np.arange(-no_horizontal//2, 1+no_horizontal//2):
                
                if int(i) == 0 and int(j) < 0:
                    color_above = BLUE
                    color_below = BLUE
                elif int(i) == 1 and (int(j) < -1 and int(j) > -7):
                    color_above = BLUE
                    color_below = BLUE

                elif int(i) == 2 and (int(j) < -2 and int(j) > -6):
                    color_above = BLUE
                    color_below = BLUE

                elif int(i) == 0 and int(j) > 0:
                    color_above = RED
                    color_below = RED
                elif int(i) == 1 and (int(j) > 1 and int(j) < 7):
                    color_above = RED
                    color_below = RED
                elif int(i) == 2 and (int(j) > 2 and int(j) < 6):
                    color_above = RED
                    color_below = RED
                else:
                    color_above = RED
                    color_below = BLUE
                dot = Dot(point = sun.get_center() +(spacing)*(j)*RIGHT + d*UP, color = color_above)
                sun_side_warped.add(dot)
                dot = Dot(point = sun.get_center() +(spacing)*(j)*RIGHT + d*DOWN, color = color_below)
                sun_side_warped.add(dot)
                
                if i == 0:
                    if j < 0:
                        dot = Dot(point = sun.get_center() +(spacing)*(j)*RIGHT, color = BLUE)
                        #sun_side_warped.add(dot)
                        sun_side_warped_keep.add(dot)
                    else:
                        dot = Dot(point = sun.get_center() +(spacing)*(j)*RIGHT, color = RED)
                        #sun_side_warped.add(dot)
                        sun_side_warped_keep.add(dot)
                        
        sun_side_warped.move_to(sun_mini.get_center())
        sun_side_warped_keep.move_to(sun_mini.get_center())
        self.play(cpy.Blink(side_earth), rate_func = rate_functions.there_and_back, run_time = 0.2)
        self.play(cpy.Blink(top_earth), rate_func = rate_functions.there_and_back, run_time = 0.2)
        
        
        
        #the second top 
        sun_top1 = Group()
        spacing = np.floor(100*sun.height/(2*7))/100
        for i in np.arange(0,7):
            d = (spacing)*(i+1)
            chord_length = 2*np.sqrt((sun.height/2)**2 - d**2)
            no_horizontal = chord_length // spacing
            
            print(no_horizontal)
            for j in np.arange(1-no_horizontal//2, no_horizontal//2):
                if i == 0:
                    dot = Dot(point = sun.get_center() +(spacing)*(j)*RIGHT, color = RED)
                    sun_top1.add(dot)
                
                dot = Dot(point = sun.get_center() +(spacing)*(j)*RIGHT + d*UP, color = RED)
                sun_top1.add(dot)
                dot = Dot(point = sun.get_center() +(spacing)*(j)*RIGHT + d*DOWN, color = RED)
                sun_top1.add(dot)
        
        sun_top1.move_to(sun_mini1.get_center())
        #extra points
        dots = ring_of_parcels(36, radius = sun_mini1.height/2, phi_offset = 0)
        ring_dots = VGroup(*dots)
        ring_dots.move_to(sun_mini1.get_center())
        
        
        self.play(FadeIn(sun_top1), FadeIn(ring_dots),
        FadeIn(sun_side_warped), FadeIn(sun_side_warped_keep))
        self.wait(2)
        
        #leave just the rings around each mini sun
        self.play(FadeOut(sun_side_warped), FadeOut(sun_top1))
        self.wait(2)
        
        self.play(cpy.Blink(top_earth), rate_func = rate_functions.there_and_back, run_time = 0.2)
        self.play(self.camera.frame.animate.move_to(sun_mini1).set(height = 4*sun.height), FadeOut(top_earth),
        FadeOut(side_earth), FadeOut(corona), FadeOut(sun_mini), FadeOut(sun_side_warped_keep))
        
        
        self.wait()