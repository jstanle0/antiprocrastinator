import sys

def printHelp():
    print("antiprocrastinator usage:")
    print("python antiprocrastinator.py [availability-file] [tasks-file]")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        try:
            with open(sys.argv[1], 'r') as availabilityFile:
                availabilty = availabilityFile.readlines()
            with open(sys.argv[2], 'r') as tasksFile:
                tasks = tasksFile.readlines()
        except:
            print("Error: Invalid filenames")
            sys.exit(1)
        print (availabilty)
    else:
        printHelp()
        sys.exit(1)
    