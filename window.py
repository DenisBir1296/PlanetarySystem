import wx
import math
import parameters
from planetary_system import planetary_system_arr
from editable_list_ctrl import EditableListCtrl
from parameters_sizer import ParametersSizer
from planets_window import PlanetsWindow


class Window(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=parameters.DEF_SIZE)

        pnl = wx.Panel(self)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.settings_table_plot = wx.BoxSizer(wx.HORIZONTAL)
        self.settings_and_table = wx.BoxSizer(wx.VERTICAL)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.settings_sizer = ParametersSizer(panel=pnl, parameters=parameters.parameters, vgap=20, hgap=20)

        self.planet_parameters = EditableListCtrl(parent=pnl,
                                                  titles=parameters.table_headers_name,
                                                  style=wx.LC_REPORT | wx.BORDER_SUNKEN)

        self.planet_win = PlanetsWindow(pnl)

        self.add_row_button = wx.Button(pnl, label=parameters.buttons_name['add row'])
        self.del_row_button = wx.Button(pnl, label=parameters.buttons_name['del row'])
        self.reset_button = wx.Button(pnl, label=parameters.buttons_name['reset'])
        self.calculate_button = wx.Button(pnl, label=parameters.buttons_name['calculate'])

        self.add_row_button.Bind(wx.EVT_BUTTON, self.add_row)
        self.del_row_button.Bind(wx.EVT_BUTTON, self.del_row)
        self.reset_button.Bind(wx.EVT_BUTTON, self.reset)
        self.calculate_button.Bind(wx.EVT_BUTTON, self.calculate)

        self.button_sizer.Add(self.add_row_button, flag=wx.LEFT, border=20)
        self.button_sizer.Add(self.del_row_button, flag=wx.LEFT, border=20)
        self.button_sizer.Add(self.reset_button, flag=wx.LEFT, border=20)
        self.button_sizer.AddStretchSpacer()
        self.button_sizer.Add(self.calculate_button)

        self.settings_and_table.Add(self.settings_sizer, proportion=0)
        self.settings_and_table.Add(self.planet_parameters, flag=wx.TOP | wx.EXPAND, proportion=1, border=40)
        self.settings_table_plot.Add(self.settings_and_table, flag=wx.EXPAND)
        self.settings_table_plot.Add(self.planet_win, flag=wx.EXPAND | wx.LEFT, proportion=1, border=40)
        self.main_sizer.Add(self.settings_table_plot, flag=wx.ALL | wx.EXPAND, border=30, proportion=1)
        self.main_sizer.Add(self.button_sizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=50)

        self.reset()

        pnl.SetSizer(self.main_sizer)
        self.SetMinSize(parameters.MIN_SIZE)
        self.Show(True)

    def add_row(self, event):

        count = self.planet_parameters.GetItemCount()
        if not count:
            m = parameters.SUN_MASS
            p = (0., 0.)
            v = (0., 0.)
        else:
            m = parameters.EARTH_MASS * pow(1.5, count - 1)
            p = (parameters.EARTH_X_POS * pow(2., count - 1), 0.)
            v = (0., parameters.EARTH_Y_VEL / pow(math.sqrt(2.), count - 1))

        self.planet_parameters.insert_row({'m': str(m),
                                           'x pos': str(p[0]),
                                           'y pos': str(p[1]),
                                           'x vel': str(v[0]),
                                           'y vel': str(v[1]),
                                           'res': '0.0'})

    def del_row(self, event):
        if not self.planet_parameters.IsEmpty():
            self.planet_parameters.DeleteItem(0)

    def reset(self, event=None):
        self.planet_parameters.DeleteAllItems()

        self.add_row(None)
        self.add_row(None)
        self.add_row(None)

        self.settings_sizer.set_values({k: parameters.parameters[k]['value'] for k in parameters.parameters})

    def calculate(self, event):
        prm = self.settings_sizer.get_values()
        pls = self.planet_parameters.get_rows()

        self.planet_win.timer.Stop()

        pl = planetary_system_arr(pls, prm)
        dialog = wx.GenericProgressDialog(title='Моделирование',
                                          message='Прогресс моделирования',
                                          maximum=pl.count,
                                          style=wx.PD_CAN_ABORT | wx.PD_AUTO_HIDE | wx.PD_APP_MODAL)
        result = pl.calculate(func=dialog.Update)

        self.planet_win.set_pl(result)
