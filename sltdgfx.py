import wx
#import wx.lib.agw.aui as aui
import pycasper
import sltd_ui
import sltd_couple


__author__ = 'Callum McLean'


if __name__ == "__main__":
    app = wx.App(False)
    window = sltd_ui.MainWindow()
    app.MainLoop()
