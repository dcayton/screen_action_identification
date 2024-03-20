#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 13:33:36 2024

@author: donaldcayton
"""
def horizontal_court_elements():
    """
    Takes no arguments.

    Returns
    -------
    Axes elements to create a horizontal court.

    """
    from matplotlib.patches import Circle, Rectangle, Arc
    
    lw = 1
    color = 'black'
    right_hoop = Circle((89.25, 25), radius=.85, linewidth=lw, color=color, fill=False)
    left_hoop = Circle((4.75, 25), radius=.85, linewidth=lw, color=color, fill=False)
    
    right_outer_box = Rectangle((75, 17), 19, 16, linewidth=lw, color=color,
                               fill=False)
    left_outer_box = Rectangle((0, 17), 19, 16, linewidth=lw, color=color,
                                fill=False)
    
    right_inner_box = Rectangle((75, 19), 19, 12, linewidth=lw, color=color,
                          fill=False)
    left_inner_box = Rectangle((0, 19), 19, 12, linewidth=lw, color=color,
                          fill=False)
    
    right_top_free_throw = Arc((75, 25), 12, 12, theta1=90, theta2=270,
                          linewidth=lw, color=color, fill=False)
    
    right_bottom_free_throw = Arc((75, 25), 12, 12, theta1=270, theta2=90,
                            linewidth=lw, color=color, linestyle='dashed')
    
    left_top_free_throw = Arc((19, 25), 12, 12, theta1=270, theta2=90,
                          linewidth=lw, color=color, fill=False)
    left_bottom_free_throw = Arc((19, 25), 12, 12, theta1=90, theta2=270,
                            linewidth=lw, color=color, linestyle='dashed')
    
    right_corner_three_a = Rectangle((80, 3), 14, 0, linewidth=lw,
                                color=color)
    right_corner_three_b = Rectangle((80, 47), 14, 0, linewidth=lw, color=color)
    
    left_corner_three_a = Rectangle((0, 3), 14, 0, linewidth=lw, color=color)
    left_corner_three_b = Rectangle((0, 47), 14, 0, linewidth=lw, color=color)
    
    right_three_arc = Arc((89.25, 25), 47.5, 47.5, theta1=112.5, theta2=247.5, linewidth=lw,
                    color=color)
    left_three_arc = Arc((4.75, 25), 47.5, 47.5, theta1=292.5, theta2=67.5, linewidth=lw,
                    color=color)
    
    half_court_line = Rectangle((47, 0), 0, 50, linewidth = lw, color = color)
    half_court_circle = Circle((47, 25), radius = 6, linewidth = lw, color = color, fill = False)
    
    
    court_elements = [left_hoop, right_hoop, left_outer_box, right_outer_box,
                      left_inner_box, right_inner_box, right_top_free_throw, left_top_free_throw,
                      right_bottom_free_throw, left_bottom_free_throw, right_corner_three_a,
                      right_corner_three_b, left_corner_three_a, left_corner_three_b,
                      right_three_arc, left_three_arc, half_court_line, half_court_circle]
    
    return court_elements
    

def vertical_halfcourt_elements():
    """
    Takes in no arguments

    Returns
    -------
    Axes elements to create a vertical halfcourt.

    """
    from matplotlib.patches import Circle, Rectangle, Arc
    
    lw = 1
    color = 'black'
    hoop = Circle((25, 89.25), radius=.85, linewidth=lw, color=color, fill=False)
    
    outer_box = Rectangle((17, 75), 16, 19, linewidth=lw, color=color,
                          fill=False)
    
    inner_box = Rectangle((19, 75), 12, 19, linewidth=lw, color=color,
                          fill=False)
    
    top_free_throw = Arc((25, 75), 12, 12, theta1=180, theta2=0,
                          linewidth=lw, color=color, fill=False)
    
    bottom_free_throw = Arc((25, 75), 12, 12, theta1=0, theta2=180,
                            linewidth=lw, color=color, linestyle='dashed')
    
    corner_three_a = Rectangle((3, 80), 0, 14, linewidth=lw,
                                color=color)
    corner_three_b = Rectangle((47, 80), 0, 14, linewidth=lw, color=color)
    three_arc = Arc((25, 89.25), 47.5, 47.5, theta1=202, theta2=337.5, linewidth=lw,
                    color=color)
    
    court_elements = [hoop, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, corner_three_a,
                      corner_three_b, three_arc]
    
    return court_elements
    