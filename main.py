def userVerification(enteredUser):
    ah = open("admins.txt")
    uh = open("users.txt")

    adminList = ah.read()
    userList = uh.read()

    admins = adminList.split(",")
    users = userList.split(",")

    if enteredUser in admins:
        return 2
    elif enteredUser in users:
        return 1
    else:
        return 0

def loadApprovedEvents():
    eh = open ("approvedevents.txt")

    approvedEvents = eh.readlines()

    return approvedEvents

def saveApprovedEvents():
    print("not done")

def eventEntry():
    event = []

    eventName = input("Enter event name")
    eventDate = input("Enter event date")
    eventPoints = input("Enter event points")

    event.insert(0, eventDate)
    event.insert(1, eventPoints)

    if input("You entered '%s', on '%s', for '%s' points, is this correct(type 'yes' if it is)?" % (
    eventName, eventDate, eventPoints)).lower() == "yes":
        approvedEvents[eventName] = event

def attendedEvent(username):
    print("not done")

def verifyEvent():
    print("not done")

def displayStats():
    print("not done")

def displayCommands(privLevel):

    if privLevel >= 2:
        print("Enter 'event' to create/delete/modify an event")
        print("Enter 'stats' to view statistics")
    if privLevel >= 1:
        print("Enter 'attend' to enter attendance")
        return(input("Enter command to execute: "))
    if privLevel == 0:
        print("Incorrect name, either you entered your name incorrectly, or you aren't in the system")
        quit()

print("Welcome to the Greek Life Point Calculator")

# Login handler
username = input("Please enter your name: ").title()
privLevel = userVerification(username)

done = False

# User input loop

if privLevel == 0:
    print("Incorrect login, contact an administrator")
else:
    while not done:
        displayCommands(privLevel)
        usrInput = input("Enter command to begin, or 'done' to finish")
        if usrInput == "event" and privLevel >= 2:
            eventEntry()
        elif usrInput == "stats" and privLevel >= 2:
            displayStats()
        elif usrInput == "attend" and privLevel >= 1:
            attendedEvent(username)
        else:
            print("Incorrect command or incorrect permission level.")

approvedEvents = {}
attendance = {}


