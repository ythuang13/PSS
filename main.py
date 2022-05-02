from pss import PSS

def main():
    pss = PSS()
    pss.readFromFile(default=True)

    running = True
    while running:
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

    pss.writeToFile(default=True)

def manageTask(pss: PSS) -> None:
    pass

def manageSchedule(pss: PSS) -> None:
    pass


if __name__ == '__main__':
    main()