#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 22:07:20 2024

@author: denis
"""

import wx
import matplotlib.pyplot
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import parameters
import numpy as np

planet_sc_size = 100
scale_factor = 0.15


class PlanetsWindow(wx.BoxSizer):
    def __init__(self, pnl):
        super().__init__(wx.VERTICAL)

        self.sliderSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.result = None
        self.pointer = None
        self.sc = None
        self.time_text = None

        self.time_slider = wx.Slider(pnl, value=0, minValue=0, maxValue=0, style=wx.SL_VALUE_LABEL)
        self.speed_slider = wx.Slider(pnl, value=50, minValue=10, maxValue=200, style=wx.SL_VALUE_LABEL | wx.SL_INVERSE)

        self.time_slider.Bind(wx.EVT_SCROLL, self.change_pointer)
        self.time_slider.Bind(wx.EVT_SCROLL_CHANGED, self.set_pointer)
        # self.speed_slider.Bind(wx.EVT_SCROLL, self.set_speed)

        self.timer = wx.Timer(pnl)
        pnl.Bind(wx.EVT_TIMER, self.next, self.timer)

        self.start_button = wx.BitmapButton(pnl, bitmap=wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_BUTTON))
        self.stop_button = wx.BitmapButton(pnl, bitmap=wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_BUTTON))

        self.start_button.Bind(wx.EVT_BUTTON, lambda event: self.timer.StartOnce(self.speed_slider.GetValue()))
        self.stop_button.Bind(wx.EVT_BUTTON, lambda event: self.timer.Stop())

        matplotlib.rcParams['font.size'] = parameters.FONT_SIZE

        # matplotlib.use('WXAgg')

        self.figure = matplotlib.figure.Figure()
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasWxAgg(pnl, wx.ID_ANY, self.figure)

        self.sliderSizer.Add(self.start_button)
        self.sliderSizer.Add(self.stop_button, flag=wx.LEFT, border=10)
        self.sliderSizer.Add(self.time_slider, flag=wx.LEFT, border=20, proportion=3)
        self.sliderSizer.Add(self.speed_slider, flag=wx.LEFT, border=20, proportion=1)

        self.Add(self.canvas, flag=wx.EXPAND, proportion=1)
        self.Add(self.sliderSizer, flag=wx.EXPAND | wx.ALL, border=20)

        self.axes.set_xlabel(parameters.X_NAME)
        self.axes.set_ylabel(parameters.Y_NAME)
        self.axes.set_aspect('equal')
        self.axes.grid(True)

        # self.SetMinSize(parameters.DIALOG_MIN_SIZE)

        self.canvas.draw()

        # self.timer.Start(40)

    def set_pl(self, result):
        self.timer.Stop()
        self.result = result
        self.time_slider.SetMax(result['count'] - 1)
        self.pointer = 0

        self.time_slider.SetValue(self.pointer)

        plot_size = 1.4 * max(abs(result['pos'][0, :, self.pointer] + 1j * result['pos'][1, :, self.pointer]))
        self.axes.set_xlim(-plot_size, plot_size)
        self.axes.set_ylim(-plot_size, plot_size)

        if self.sc is not None:
            self.sc.remove()

        if self.time_text is not None:
            self.time_text.remove()

        sc_size = planet_sc_size * pow(self.result['m'] / parameters.EARTH_MASS, scale_factor)
        # self.sc = self.axes.scatter([], [])

        self.time_text = self.axes.text(-plot_size/1.2, plot_size/1.2, f'time = {self.result["t"][self.pointer]}')
        self.sc = self.axes.scatter(self.result['pos'][0, :, self.pointer],
                                    self.result['pos'][1, :, self.pointer],
                                    s=sc_size, c=np.linspace(1., 0., len(self.result['m'])), alpha=0.7)

        self.canvas.draw_idle()
        self.canvas.Refresh()

    def change_pointer(self, event=None):
        self.pointer = self.time_slider.GetValue()

    def set_pointer(self, event=None):
        self.pointer = self.time_slider.GetValue()
        if not self.timer.IsRunning():
            self.update()

    def update(self, event=None):
        if self.pointer is None or self.sc is None or self.result is None:
            return

        self.time_text.set_text(f'time = {self.result["t"][self.pointer]}')
        self.sc.set(offsets=self.result['pos'][:, :, self.pointer].T)

        self.canvas.draw_idle()
        self.canvas.Refresh()

    def next(self, event=None):
        self.timer.StartOnce(self.speed_slider.GetValue())
        self.update()

        self.pointer += 1
        self.pointer %= self.result['count']

        self.time_slider.SetValue(self.pointer)
