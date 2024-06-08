import os.path

import wx
from ca import CoronaArchiver

def resource(filename) -> str:
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath('resources')

    return os.path.join(base, filename)


def archive(event):
    print('action')


class Program(wx.Frame):

    def __init__(self):
        super().__init__(None, size=(300, 200), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetIcon(wx.Icon(resource('default.ico')))
        self.SetTitle('Corona Archiver')
        panel = wx.Panel(self)
        button = wx.Button(panel, label="Action")
        button.SetPosition(((140-int(button.GetSize()[0]/2)), 140-int(button.GetSize()[1]/2)))
        self.types = wx.RadioBox(panel, choices=['Archive', 'Unarchive'])
        self.types.SetPosition((140-int(self.types.GetSize()[0]/2), 90-int(self.types.GetSize()[1]/2)))
        self.file = wx.TextCtrl(panel)
        self.file.SetSize((160, 20))
        self.file.SetHint('File')
        self.file.SetPosition((140-int(self.file.GetSize()[0]/2), 50-int(self.file.GetSize()[1]/2)))
        self.file2 = wx.TextCtrl(panel)
        self.file2.SetSize((160, 20))
        self.file2.SetHint('Folder')
        self.file2.SetPosition((140 - int(self.file2.GetSize()[0] / 2), 20 - int(self.file2.GetSize()[1] / 2)))
        self.select = wx.Button(panel, label='...')
        self.select.SetSize((30, 20))
        self.select.SetPosition((self.file2.GetPosition()[0]+160, self.file2.GetPosition()[1]))
        self.select2 = wx.Button(panel, label='...')
        self.select2.SetSize((30, 20))
        self.select2.SetPosition((self.file.GetPosition()[0] + 160, self.file.GetPosition()[1]))
        button.Bind(wx.EVT_BUTTON, self.act)
        self.__close_callback = None
        self.Bind(wx.EVT_CLOSE, self._when_closed)
        self.select.Bind(wx.EVT_BUTTON, self.select_1)
        self.select2.Bind(wx.EVT_BUTTON, self.select_2)
        self.Centre()

    def select_1(self, event):
        dlg = wx.DirDialog(None, "Choose output/input folder", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() != wx.CANCEL:
            self.file2.SetValue(dlg.GetPath())
        else:
            self.file2.SetValue('')

    def register_close_callback(self, callback):
        self.__close_callback = callback

    def select_2(self, event):
        with wx.FileDialog(self, "Save car file", wildcard="CAR files (*.car)|*.car", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() != wx.CANCEL:
                self.file.SetValue(fileDialog.GetPath())
            else:
                self.file.SetValue('')

    def act(self, event):
        arc = CoronaArchiver()
        if self.types.GetSelection() == 0:
            text = arc.pack(input_dir=os.path.join(self.file2.GetValue(), ''), output_file=self.file.GetValue())
            wx.MessageBox(text)
        else:
            text = arc.unpack(input_file=self.file.GetValue(), output_dir=os.path.join(self.file2.GetValue(), ''))
            wx.MessageBox(text)

    def _when_closed(self, event):
        doClose = True if not self.__close_callback else self.__close_callback()
        if doClose:
            event.Skip()


if __name__ == '__main__':
    app = wx.App()
    win = Program()
    win.Show()
    win.register_close_callback(lambda: True)
    app.MainLoop()
