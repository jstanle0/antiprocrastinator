class Week:
    days = ('Monday:', 'Tuesday:', 'Wednesday:', 'Thursday:', 'Friday:')
    def __init__(self):
        self.days = []

    def addDay(self, day):
        self.days.append(day)



class Day:
    def __init__(self, name, availability):
        self.availability = availability#{x:0 for x in range(24)}
        self.name = name
    
    def timeAvailable(self):
        return .5 * len(sum(self.availability, []))