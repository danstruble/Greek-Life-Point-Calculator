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
# into a dictionary. Also contains a fail safe if file does not exist or contains not a dictionary
def loadApprovedEvents():
    try:
        eh = open ("approvedevents.txt")
        approvedEvents = ast.literal_eval(eh.read())
    except FileNotFoundError:
        approvedEvents = {}

    if not isinstance(approvedEvents, dict):
        approvedEvents = {}

    return approvedEvents

# This function saves the approved event dictionary into a text file by turning it into a string
def saveApprovedEvents():
    with open('approvedevents.txt', 'w+') as file:
        file.write(str(approvedEvents))

# Utilizes same method for approved events to load attended events dictionary from a text file, and evaluate it from a
# string to a dictionary. Also contains a fail safe if file does not exist or contains not a dictionary
def loadAttendedEvents():
    try:
        eh = open ("attendedevents.txt")
        attendedEvents = ast.literal_eval(eh.read())
    except FileNotFoundError:
        attendedEvents = {}

    if not isinstance(attendedEvents, dict):
        attendedEvents = {}
    return attendedEvents

# Utilizes same save method as above to save the attended dictionary to a text file
def saveAttendedEvents():
    with open('attendedevents.txt', 'w+') as file:
        file.write(str(attendedEvents))

# This function allows you to enter approved event information into the approved events dictionary
def eventEntry():
    finished = False
    while not finished:
        event = []

        eventName = input("Enter event name: ")
        eventDate = input("Enter event date: ")
        eventPoints = input("Enter event points: ")

        event.insert(0, eventName)
        event.insert(1, eventDate)
        event.insert(2, eventPoints)

        if input("You entered '%s', on '%s', for '%s' points, is this correct(type 'yes' if it is)?: " % (
        eventName, eventDate, eventPoints)).lower() == "yes":
            approvedEvents[len(approvedEvents)] = event

        print(approvedEvents)

        if input("Type 'done' to finish, or hit enter to continue entering other events: ").lower() == "done":
            finished = True
            saveApprovedEvents()

# This populates the index dictionaries to search for events
def indexEvents():
    nameIndex = {}
    dateIndex = {}

    # Main indexing for loop
    for entry in approvedEvents:
        terms = approvedEvents[entry][0].lower().split()
        date = approvedEvents[entry][1]
        # Indexes by name
        for term in terms:
            if term not in nameIndex:
                nameIndex[term] = [entry]
            else:
                currentEntry = nameIndex[term]
                currentEntry.append(entry)
                nameIndex[term] = currentEntry

        # Indexes by date
        if date not in dateIndex:
            dateIndex[date] = [entry]
        else:
            currentDates = dateIndex[date]
            currentDates.append(entry)
            dateIndex[date] = currentDates

    return [nameIndex,dateIndex]

# This function allows users to search for events by date or search term
def searcbEvents(nIndex, dIndex):
    searchTerm = input("Enter term to search for, or date (mm/dd/yy): ").lower()
    results = []

    for term in nIndex:
        if searchTerm == term:
            results = nIndex[term]
    for date in dIndex:
        if searchTerm == date:
            results = dIndex[date]

    if len(results) < 1:
        print("No events found with that search")
    else:
        for result in results:
            print("%i  |  %s  |  %s" %(result,approvedEvents[result][0],approvedEvents[result][1]))


# This function adds the event key to a list in a person's dictionary
#  entry to show event attendance
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
        print("Enter 'search' to search events")

# Startup

approvedEvents = loadApprovedEvents()
nameIndex = indexEvents()[0]
dateIndex = indexEvents()[1]
print(approvedEvents)
attendedEvents = loadAttendedEvents()
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
        elif usrInput == "search" and privLevel >= 1:
            searcbEvents(nameIndex,dateIndex)
        else:
            print("Incorrect command or incorrect permission level.")



