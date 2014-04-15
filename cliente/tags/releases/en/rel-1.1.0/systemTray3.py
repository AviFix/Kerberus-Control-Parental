import wx


ID_SHOW_OPTION = wx.NewId()
ID_EDIT_OPTION = wx.NewId()


class Icon(wx.TaskBarIcon):

    def __init__(self, parent, icon, tooltip):
        wx.TaskBarIcon.__init__(self)
        self.SetIcon(icon, tooltip)
        self.parent = parent
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnLeftDClick)
        self.CreateMenu()

    def CreateMenu(self):
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.OnPopup)
        self.menu = wx.Menu()
        self.menu.Append(ID_SHOW_OPTION, '&Show Option 1')
        self.menu.Append(ID_EDIT_OPTION, '&Edit Option 2')
        self.menu.AppendSeparator()
        self.menu.Append(wx.ID_EXIT, 'E&xit')

    def OnPopup(self, event):
        self.PopupMenu(self.menu)

    def OnLeftDClick(self, event):
        if self.parent.IsIconized():
            self.parent.Iconize(False)
        if not self.parent.IsShown():
            self.parent.Show(True)
        self.parent.Raise()