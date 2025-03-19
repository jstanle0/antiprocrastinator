class Week:
    days = ('Monday:', 'Tuesday:', 'Wednesday:', 'Thursday:', 'Friday:')
    def __init__(self):
        self.days = {}

    def addDay(self, day):
        self.days.update(day)



class Day:
    def __init__(self, availability):
        self.availability = availability