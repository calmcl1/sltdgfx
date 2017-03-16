import wx

import sltd_couple
import sltd_scoreboard

import random
random.seed()

couple_mgr = sltd_couple.CoupleMgr()

class SystemSetupPanel(wx.Panel):
    """"""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # COUPLES SETUP

        self.couples_box = wx.StaticBox(self, -1, "Couples Setup")
        self.couples_sizer = wx.StaticBoxSizer(self.couples_box, wx.VERTICAL)
        self.couple_entries = [] # (StaticText, TextCtrl)

        for couple in couple_mgr.get_couples_order_id():
            couple_sizer = wx.BoxSizer(wx.HORIZONTAL)
            couple_label = wx.StaticText(self, -1, "{0}:".format(couple[0]), style=wx.TE_RIGHT| wx.TE_CENTRE)
            couple_text = wx.TextCtrl(self, -1, couple[1].couple_name)
            couple_text.SetMinSize((500,-1))
            couple_sizer.Add(couple_label)
            couple_sizer.AddSpacer(5)
            couple_sizer.Add(couple_text, 3, wx.EXPAND)
            self.couples_sizer.Add(couple_sizer)
            self.couples_sizer.AddSpacer(5)

            self.couple_entries.append((couple_label, couple_text))
        
        self.couples_save_btn = wx.Button(self,-1, "Save Couples Data")
        self.couples_sizer.Add(self.couples_save_btn)
        self.sizer.Add(self.couples_sizer)
        
        # JUDGES SETUP

        self.judges_box = wx.StaticBox(self, -1, "Judges Setup")
        self.judges_sizer = wx.StaticBoxSizer(self.judges_box, wx.VERTICAL)
        self.judges_entries = [] # (StaticText, TextCtrl)

        #for couple in couple_mgr.get_couples_order_id():
        #    couple_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #    couple_label = wx.StaticText(self, -1, "{0}:".format(couple[0]), style=wx.TE_RIGHT| wx.TE_CENTRE)
        #    couple_text = wx.TextCtrl(self, -1, couple[1].couple_name)
        #    couple_text.SetMinSize((500,-1))
        #    couple_sizer.Add(couple_label)
        #    couple_sizer.AddSpacer(5)
        #    couple_sizer.Add(couple_text, 3, wx.EXPAND)
        #    self.couples_sizer.Add(couple_sizer)
        #    self.couples_sizer.AddSpacer(5)
        
        self.judges_save_btn = wx.Button(self,-1, "Save Judges Data")
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

        self.scoreboard = sltd_scoreboard.Scoreboard(self)

        # Generate some fake couples for now
        for i in xrange(0, 10):
            c = sltd_couple.Couple()
            c.set_couple_name("Couple {0}".format(i))
            for j in xrange(0, 4):
                c.set_score(j, random.randint(1, 10))
            couple_mgr.add_couple(c, i)

        # Get list of couples in score order and add them to the leaderboard
        self.scoreboard.populate_scoreboard(couple_mgr.get_couples_order_score())

        self.tab_window = wx.Notebook(self, -1, style=wx.NB_TOP)

        self.panel_system_setup = SystemSetupPanel(self.tab_window)
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