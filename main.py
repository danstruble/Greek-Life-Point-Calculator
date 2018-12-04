import ast

# This function checks if the entered username is in either the user or admin file, and assigns a privilege level.
# This function also uses try excepts to ensure that the program doesn't break if you are missing the required files
# This will notify the user of the file that they are missing.
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

# This function loads the approved events dictionary from a text file, and does a literal evaluation to turn the string
# into a dictionary
def loadApprovedEvents():
    try:
        eh = open ("approvedevents.txt")
        approvedEvents = ast.literal_eval(eh.read())
    except FileNotFoundError:
        approvedEvents = {}

    return approvedEvents

# This function saves the approved event dictionary into a text file by turning it into a string
def saveApprovedEvents():
    with open('approvedevents.txt', 'w+') as file:
        file.write(str(approvedEvents))

# This function allows you to enter approved event information into the approved events dictionary
def eventEntry():
    finished = False
    while not finished:
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

        if input("Type 'done' to finish, or hit enter to continue entering other events: ").lower() == "done":
            finished = True
            saveApprovedEvents()

# This function adds the event key to a list in a person's dictonary entry to show event attendance
def attendedEvent(username):
    print("not done")

# This function displays attendance stats, allowing admins to search for users or run a report for all users
# Regular users will be able to see their own stats.
def displayStats():
    print("not done")

# This function displays commands for the highest privilege level, and displays lower privilege level commands that the
# user can also use
def displayCommands(privLevel):

    if privLevel >= 2:
        print("Enter 'event' to create/delete/modify an event")
        print("Enter 'stats' to view statistics")
    if privLevel >= 1:
        print("Enter 'attend' to enter attendance")


approvedEvents = loadApprovedEvents()
print(approvedEvents)
attendance = {}
done = False


print("Welcome to the Greek Life Point Calculator")
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



