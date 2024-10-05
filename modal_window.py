#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 22:07:20 2024

@author: denis
"""

import wx
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import parameters
import numpy as np

planet_sc_size = 100
scale_factor = 0.12


class AnimationWindow(wx.Dialog):
    def __init__(self, parent, pl):
        super().__init__(parent, title=parameters.ANIMATION_WINDOW_NAME, 
                         style=wx.RESIZE_BORDER | wx.CLOSE_BOX | wx.CAPTION, 
                         size = parameters.DIALOG_DEFAULT_SIZE )
        
        self.pl = pl
        
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.main_sizer)
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        
        matplotlib.pyplot.rcParams.update({'font.size': parameters.FONT_SIZE})
        
        self.figure = matplotlib.figure.Figure()

        self.axes = self.figure.add_subplot()

        self.canvas = FigureCanvasWxAgg(self.panel, wx.ID_ANY, self.figure)
        
        self.panel.SetBackgroundColour(wx.Colour(wx.WHITE))
        self.main_sizer.Add(self.canvas, flag=wx.EXPAND, proportion=1)
        
        sc_size = planet_sc_size*pow(pl.mass/parameters.EARTH_MASS, scale_factor)
        
        plot_size = 1.4*max(abs(pl.x_position + 1j*pl.y_position))
        
        self.axes.set_xlim(-plot_size, plot_size)
        self.axes.set_ylim(-plot_size, plot_size)
        self.axes.set_xlabel(parameters.X_NAME)
        self.axes.set_ylabel(parameters.Y_NAME)
        self.axes.set_aspect('equal')
        self.axes.grid(True)
        
        self.sc = self.axes.scatter(pl.x_position, pl.y_position, 
                                    s=sc_size, c=np.linspace(1., 0., len(pl.mass)))
        
        self.SetMinSize(parameters.DIALOG_MIN_SIZE)
        
        self.canvas.draw()
        
        self.timer.Start(40)
        
    
    def update(self, event):
        self.sc.set_offsets(np.stack([self.pl.x_position, self.pl.y_position]).T)
        
        self.canvas.draw_idle()
        self.canvas.Refresh()
        
        self.pl.next()



class TrajectoryWindow(wx.Dialog):
    def __init__(self, parent, pl, time):
        super().__init__(parent, title=parameters.TRAJECTORY_WINDOW_NAME, 
                         style=wx.RESIZE_BORDER | wx.CLOSE_BOX | wx.CAPTION, 
                         size = parameters.DIALOG_DEFAULT_SIZE )
        
        self.pl = pl
        
        self.SetMinSize(parameters.DIALOG_MIN_SIZE)
        
        self.panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.main_sizer)
        
        matplotlib.pyplot.rcParams.update({'font.size': parameters.FONT_SIZE})
        
        self.figure = matplotlib.figure.Figure()

        self.xy_ax = self.figure.add_subplot(2, 2, (1, 3))
        self.r_ax = self.figure.add_subplot(2, 2, 2)
        self.alp_ax = self.figure.add_subplot(2, 2, 4)
        
        self.x_arr = [[] for i in range(pl.count_of_planet())]
        self.y_arr = [[] for i in range(pl.count_of_planet())]
        self.time_arr = []

        self.canvas = FigureCanvasWxAgg(self.panel, wx.ID_ANY, self.figure)
        
        self.panel.SetBackgroundColour(wx.Colour(wx.WHITE))
        self.main_sizer.Add(self.canvas, flag=wx.EXPAND, proportion=1)
        
        while pl.time < time:
            self.time_arr.append(pl.time)
            for i in range(pl.count_of_planet()):
                
                self.x_arr[i].append(pl.x_position[i])
                self.y_arr[i].append(pl.y_position[i])
                            
            pl.next()
        
        self.xy_ax.set_aspect('equal')
        self.xy_ax.set_xlabel(parameters.X_NAME)
        self.xy_ax.set_ylabel(parameters.X_NAME)
        self.xy_ax.set_title(parameters.TRAJ_TITLE_NAME)
        self.xy_ax.grid(True)
        
        self.r_ax.set_xlabel(parameters.TIME_NAME)
        self.r_ax.set_ylabel(parameters.RAD_NAME)
        
        self.alp_ax.set_xlabel(parameters.TIME_NAME)
        self.alp_ax.set_ylabel(parameters.ALP_NAME)
        
        for x, y in zip(self.x_arr, self.y_arr):
            x , y = np.array(x), np.array(y)
            sc = self.xy_ax.scatter(x, y, c=self.time_arr, s=1.5)
            pol = x + 1j*y
            self.r_ax.plot(self.time_arr, np.absolute(pol))
            self.alp_ax.plot(self.time_arr, np.angle(pol, deg=True))
            
        self.figure.colorbar(sc, label=parameters.TIME_NAME)
        
        self.canvas.draw()
        
            
        
    
    
    
    
        
    
    
        
        