def userVerification(enteredUser):
    try:
        ah = open("admins.txt")
    except FileNotFoundError:
        print("Missing admins file, check to make sure you have everything in the right directory")
        quit()
    try:
        uh = open("users.txt")
    except FileNotFoundError:
        print("Missing users file, check to make sure you have everything in the right directory")
        quit()

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
    try:
        eh = open ("approvedevents.txt")
        approvedEvents = eh.read()
    except FileNotFoundError:
        approvedEvents = {}

    return approvedEvents

def saveApprovedEvents():
    with open('approvedevents.txt', 'w') as file:
        file.write(approvedEvents)

def eventEntry():
    event = []

    eventName = input("Enter event name: ")
    eventDate = input("Enter event date: ")
    eventPoints = input("Enter event points: ")

    event.insert(0, eventDate)
    event.insert(1, eventPoints)

    if input("You entered '%s', on '%s', for '%s' points, is this correct(type 'yes' if it is)?: " % (
    eventName, eventDate, eventPoints)).lower() == "yes":
        approvedEvents[eventName] = event

    print(approvedEvents)

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


approvedEvents = {}
attendance = {}
done = False


print("Welcome to the Greek Life Point Calculator")
loadApprovedEvents()
# Login handler
username = input("Please enter your name: ").title()
print(username)
privLevel = userVerification(username)


# User input loop

if privLevel == 0:
    print("Incorrect login, contact an administrator")
else:
    while not done:
        displayCommands(privLevel)
        usrInput = input("Enter command to begin, or 'done' to finish: ").lower()
        if usrInput == "done":
            done = True
        elif usrInput == "event" and privLevel >= 2:
            eventEntry()
        elif usrInput == "stats" and privLevel >= 2:
            displayStats()
        elif usrInput == "attend" and privLevel >= 1:
            attendedEvent(username)
        else:
            print("Incorrect command or incorrect permission level.")



