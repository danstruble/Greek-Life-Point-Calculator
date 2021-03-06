import ast
import pandas as pd

# This function checks if the entered username is in either the user or admin file, and assigns a privilege level.
# This function also uses try excepts to ensure that the program doesn't break if you are missing the required files
# This will notify the user of the file that they are missing.
# Coded by Dan and Corey
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
# Coded by Dan and Jon
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
# Coded by Dan and Jon
def saveApprovedEvents():
    with open('approvedevents.txt', 'w+') as file:
        file.write(str(approvedEvents))

# Utilizes same method for approved events to load attended events dictionary from a text file, and evaluate it from a
# string to a dictionary. Also contains a fail safe if file does not exist or contains not a dictionary
# Coded by Dan and Jon
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
# Coded by Dan and Jon
def saveAttendedEvents():
    with open('attendedevents.txt', 'w+') as file:
        file.write(str(attendedEvents))
    print("done")

# This function allows you to enter approved event information into the approved events dictionary
# Coded by Dan and Grace
def eventEntry():
    finished = False
    while not finished:
        event = []

        eventName = input("Enter event name: ")
        eventDate = input("Enter event date (mm/dd/yy): ")
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
            indexEvents()

# This populates the index dictionaries to search for events
# Coded by Dan, Natalie, and Grace
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
# Coded by Dan, Natalie, Grace, Corey, and Jon
def searchEvents():
    searchTerm = input("Enter term to search for, or date (mm/dd/yy): ").lower()
    results = []

    for term in nameIndex:
        if searchTerm == term:
            results = nameIndex[term]
    for date in dateIndex:
        if searchTerm == date:
            results = dateIndex[date]

    if len(results) < 1:
        print("No events found with that search")
    else:
        print("ID\t| Name\t| Date")
        for result in results:
            print("%i  |  %s  |  %s" %(result, approvedEvents[result][0], approvedEvents[result][1]))


# This function allows administrators to tweak other user's attendance
# Main intention of this function is to prompt user for event ID, or search for an event using the indexed criteria
# Which appends the event id to the key value pair associated with the person's name
# Uses try excepts as an interesting approach to handle different data types being entered in one prompt
# Coded by Dan, Natalie, and Grace
def attendedEvent(username):
    finished = False

    if userVerification(username) >= 2:
        usrInput = input("Would you like to modify user attendance?: ")
        if usrInput.lower() == "yes":
            while not finished:
                user = input("Enter user to modify: ").title()
                if user.lower() == "done":
                    finished = True
                elif userVerification(user) < 1:
                    print("Incorrect user, try again.")
                else:
                    # show stats here
                    usrInput = input("Would you like to 'add' or 'delete' attendance for %s? or 'done' to finish: " %(user))

                    if usrInput.lower() == "done":
                        finished = True
                        saveAttendedEvents()

                    elif usrInput.lower() == "add":
                        attendedEvent(user)

                    elif usrInput.lower() == "delete":
                        print(attendedEvents[user])
                        usrInput = int(input("Specify an event to delete: "))
                        if usrInput in attendedEvents[user]:
                            attendedEvents[user].remove(usrInput)
                        else:
                            print("Incorrect event ID")

    while not finished:
        usrInput = input("Enter the event ID, hit enter to search for events, or 'done' to finish: ")
        if usrInput.lower() == "done":
            finished = True
            saveAttendedEvents()
        else:
            try:
                key = int(usrInput)

                if key in approvedEvents:
                    if username in attendedEvents:
                        if key in attendedEvents[username]:
                            usrInput = input("You already have attended this event, would you like to delete your attendance for this event?: ")
                            if usrInput.lower() == "yes":
                                attendedEvents[username].remove(key)
                        else:
                            currentList = attendedEvents[username]
                            currentList.append(key)
                            attendedEvents[username] = currentList
                    else:
                        attendedEvents[username] = [key]
                else:
                    print("Incorrect event ID, try again.")

            except ValueError:
                searchEvents()

# This function displays attendance stats, allowing admins to search for users or run a report for all users
# Regular users will be able to see their own stats.
# Coded by Dan, Natalie, Grace, and Corey
def displayStats():

    # This populates the dictionary with current stats from attendedEvents dictionary
    statsDict = {}

    for user in attendedEvents:
        statsDict[user] = len(attendedEvents[user])

    stats = pd.DataFrame.from_dict(statsDict, orient="index", columns=["Events Attended"])
    stats = stats.sort_values(by="Events Attended", ascending=False)

    if privLevel >= 2:
        usrInput = input("Do you want 'all' stats or a specific 'user'?: ").lower()
        if usrInput == "all":
            print(stats)

        elif usrInput == "user":
            usrInput = input("Which user do you want to run stats for?: ").title()

            if usrInput in attendedEvents:
                print("%s attended %s events" %(usrInput, statsDict[usrInput]))

            else:
                print("Incorrect user, or no recorded events.")

        else:
            print("Incorrect entry.")
    elif privLevel >= 1:
        print("You attended %s events" %(statsDict[username]))

# This function displays commands for the highest privilege level, and displays lower privilege level commands that the
# user can also use
# Coded by Dan, Corey, and Jon
def displayCommands(privLevel):

    if privLevel >= 2:
        print("Enter 'event' to create an event")
    if privLevel >= 1:
        print("Enter 'attend' to enter attendance")
        print("Enter 'search' to search events")
        print("Enter 'stats' to see statistics")

# Below was coded by Dan, Natalie, and Grace
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
        elif usrInput == "stats" and privLevel >= 1:
            displayStats()
        elif usrInput == "attend" and privLevel >= 1:
            attendedEvent(username)
        elif usrInput == "search" and privLevel >= 1:
            searchEvents()
        else:
            print("Incorrect command or incorrect permission level.")