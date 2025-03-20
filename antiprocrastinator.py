import sys
from datetime import date, datetime
from task import Task
from availability import *
import re
from random import randint, randrange

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
    for count, day in enumerate(Week.days):
        try:
            dayAvailability = []
            if count == len(Week.days)-1:
                inputAvailability.append('')
                nextDay = ''
            else:
                nextDay = Week.days[count + 1]
            while inputAvailability[i].strip() != nextDay:
                curLine = inputAvailability[i].strip()
                if curLine != '' and curLine != day:
                    dayAvailability.append(parseTime(curLine))
                i += 1
            week.addDay(Day(day, sum(dayAvailability,[])))
        except:
            raise ValueError(f'Invalid time format, line {i+1}')
    return week

def availabilityGenerator(availability):
    for day in availability.days:
        while day.availability:
            yield day.availability[0], day

def processTasks(tasks, availability):
    gen = availabilityGenerator(availability)
    for task in tasks:
        while task.time > 0:
            a, day = next(gen)
            day.addTask(a, task.name)
            task.time -= .5

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
            tasks.sort(key=lambda x:x.priority, reverse=True)
            availability = readAvailability(availabiltyInput)
            for day in availability.days:
                print(day.availability)
            processTasks(tasks, availability)
            for day in availability.days:
                print(day.availability)
                print(day.tasks)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        printHelp()
        sys.exit(1)
    