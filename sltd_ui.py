import wx

import sltd_couple
import sltd_scoreboard

import random
random.seed()

couple_mgr = sltd_couple.CoupleMgr()
judges = {}


class SystemSetupPanel(wx.Panel):
    """"""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # COUPLES SETUP

        self.couples_box = wx.StaticBox(self, -1, "Couples Setup")
        self.couples_sizer = wx.StaticBoxSizer(self.couples_box, wx.VERTICAL)
        self.couple_entries = []  # (StaticText, TextCtrl)

        for couple in couple_mgr.get_couples_order_id():
            couple_sizer = wx.BoxSizer(wx.HORIZONTAL)
            couple_label = wx.StaticText(
                self, -1, "{0}".format(couple[0] + 1), style=wx.TE_CENTRE)
            couple_label.SetMinSize((50, -1))
            couple_text = wx.TextCtrl(self, -1, couple[1].couple_name)
            couple_text.SetMinSize((500, -1))
            couple_sizer.Add(couple_label)
            couple_sizer.Add(couple_text, 3, wx.EXPAND)
            self.couples_sizer.Add(couple_sizer)
            self.couples_sizer.AddSpacer(5)

            self.couple_entries.append((couple_label, couple_text))

        self.couples_save_btn = wx.Button(self, -1, "Save Couples Data")
        self.couples_sizer.Add(self.couples_save_btn)
        self.sizer.Add(self.couples_sizer)

        # JUDGES SETUP

        self.judges_box = wx.StaticBox(self, -1, "Judges Setup")
        self.judges_sizer = wx.StaticBoxSizer(self.judges_box, wx.VERTICAL)
        self.judges_entries = []  # (StaticText, TextCtrl)

        for judge in judges.iteritems():
            judge_sizer = wx.BoxSizer(wx.HORIZONTAL)
            judge_label = wx.StaticText(
                self, -1, "{0}".format(judges.values().index(judge[1]) + 1), style=wx.TE_CENTRE)
            judge_label.SetMinSize((50, -1))
            judge_text = wx.TextCtrl(self, -1, judge[1])
            judge_text.SetMinSize((500, -1))
            judge_sizer.Add(judge_label)
            judge_sizer.AddSpacer(5)
            judge_sizer.Add(judge_text, 3, wx.EXPAND)
            self.judges_sizer.Add(judge_sizer)
            self.judges_sizer.AddSpacer(5)

            self.judges_entries.append((judge_label, judge_text))

        self.judges_save_btn = wx.Button(self, -1, "Save Judges Data")
        self.judges_sizer.Add(self.judges_save_btn)
        self.sizer.Add(self.judges_sizer)

        self.SetAutoLayout(True)
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

        self.judges_entries = []  # (StaticText, TextCtrl)

        judge_score_font = wx.Font(48, wx.SWISS, wx.NORMAL, wx.BOLD)

        i = 1
        for judge in judges.iteritems():
            judge_label = wx.StaticText(self, -1, judge[1])
            self.sizer.Add(judge_label, (1, i), (1, 1), wx.EXPAND)
            judge_score = wx.TextCtrl(self, -1, style=wx.TE_CENTRE)
            judge_score.SetFont(judge_score_font)
            self.sizer.Add(judge_score, (2, i), (1, 1), wx.EXPAND)

            i += 2

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

        self.scoreboard = sltd_scoreboard.Scoreboard(self)

        # Generate some fake couples for now
        for i in xrange(0, 10):
            c = sltd_couple.Couple()
            c.set_couple_name("Couple {0}".format(i))
            for j in xrange(0, 4):
                c.set_score(j, random.randint(1, 10))
            couple_mgr.add_couple(c, i)

        # And some judges
        for i in xrange(0, 4):
            judges[i] = "Judge {0}".format(i + 1)

        # Get list of couples in score order and add them to the leaderboard
        self.scoreboard.populate_scoreboard(
            couple_mgr.get_couples_order_score())

        self.tab_window = wx.Notebook(self, -1, style=wx.NB_TOP)

        self.panel_system_setup = SystemSetupPanel(self.tab_window)
        self.panel_system_setup.judges_save_btn.Bind(
            wx.EVT_BUTTON, self.on_save_judges_data)

        self.panel_scoring_judges = CoupleScoringJudgesPanel(self.tab_window)

        self.tab_window.AddPage(self.panel_system_setup, "Scoring Setup", True)
        self.tab_window.AddPage(self.panel_scoring_judges,
                                "Couple Scoring: Judges", False)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.tab_window, 3, wx.EXPAND)
        self.sizer.Add(self.scoreboard, 1, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)
        self.Layout()

        self.Show()

    def on_close(self, event):
        """
        Do a thing to make a thing happen
        :param event: The event provided by wxWindows
        :return:
        """
        self.Destroy()

    def on_save_judges_data(self, event):
        """Update new judge names"""

        judges.clear()

        for i in xrange(0, 4):
            judges[i] = self.panel_system_setup.judges_entries[i][1].GetValue()
            print "Saving Judge {0} as {1}".format(i, judges[i])
