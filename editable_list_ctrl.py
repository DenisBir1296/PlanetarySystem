import wx.lib.mixins.listctrl as listmix
import wx


class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin):
    ''' TextEditMixin allows any column to be edited. '''

    # ----------------------------------------------------------------------
    def __init__(self, parent, titles, width=80, ID=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        """Constructor"""

        self.keys = {}

        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.TextEditMixin.__init__(self)

        for i, k in enumerate(titles):
            self.keys[k] = i
            self.InsertColumn(i, titles[k], width=width)

    def insert_row(self, data):
        index = None

        for k in self.keys:
            if index is None:
                index = self.InsertItem(self.keys[k], str(data[k]))
            else:
                self.SetItem(index, self.keys[k], str(data[k]))

    def get_row(self, index):
        return {k: self.GetItemText(index, self.keys[k]) for k in self.keys}

    def get_rows(self):
        return [self.get_row(i) for i in range(self.GetItemCount())]
