class Couple(object):

    def __init__(self):

        self.couple_name = ""
        self.scores = [0, 0, 0, 0]
        self.total = sum(self.scores)

    def __updateTotal(self):
        self.total = sum(self.scores)

    def set_score(self, score_no, value):
        self.scores[score_no] = value
        self.__updateTotal()

class CoupleList(object):
    def __init__(self):
        pass