import sys
from datetime import date, datetime
from task import Task
from availability import *

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
                    dayAvailability.append(curLine)
                i += 1
            week.addDay({day: dayAvailability})
        except Exception as e:
            print(f'Error: {e}')
            sys.exit(1)
    return week

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
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        printHelp()
        sys.exit(1)
    