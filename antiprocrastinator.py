import sys

def printHelp():
    print("antiprocrastinator usage:")
    print("python antiprocrastinator.py [availability-file] [tasks-file]")

if __name__ == "__main__":
    if len(sys.argv) > 3:
        print("hi")
    else:
        printHelp()
    