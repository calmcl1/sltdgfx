import wx


class ScoreItem(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.sizer = wx.GridBagSizer(hgap=10)

        self.position_no = wx.StaticText(self, -1, "")
        self.position_no.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.position_no.SetMinSize((50, -1))
        self.sizer.Add(self.position_no, (0, 0), (2, 1), wx.EXPAND)
        self.couple_name = wx.StaticText(self, -1, "")
        self.couple_name.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(self.couple_name, (0, 1), (1, 4), wx.EXPAND)
        self.score = wx.StaticText(self, -1, "", style=wx.ALIGN_RIGHT)
        self.score.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(self.score, (0, 5), (1, 1), wx.EXPAND)

        score_font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.score_1 = wx.StaticText(self, -1, "")
        self.score_1.SetFont(score_font)
        self.sizer.Add(self.score_1, (1, 1), (1, 1), wx.EXPAND)
        self.score_2 = wx.StaticText(self, -1, "")
        self.score_2.SetFont(score_font)
        self.sizer.Add(self.score_2, (1, 2), (1, 1), wx.EXPAND)
        self.score_3 = wx.StaticText(self, -1, "")
        self.score_3.SetFont(score_font)
        self.sizer.Add(self.score_3, (1, 3), (1, 1), wx.EXPAND)
        self.score_4 = wx.StaticText(self, -1, "")
        self.score_4.SetFont(score_font)
        self.sizer.Add(self.score_4, (1, 4), (1, 1), wx.EXPAND)

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

    def populate_scoreboard(self, couples_data):
        """Create all of the entries in the leaderboard according to the data passed in
        couples_data. 
        """

        for couple in couples_data:
            si = ScoreItem(self)
            si.set_couple_name(couple[1].couple_name)
            si.set_scores(couple[1].scores)
            si.set_total(couple[1].total)
            si.set_position(couples_data.index((couple[0], couple[1])) + 1)
            self.scoreItems.append(si)

            self.sizer.Add(si, 1, wx.EXPAND)

    def clear_scoreboard(self):
        for si in self.scoreItems:
            si.Destroy()
            self.scoreItems = []
