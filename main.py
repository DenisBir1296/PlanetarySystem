import wx
import window
from parameters import PROGRAM_TITLE

app = wx.App()
wnd = window.Window(None, PROGRAM_TITLE)
app.MainLoop()