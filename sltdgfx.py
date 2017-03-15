import wx
#import wx.lib.agw.aui as aui
import pycasper

import random
random.seed()


__author__ = 'Callum McLean'


class SystemSetupPanel(wx.Panel):
    """"""

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
        self.text_input_fields = []

        for i in xrange(0, num_text_fields):
            text_field = wx.TextCtrl(self)
            text_field_label = wx.StaticText(
                self, -1, "f{0} text".format(i))
            controls = [text_field_label, text_field]
            self.text_input_fields.append(controls)
            sizer_text_fields.AddMany(controls)

        self.sizer.Add(sizer_text_fields)
        self.SetSizerAndFit(self.sizer)


class CoupleScoringJudgesPanel(wx.Panel):
    """"""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        num_templates = 5  # How many templates shall we have?
        self.template_buttons = []
        for i in xrange(0, num_templates):
            btn = wx.Button(self,
                            label="Recall Template {0}".format(i))
            self.template_buttons.append(btn)
            self.sizer.Add(btn)

        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.sizer)
        self.Layout()


class Couple(object):

    def __init__(self):

        self.couple_name = ""
        self.scores = [0, 0, 0, 0]
        self.total = sum(self.scores)

    def updateTotal(self):
        self.total = sum(self.scores)


class ScoreItem(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.sizer = wx.GridBagSizer(hgap=10)

        self.position_no = wx.StaticText(self, -1, "")
        self.position_no.SetFont(wx.Font(24,wx.SWISS, wx.NORMAL, wx.BOLD))
        self.position_no.SetMinSize((50,-1))
        self.sizer.Add(self.position_no, (0, 0), (2, 1), wx.EXPAND)
        self.couple_name = wx.StaticText(self, -1, "")
        self.couple_name.SetFont(wx.Font(18,wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(self.couple_name, (0, 1), (1, 4), wx.EXPAND)
        self.score = wx.StaticText(self, -1, "", style=wx.ALIGN_RIGHT)
        self.score.SetFont(wx.Font(24,wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(self.score, (0,5), (1,1), wx.EXPAND)

        scoreFont = wx.Font(14,wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.score_1 = wx.StaticText(self, -1, "")
        self.score_1.SetFont(scoreFont)
        self.sizer.Add(self.score_1, (1, 1), (1,1), wx.EXPAND)
        self.score_2 = wx.StaticText(self, -1, "")
        self.score_2.SetFont(scoreFont)
        self.sizer.Add(self.score_2, (1, 2), (1,1), wx.EXPAND)
        self.score_3 = wx.StaticText(self, -1, "")
        self.score_3.SetFont(scoreFont)
        self.sizer.Add(self.score_3, (1, 3), (1,1), wx.EXPAND)
        self.score_4 = wx.StaticText(self, -1, "")
        self.score_4.SetFont(scoreFont)
        self.sizer.Add(self.score_4, (1, 4), (1,1), wx.EXPAND)

        self.SetSizerAndFit(self.sizer)

    def set_couple_name(self, name):
        self.couple_name.SetLabel(name)

    def set_scores(self, scores):
        self.score_1.SetLabel("{0}".format(scores[0]))
        self.score_2.SetLabel("{0}".format(scores[1]))
        self.score_3.SetLabel("{0}".format(scores[2]))
        self.score_4.SetLabel("{0}".format(scores[3]))

    def set_total(self, total):
        self.score.SetLabel("{0}".format(total))

    def set_position(self, pos):
        self.position_no.SetLabel("{0}".format(pos))


class Scoreboard(wx.Panel):
    """The right-hand-side scoreboard layout"""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.scoreItems = []

        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)
        self.Layout()

    def populateLeaderboard(self, coupleData):
        i = 1
        for couple in coupleData:
            si = ScoreItem(self)
            si.set_couple_name(couple.couple_name)
            si.set_scores(couple.scores)
            si.set_total(couple.total)
            si.set_position(i)

            self.sizer.Add(si, 1, wx.EXPAND)

            i += 1


class MainWindow(wx.Frame):
    """
    Does a thing, makes a thing happen
    """

    def __init__(self):
        wx.Frame.__init__(self, None, title="SLTD Scoring",
                          size=(1000, 800))
        self.Bind(wx.EVT_CLOSE, self.on_close)

        print "Loading UI..."

        self.tab_window = wx.Notebook(self, -1)

        self.panel_system_setup = SystemSetupPanel(self.tab_window)
        self.panel_scoring_judges = CoupleScoringJudgesPanel(self.tab_window)

        self.tab_window.AddPage(self.panel_system_setup, "boxes", True)
        self.tab_window.AddPage(self.panel_scoring_judges, "data", False)

        self.sb = Scoreboard(self)

        couples = []
        for i in xrange(0, 10):
            c = Couple()
            c.couple_name = "Couple {0}".format(i)
            c.scores = [random.randint(0, 10), random.randint(
                0, 10), random.randint(0, 10), random.randint(0, 10)]
            c.updateTotal()
            couples.append(c)

        self.sb.populateLeaderboard(couples)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.tab_window, 3, wx.EXPAND)
        self.sizer.Add(self.sb, 1, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)
        self.Layout()

        # self._mgr.Update()
        # Boom.
        self.Show()

    def on_close(self, event):
        """
        Do a thing to make a thing happen
        :param event: The event provided by wxWindows
        :return:
        """
        # self._mgr.UnInit()
        self.Destroy()


if __name__ == "__main__":
    app = wx.App(False)
    window = MainWindow()
    app.MainLoop()
