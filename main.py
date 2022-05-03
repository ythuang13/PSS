from pss import PSS
from setting import *

def main():
    # greeting
    print("Welcome to your personal schedule system (PSS)!")

    # initialize PSS
    pss = PSS()
    # initial load default file to have persistence data
    if not pss.readFromFile(default=True):
        print("Default file corrupted, please fix or delete.")
        return

    # main loop
    running = True
    while running:
        print(MAIN_MENU)
        option = input("Enter option: ")
        if option == "1":
            # manage task
            manageTask(pss)
        elif option == "2":
            # manage schedule
            manageSchedule(pss)
        elif option == "3":
            # quit
            print("Goodbye!")
            running = False
        else:
            print("Invalid option")

    # save back to default file before exiting program
    pss.writeToFile(default=True)

def manageTask(pss: PSS) -> None:
    running = True
    while running:
        print(TASKS_MENU)
        option = input("Enter option: ")
        if option == "1":
            # create task
            pss.createTask()
        elif option == "2":
            # find task
            pss.findTask()
        elif option == "3":
            # delete task
            pss.deleteTask()
        elif option == "4":
            # edit task
            pss.editTask()
        elif option == "5":
            # back to main menu
            running = False
        else:
            print("Invalid option")

def manageSchedule(pss: PSS) -> None:
    running = True
    while running:
        print(SCHEDULE_MENU)
        option = input("Enter option: ")
        if option == "1":
            # write schedule to file
            pss.writeToFile()
        elif option == "2":
            # read schedule from file
            pss.readFromFile()
        elif option == "3":
            # view schedule
            pss.viewSchedule()
        elif option == "4":
            # back to main menu
            running = False
        else:
            print("Invalid option")


if __name__ == '__main__':
    main()