class Week:
    weekdays = ('Monday:', 'Tuesday:', 'Wednesday:', 'Thursday:', 'Friday:', 'Saturday:', 'Sunday:')
    def __init__(self, days=[]):
        self.days = days

    def addDay(self, day):
        self.days.append(day)
    
    def timeAvailable(self):
        dayAvailability = [day.timeAvailable() for day in self.days]
        return sum(dayAvailability)



class Day:
    def __init__(self, name, availability):
        self.availability = availability#{x:0 for x in range(24)}
        self.name = name
        self.tasks = {}
    
    def timeAvailable(self):
        return .5 * len(self.availability) or 0
    
    def addTask(self, time, task):
        self.tasks.update({time: task})
        self.availability.remove(time)