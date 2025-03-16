from datetime import datetime, date

class Task:
    def __init__(self, name, time, dueDate, priority):
        self.name = name
        self.time = float(time)
        self.dueDate = datetime.strptime(f"{dueDate}/{datetime.now().year}", '%m/%d/%Y')
        self.priority = int(priority)
