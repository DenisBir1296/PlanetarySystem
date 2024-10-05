import wx
import wx.lib.mixins.listctrl  as  listmix
import math
import parameters
from planetary_system import planetary_system
from modal_window import AnimationWindow, TrajectoryWindow


class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin):
    ''' TextEditMixin allows any column to be edited. '''

    #----------------------------------------------------------------------
    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        """Constructor"""
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.TextEditMixin.__init__(self)
        


class Window(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, size = parameters.DEF_SIZE)
        
        pnl = wx.Panel(self)
        
        self.planet = -1
        
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.settings_and_table = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.settings_sizer = wx.GridSizer(2, 20, 20)

        self.planet_parameters = EditableListCtrl(pnl, style = wx.LC_REPORT | wx.BORDER_SUNKEN) 
        
        self.planet_parameters.InsertColumn(0, parameters.MASS_NAME,
                                            width=parameters.WIGHT)
        self.planet_parameters.InsertColumn(1, parameters.X_POS_NAME, 
                                            width=parameters.WIGHT)
        self.planet_parameters.InsertColumn(2, parameters.Y_POS_NAME, 
                                            width=parameters.WIGHT)
        self.planet_parameters.InsertColumn(3, parameters.X_VEL_NAME, 
                                            width=parameters.WIGHT)
        self.planet_parameters.InsertColumn(4, parameters.Y_VEL_NAME, 
                                            width=parameters.WIGHT)
        
        self.g = wx.TextCtrl(pnl, value=parameters.G_DEF_VAL)
        self.step = wx.TextCtrl(pnl, value=parameters.STEP_DEF_VAL)
        self.next_step = wx.TextCtrl(pnl, value=parameters.STEP_NEXT_VAL)
        self.time = wx.TextCtrl(pnl, value=parameters.TIME_DEF_VAL)

        self.balance_mass = wx.CheckBox(pnl)
        self.balance_impulse = wx.CheckBox(pnl)

        self.add_row_button = wx.Button(pnl, label=parameters.ADD_ROW_NAME)
        self.del_row_button = wx.Button(pnl, label=parameters.DEL_ROW_NAME)
        self.reset_button = wx.Button(pnl, label=parameters.RESET_NAME)
        self.animate_button = wx.Button(pnl, label=parameters.ANI_NAME)
        self.trajectory_button = wx.Button(pnl, label=parameters.TRAJ_NAME)

        self.add_row_button.Bind(wx.EVT_BUTTON, self.add_row)
        self.del_row_button.Bind(wx.EVT_BUTTON, self.del_row)
        self.reset_button.Bind(wx.EVT_BUTTON, self.reset)
        self.animate_button.Bind(wx.EVT_BUTTON, self.animate)
        self.trajectory_button.Bind(wx.EVT_BUTTON, self.show_trajectory)

        
        self.settings_sizer.Add(wx.StaticText(pnl, label=parameters.G_NAME))
        self.settings_sizer.Add(self.g)
        self.settings_sizer.Add(wx.StaticText(pnl, label=parameters.STEP_NAME))
        self.settings_sizer.Add(self.step)
        self.settings_sizer.Add(wx.StaticText(pnl, label=parameters.STEP_NEXT_NAME))
        self.settings_sizer.Add(self.next_step)
        self.settings_sizer.Add(wx.StaticText(pnl, label=parameters.TIME_NAME))
        self.settings_sizer.Add(self.time)
        self.settings_sizer.Add(wx.StaticText(pnl, label=parameters.BAL_MASS_NAME))
        self.settings_sizer.Add(self.balance_mass)
        self.settings_sizer.Add(wx.StaticText(pnl, label=parameters.BAL_IMPL_NAME))
        self.settings_sizer.Add(self.balance_impulse)
        
        self.button_sizer.Add(self.add_row_button, flag= wx.LEFT, border=20)
        self.button_sizer.Add(self.del_row_button, flag= wx.LEFT, border=20)
        self.button_sizer.Add(self.reset_button, flag= wx.LEFT, border=20)
        self.button_sizer.AddStretchSpacer()
        self.button_sizer.Add(self.animate_button)
        self.button_sizer.Add(self.trajectory_button, flag= wx.LEFT | wx.RIGHT, border=20)

        self.settings_and_table.Add(self.settings_sizer, flag=wx.EXPAND)
        self.settings_and_table.Add(self.planet_parameters, flag=wx.EXPAND, proportion=1)
        self.main_sizer.Add(self.settings_and_table, flag=wx.EXPAND | wx.ALL, border=30)
        self.main_sizer.AddStretchSpacer()
        self.main_sizer.Add(self.button_sizer, flag= wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=50)
        
        self.reset()
        
        pnl.SetSizer(self.main_sizer)
        self.SetMinSize(parameters.MIN_SIZE)
        self.Show(True)
        
    def add_row(self, event):
        
        if self.planet == -1:
            m = parameters.SUN_MASS
            p = (0., 0.)
            v = (0., 0.)
        else:
            m = parameters.EARTH_MASS*pow(1.5, self.planet)
            p = (parameters.EARTH_X_POS*pow(2., self.planet), 0.)
            v = (0., parameters.EARTH_Y_VEL/pow(math.sqrt(2.), self.planet))
            
        self.planet += 1;
            
        index = self.planet_parameters.InsertItem(0, str(m))
        self.planet_parameters.SetItem(index, 1, str(p[0]))
        self.planet_parameters.SetItem(index, 2, str(p[1]))
        self.planet_parameters.SetItem(index, 3, str(v[0]))
        self.planet_parameters.SetItem(index, 4, str(v[1]))

    def del_row(self, event):
        self.planet -= 1
        count  = self.planet_parameters.GetItemCount()
        if count:
            self.planet_parameters.DeleteItem(0)
    
    def reset(self, event=None):
        self.planet_parameters.DeleteAllItems()
        
        self.planet = -1
        
        self.add_row(None)
        self.add_row(None)
        self.add_row(None)
        
        self.g.SetValue(parameters.G_DEF_VAL)
        self.step.SetValue(parameters.STEP_DEF_VAL)
        self.next_step.SetValue(parameters.STEP_NEXT_VAL)
        self.time.SetValue(parameters.TIME_DEF_VAL)
        
    
    def get_values(self):
        g = float(self.g.GetLineText(0))
        step = float(self.step.GetLineText(0))
        next_step = float(self.next_step.GetLineText(0))
        time = float(self.time.GetLineText(0))
        
        bm = self.balance_mass.GetValue()
        bi = self.balance_impulse.GetValue()
        
        res = []
        flag = True
        
        count  = self.planet_parameters.GetItemCount()
        for i in range(count):
            try:
                i =     {'m': float(self.planet_parameters.GetItemText(i, 0)),
                         'px': float(self.planet_parameters.GetItemText(i, 1)),
                         'py': float(self.planet_parameters.GetItemText(i, 2)),
                         'vx': float(self.planet_parameters.GetItemText(i, 3)),
                         'vy': float(self.planet_parameters.GetItemText(i, 4))}
                res.append(i)
            except:
                flag = False
        
        return flag, g, step, next_step, time, {'bm': bm, 'bi': bi}, res
    
    
    def create_pl(self):
        try:
            flag, g, step, next_step, time, b, res = self.get_values()
        except:
            wx.MessageBox(parameters.PARAMETER_ERROR , style=wx.OK | wx.ICON_ERROR)
            raise
        
        if not flag:
            wx.MessageBox(parameters.PLANET_PARAMETER_WARNING, style=wx.OK | wx.ICON_WARNING)
            
        if next_step < step:
            wx.MessageBox(parameters.NEXT_STEP_WARNING, style=wx.OK | wx.ICON_WARNING)
            pl = planetary_system(dt=step, g=g)
        else:
            pl = planetary_system(dt=step, g=g, next_step=next_step)
        
        for i in res:
            if i['m'] <= 0:
                continue
            pl.add(m=i['m'], velocity=(i['vx'], i['vy']), position=(i['px'], i['py']))
        
        if b['bm']:
            pl.balancing_mass()
        
        if b['bi']:
            pl.balancing_impulse()
        
        return pl, time
        

    def animate(self, event):
        try:
            pl, time = self.create_pl()
        except:
            return
    
        aw = AnimationWindow(self, pl)
        aw.ShowModal()
        aw.Destroy()
        

    def show_trajectory(self, event):
        try:
            pl, time = self.create_pl()
        except:
            return
        
        tw = TrajectoryWindow(self, pl, time)
        tw.ShowModal()
        tw.Destroy()
       
