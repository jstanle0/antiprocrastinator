class Week:
    days = ('Monday:', 'Tuesday:', 'Wednesday:', 'Thursday:', 'Friday:')
    def __init__(self):
        self.days = []

    def addDay(self, day):
        self.days.append(day)
    
    def timeAvailable(self):
        return sum([day.timeAvailable for day in self.days])



class Day:
    def __init__(self, name, availability):
        self.availability = availability#{x:0 for x in range(24)}
        self.name = name
        self.tasks = {}
    
    def timeAvailable(self):
        return .5 * len(self.availability)
    
    def addTask(self, time, task):
        self.tasks.update({time: task})
        self.availability.remove(time)