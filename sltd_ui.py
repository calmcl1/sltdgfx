import wx

import sltd_couple
import sltd_scoreboard

import random
random.seed()

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

        self.sizer = wx.GridBagSizer(vgap=10, hgap=10)

        self.couples_box = wx.ComboBox(
            self, -1, style=wx.CB_READONLY, value="Couples")
        self.couples_box.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(self.couples_box, (0, 1), (1, 7), wx.EXPAND)

        judge_score_font = wx.Font(48, wx.SWISS, wx.NORMAL, wx.BOLD)

        self.judge_1_label = wx.StaticText(self, -1, "Judge 1")
        self.sizer.Add(self.judge_1_label, (1, 1), (1, 1), wx.EXPAND)
        self.judge_1_score = wx.TextCtrl(self, -1, style=wx.TE_CENTRE)
        self.judge_1_score.SetFont(judge_score_font)
        self.sizer.Add(self.judge_1_score, (2, 1), (1, 1), wx.EXPAND)

        self.judge_2_label = wx.StaticText(self, -1, "Judge 2")
        self.sizer.Add(self.judge_2_label, (1, 3), (1, 1), wx.EXPAND)
        self.judge_2_score = wx.TextCtrl(self, -1, style=wx.TE_CENTRE)
        self.judge_2_score.SetFont(judge_score_font)
        self.sizer.Add(self.judge_2_score, (2, 3), (1, 1), wx.EXPAND)

        self.judge_3_label = wx.StaticText(self, -1, "Judge 3")
        self.sizer.Add(self.judge_3_label, (1, 5), (1, 1), wx.EXPAND)
        self.judge_3_score = wx.TextCtrl(self, -1, style=wx.TE_CENTRE)
        self.judge_3_score.SetFont(judge_score_font)
        self.sizer.Add(self.judge_3_score, (2, 5), (1, 1), wx.EXPAND)

        self.judge_4_label = wx.StaticText(self, -1, "Judge 4")
        self.sizer.Add(self.judge_4_label, (1, 7), (1, 1), wx.EXPAND)
        self.judge_4_score = wx.TextCtrl(self, -1, style=wx.TE_CENTRE)
        self.judge_4_score.SetFont(judge_score_font)
        self.sizer.Add(self.judge_4_score, (2, 7), (1, 1), wx.EXPAND)

        self.calculate_score_btn = wx.Button(self, -1, "Calculate Score")
        self.sizer.Add(self.calculate_score_btn, (4, 1), (1, 4), wx.EXPAND) 

        self.total_label = wx.StaticText(self, -1, "45", style=wx.TE_CENTRE)
        self.total_label.SetFont(wx.Font(26, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.total_label.SetBackgroundColour(wx.LIGHT_GREY)
        self.sizer.Add(self.total_label, (4, 6), (1, 2))

        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.sizer)
        self.Layout()


class MainWindow(wx.Frame):
    """
    Does a thing, makes a thing happen
    """

    def __init__(self):
        wx.Frame.__init__(self, None, title="SLTD Scoring",
                          size=(1000, 800))
        self.Bind(wx.EVT_CLOSE, self.on_close)

        print "Loading UI..."

        self.tab_window = wx.Notebook(self, -1, style=wx.NB_TOP)

        self.panel_system_setup = SystemSetupPanel(self.tab_window)
        self.panel_scoring_judges = CoupleScoringJudgesPanel(self.tab_window)

        self.tab_window.AddPage(self.panel_system_setup, "Scoring Setup", True)
        self.tab_window.AddPage(self.panel_scoring_judges,
                                "Couple Scoring: Judges", False)

        self.scoreboard = sltd_scoreboard.Scoreboard(self)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.tab_window, 3, wx.EXPAND)
        self.sizer.Add(self.scoreboard, 1, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)
        self.Layout()

        couple_mgr = sltd_couple.CoupleMgr()

        # Generate some fake couples for now
        for i in xrange(0, 10):
            c = sltd_couple.Couple()
            c.set_couple_name("Couple {0}".format(i))
            for j in xrange(0, 4):
                c.set_score(j, random.randint(1, 10))
            couple_mgr.add_couple(c, i)

        # Get list of couples in score order and add them to the leaderboard
        self.scoreboard.populate_scoreboard(couple_mgr.get_couples_order_score())
        
        self.Show()


    def on_close(self, event):
        """
        Do a thing to make a thing happen
        :param event: The event provided by wxWindows
        :return:
        """
        self.Destroy()