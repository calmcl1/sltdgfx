import wx
import wx.lib.agw.aui as aui
import pycasper


__author__ = 'Callum McLean'


class SystemSetupPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # We need lots of text fields, to enter text in!
        # These also need labels.
        # To keep thing simple, we'll group each text-field/label pair in a
        # mini-array, which will populate a large array of all of the text fields.
        # There's also a separate sizer for all of the text controls.

        num_text_fields = 20  # How many text fields do we want to provide?
        sizer_text_fields = wx.FlexGridSizer(num_text_fields, 2)
        self.textInputFields = []

        for i in xrange(0, num_text_fields):
            text_field = wx.TextCtrl(self)
            text_field_label = wx.StaticText(
                self, -1, "f{0} text".format(i))
            print "\tAdding text field: f{0}".format(i)
            controls = [text_field_label, text_field]
            self.textInputFields.append(controls)
            sizer_text_fields.AddMany(controls)

        print "\tAdding SUBMIT button"  # The important one
        self.button_submit = wx.Button(
            self, -1, "SUBMIT", style=wx.BU_EXACTFIT)

        self.sizer.Add(sizer_text_fields)
        self.sizer.Add(self.button_submit)
        self.SetSizerAndFit(self.sizer)


class CoupleScoringJudgesPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        num_templates = 5  # How many templates shall we have?
        self.template_buttons = []
        for i in xrange(0, num_templates):
            print "\tAdding recall button: #{0}".format(i)
            btn = wx.Button(self,
                            label="Recall Template {0}".format(i))
            self.template_buttons.append(btn)
            self.sizer.Add(btn)

        self.SetSizerAndFit(self.sizer)


class MainWindow(wx.Frame):
    """
    Does a thing, makes a thing happen
    """

    def __init__(self):
        wx.Frame.__init__(self, None, title="UberCarrot", size=(1000, 800))
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self._mgr = aui.AuiManager()
        self._mgr.SetAGWFlags(aui.AUI_MGR_LIVE_RESIZE |
                              aui.AUI_MGR_USE_NATIVE_MINIFRAMES)

        # notify AUI which frame to use
        self._mgr.SetManagedWindow(self)

        print "Loading UI..."
        # To avoid having the ugly dark-grey background on Windows, we'll use a wxPanel as the only
        # child object of the wxFrame. All the control will be children of the
        # wxPanel.

        self.tab_window = aui.wx.Notebook(self, -1)
        self.panel_system_setup = SystemSetupPanel(self.tab_window)
        self.panel_scoring_judges = CoupleScoringJudgesPanel(self.tab_window)

        self.tab_window.AddPage(self.panel_system_setup, "boxes", True)
        self.tab_window.AddPage(self.panel_scoring_judges, "data", False)

        self._mgr.AddPane(self.panel_system_setup, wx.CENTER, 'Template Data')
        self._mgr.AddPane(self.panel_scoring_judges,
                          wx.RIGHT, 'Template Recall')

        self._mgr.Update()
        # Boom.
        self.Show()

    def on_close(self, event):
        """
        Do a thing to make a thing happen
        :param event: The event provided by wxWindows
        :return:
        """
        self._mgr.UnInit()
        self.Destroy()


if __name__ == "__main__":
    app = wx.App(False)
    window = MainWindow()
    app.MainLoop()
