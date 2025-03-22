import sys
from datetime import date, datetime, timedelta
from task import Task
from availability import *
import re
from random import choice

warnings = []
timeSortRE = re.compile(r"\b(\d\d?)\b")

def printHelp():
    print("antiprocrastinator usage:")
    print("python antiprocrastinator.py [availability-file] [tasks-file]")

def readTasks(inputTasks):
    #Remove header line
    inputTasks.pop(0)
    output = []
    for i, inputTask in enumerate(inputTasks):
        try:
            output.append(Task(*inputTask.split(', ')))
        except:
            raise ValueError(f"Invalid task format, line {i+2}")
    return output

def parseTime(time):
    '''
    Parses range of time into list of half-hour increments
    >>> parseTime('5:30-6:00')
    ['5:30']
    >>> parseTime('12:00-14:00')
    ['12:00', '12:30', '13:00', '13:30']
    >>> parseTime('0:00-3:30')
    ['0:00', '0:30', '1:00', '1:30', '2:00', '2:30', '3:00']
    '''
    timeRE = re.compile(r"\b([0-2]?\d:[03]0)")
    timeRange = timeRE.findall(time)
    if timeRange and len(timeRange)==2:
        start = int(timeRange[0].replace(':', ''))
        end = int(timeRange[1].replace(':', ''))
        output = []
        while start != end:
            if start // 100 >= 24:
                raise ValueError
            if start >= 1000:
                output.append(str(start)[:2] + ':' + str(start)[2:])
            elif start > 30:
                output.append(str(start)[:1] + ':' + str(start)[1:])
            elif start: #Force edge cases since 0 is one digit
                output.append('0:' + str(start))
            else: 
                output.append('0:00')
            if start%100 == 0:
                start += 30
            else:
                start += 70
        return output
    else:
        raise TypeError

def readAvailability(inputAvailability, i=0):
    week = Week()
    for count, day in enumerate(Week.weekdays):
        try:
            dayAvailability = []
            if count == len(Week.weekdays)-1:
                inputAvailability.append('')
                nextDay = ''
            else:
                nextDay = Week.weekdays[count + 1]
            while inputAvailability[i].strip() != nextDay:
                curLine = inputAvailability[i].strip()
                if curLine != '' and curLine != day:
                    dayAvailability.append(parseTime(curLine))
                i += 1
            week.addDay(Day(day, sum(dayAvailability,[])))
        except:
            raise ValueError(f'Invalid time format, line {i+1}')
    return week

def prioritize(tasks, availability):
    tasks.sort(key=lambda x:x.dueDate)
    #Resort days based on what day it is
    curWeekday = datetime.today().weekday()
    for i in range(curWeekday):
        availability.days.append(availability.days[0])
        availability.days.pop(0)
    #Get current day, remove all excess information
    t = datetime.today().strftime('%d%m%y')
    today = datetime.strptime(t, '%d%m%y')
    #Find which tasks are due this week
    withinWeek = today + timedelta(weeks=1)
    for task in tasks:
        if task.dueDate < today:
            raise ValueError(f"Task {task.name} is overdue")
        if task.dueDate < withinWeek:
            dif = (task.dueDate - today).days
            weekUntilDue = Week(availability.days[:dif + 1])
            processTasks([task], weekUntilDue)
            if task.time > 0:
                warnings.append(f"Task {task.name} is unable to be completed before it's due. {task.time} hours remain.")
                task.time = 0
        else:
            #Further out tasks loose priority
            if task.dueDate > withinWeek + timedelta(weeks=1):
                task.priority -= 3
    #Resort tasks based on priority
    tasks.sort(key=lambda x:x.priority, reverse=True)

def availabilityGenerator(availability):
    #Basic linear generator
    '''for day in availability.days:
        while day.availability:
            yield day.availability[0], day'''
    #Randomized generator
    availableDays = availability.days[:]
    while availableDays:
        randDay = choice(availableDays)
        if randDay.availability:
            yield choice(randDay.availability), randDay
        else:
            availableDays.remove(randDay)

def processTasks(tasks, availability):
    '''
    Function that compares tasks to availability and assigns them to available timeslots. Mutates objects that are entered.
    '''
    gen = availabilityGenerator(availability)
    for task in tasks:
        while task.time > 0:
            try:
                a, day = next(gen)
                day.addTask(a, task.name)
                task.time -= .5
            except StopIteration:
                return

def sortTasks(x):
    '''
    Key to sort tasks back in order based on a timestamp
    '''
    output = timeSortRE.findall(x[0])
    print(output)
    if int(output[1]) > 0:
        return int(output[0]) + .5
    return int(output[0])

def printSchedule(week):
    for day in week.days:
        print(day.name)
        sortedTasks = dict(sorted(day.tasks.items(), key=sortTasks))
        for task in sortedTasks:
            print(f" - {task}, {sortedTasks[task]}")
        print('')
    for warning in warnings:
            print(warning)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        try:
            with open(sys.argv[1], 'r') as availabilityFile:
                availabiltyInput = availabilityFile.readlines()
            with open(sys.argv[2], 'r') as tasksFile:
                tasksInput = tasksFile.readlines()
        except:
            print("Error: Invalid filenames")
            sys.exit(1)
        try:
            tasks = readTasks(tasksInput)
            availability = readAvailability(availabiltyInput)
            prioritize(tasks, availability)
            processTasks(tasks, availability)
            #If an task can't be completed, warn user
            for task in tasks:
                if task.time > 0:
                    warnings.append(f"{task.name} is unable to be completed this week. {task.time} hours remain.")
            #Place breaks in leftover available slots
            if availability.timeAvailable():
                processTasks([Task("Take a break!", 99, "01/01", 0)], availability)
            printSchedule(availability)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        printHelp()
        sys.exit(1)
    