import wx


GLOBAL_FRAME_SIZE = (700,500)


class SrcTextCtrl(wx.TextCtrl):
    def __init__(self,parent):
        wx.TextCtrl.__init__(self,parent, 2, size=(GLOBAL_FRAME_SIZE[0]*0.7,GLOBAL_FRAME_SIZE[1]*0.05))
        self.Bind(wx.EVT_SET_FOCUS,self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS,self.OnKillFocus)

    def OnSetFocus(self,evt):
        self.SetTransparent(500)
        print("focus")

    def OnKillFocus(self,evt):
        self.SetTransparent(200)

class Trans(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=GLOBAL_FRAME_SIZE,style=0)
        mGridBagSizer = wx.GridBagSizer(2, 2)

        self.srcText = SrcTextCtrl(self)
        mGridBagSizer.Add(self.srcText, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)

        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.Centre(wx.BOTH)
        self.SetSizer(mGridBagSizer)
        self.SetTransparent(200)  # 设置透明
        self.Show()


if __name__ == "__main__":
    app = wx.App()
    f = Trans(None, 1, "Transparent Window")
    app.TopWindow.Move(50,50)
    app.MainLoop()