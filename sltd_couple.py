class Couple(object):
    """An object that represents a couple, with their name, score and other data."""

    def __init__(self):

        self.couple_name = ""
        self.scores = [0, 0, 0, 0]
        self.total = sum(self.scores)

    def __update_total(self):
        """Internal function used to update the total score when an indiviudal score is updated."""

        self.total = sum(self.scores)

    def set_score(self, score_no, value):
        """Set the value of an individual score. Also updates the total score to match.
        score_no should be 0 <= score_no < (amount of judges)"""

        self.scores[score_no] = value
        self.__update_total()

    def set_couple_name(self, name):
        """Update the name of the couple."""
        self.couple_name = name


class CoupleMgr(object):
    """Keeps all of the data regarding the list of couples"""

    def __init__(self):
        self.couples = {}

    def add_couple(self, couple, id=-1):
        """Add a new couple to the list."""
        if self.couples.has_key(id):
            return ValueError("Couple with key {0} already exists".format(id))

        self.couples[id] = couple

    def get_couple(self, couple_id):
        """Return the Couple with the given ID."""
        if self.couples.has_key(couple_id):
            return self.couples[couple_id]
        else:
            return KeyError("No couple exists with ID {0}".format(couple_id))

    def get_couples_order_score(self):
        """Return a list of couples in total score order, highest score first.
        Note: This returns a *copy* of the couple list - updating any of these couples will not
        update the leaderboard. Use `get_couple` to update actual couples."""
        return sorted(self.couples.iteritems(), key=lambda (k, v): v.total, reverse=True)

    def get_couples_order_id(self):
        """Return a list of couples ID order, lowest ID first.
        Note: This returns a *copy* of the couple list - updating any of these couples will not
        update the leaderboard. Use `get_couple` to update actual couples."""
        return sorted(self.couples.iteritems(), key=lambda (k, v): k)
