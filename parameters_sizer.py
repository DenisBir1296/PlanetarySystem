import wx


class ParametersSizer(wx.GridSizer):

    def __init__(self, panel, parameters, vgap, hgap):
        super().__init__(2, vgap, hgap)

        self.fields = {}
        for k in parameters:
            f = None
            self.Add(wx.StaticText(panel, label=parameters[k]['name']))
            if parameters[k]['type'] == 'textctrl':
                f = wx.TextCtrl(panel, value=parameters[k]['value'])
            if parameters[k]['type'] == 'checkbox':
                f = wx.CheckBox(panel)
                f.SetValue(parameters[k]['value'])

            if f is not None:
                self.Add(f)
                self.fields[k] = f

    def set_values(self, values):
        for k in values:
            self.fields[k].SetValue(values[k])

    def get_values(self):
        return {k: self.fields[k].GetValue() for k in self.fields}
