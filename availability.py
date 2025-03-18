class Week:
    days = ('Monday:', 'Tuesday:', 'Wednesday:', 'Thursday:', 'Friday:')
    def __init__(self):
        self.days = Week.days

    def nextDay(self):
        def getNextDay():
            for day in Week.days:
                yield day
        return getNextDay()



class Day:
    def __init__(self, availability):
        self.availability = availability