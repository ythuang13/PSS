import os

# menus
MAIN_MENU = """1. Manage task
2. Manage schedule
3. Quit"""

TASKS_MENU = """1. Create task
2. Find task
3. Delete task
4. Edit task
5. Back to main menu"""

SCHEDULE_MENU = """1. write schedule to file
2. read schedule from file
3. view schedule
4. Back to main menu"""

CREATE_TASK_MENU = """1. Create Recurring task
2. Create Transient task
3. Create Anti-task
4. Back to Manage Task menu"""

DAY_WEEK_MONTH_MENU = """1. Day
2. Week
3. Month
4. Back to Manage Schedule Menu"""

# constants
RECURRING_TASKS = [
    "Class",
    "Study",
    "Sleep",
    "Exercise",
    "Work",
    "Meal"
]


TRANSIENT_TASKS = [
    "Visit",
    "Shopping",
    "Appointment"
]

ANTI_TASKS = ["Cancellation"]

FREQUENCIES = [1, 7]

# special functions
def printHeader(title: str) -> None:
    '''print header with title'''
    def clearConsole() -> None:
        '''clear the console'''
        command = 'clear'
        if os.name in ('nt', 'dos'):
            command = 'cls'
        os.system(command)

    clearConsole()
    print("=" * 30)
    print("{:^30}".format(title))
    print("=" * 30 + "\n")

