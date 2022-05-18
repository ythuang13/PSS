import json
import datetime
from datetime import date
import calendar
import string
import time
from task import RecurringTask, TransientTask, AntiTask, TaskEncoder
from setting import *

class PSS:
    def __init__(self) -> None:
        self._tasksList = []
        self._defaultFilePath = "data.json"

        if not self.fileVerification(self._defaultFilePath):
            open(self._defaultFilePath, 'w').close()

    def createTask(self) -> None:
        """User select type of task, pss verify data including,
        name, date, time and duration before create the task
        and store in tasksList"""
        running = True
        while running:
            printHeader("Create Task")
            print(CREATE_TASK_MENU)
            option = input("Enter option: ")
            if option == "1":
                # recurring task
                printHeader("Create Recurring Task")

                taskName = taskType = taskStartDate = taskEndDate = \
                    taskStartTime = taskDuration = taskFrequency = None
                try:
                    while not self.nameVerification(taskName):
                        taskName = input("Enter the Task Name: ")
                    while not self.typeVerification(RecurringTask("", 0.0, 0.0, "Sleep", 0, 0, 1), taskType):
                        print(RECURRING_TASKS)
                        taskType = input("Enter the type of Recurring Task: ").capitalize()
                    while not self.dateVerification(taskStartDate):
                        taskStartDate = int(input("Enter the Start Date of the Task (YYYYMMDD): "))
                    while not self.dateVerification(taskEndDate):
                        taskEndDate = int(input("Enter the End Date of the Task (YYYYMMDD): "))
                    while not self.timeVerification(taskStartTime):
                        taskStartTime = float(input("Enter the Start Time of the Task (0 - 23.75): "))
                    while not self.durationVerification(taskDuration):
                        taskDuration = float(input("Enter the Duration Time of the Task (0 - 23.75): "))
                    while not self.frequencyVerification(taskFrequency):
                        taskFrequency = int(input("Enter the Frequency of the Task (1 for daily, 7 for weekly): "))
                except ValueError:
                    continue

                newRecurringTask = RecurringTask(taskName, taskDuration, taskStartTime,
                    taskType, taskStartDate, taskEndDate, taskFrequency)
                
                newRecurringTask.displayTask()

                if input("Confirm Task Creation (Y or N)? ").capitalize() == "Y":
                    if not self.taskVerification(newRecurringTask):
                        print("Sorry, unable to create task. Possible incorrect data or overlapping with another task.")
                    else:
                        self._tasksList.append(newRecurringTask)
                        print("Task added to the schedule!")
                    input("Press enter to exit...")
                else:
                    print("Task was not created.")

            elif option == "2":
                # transient task
                printHeader("Create Transient Task")

                taskName = input("Enter the Task Name: ")
                print(TRANSIENT_TASKS)
                taskType = input("Enter the type of Transient Task: ").capitalize()
                try:
                    taskDate = int(input("Enter the Date of the Task (YYYYMMDD): "))
                    taskTime = float(input("Enter the Start Time of the Task (0 - 23.75): "))
                    taskDuration= float(input("Enter the Duration Time of the Task (0 - 23.75): "))
                except ValueError:
                    continue

                newTransientTask = TransientTask(taskName, taskDuration, taskTime, taskType, taskDate)

                while self.nameVerification(taskName) == False:
                    taskName = input("Invalid name, enter new Task Name: ")
            
                while self.typeVerification(newTransientTask, taskType) == False:
                    taskType = input("Invalid type, enter type of Transient Task: ")

                while self.dateVerification(taskDate) == False:
                    taskDate = int(input("Invalid date, enter the Date of the Task (YYYYMMDD): "))

                while self.timeVerification(taskTime) == False:
                    taskTime = float(input("Invalid time, nter the Start Time of the Task (0 - 23.75): "))

                while self.durationVerification(taskDuration) == False:
                    taskDuration = float(input("Invalid duration, enter the Duration Time of the Task (0 - 23.75): "))
                
                newTransientTask = TransientTask(taskName, taskDuration, taskTime, taskType, taskDate)

                newTransientTask.displayTask()

                if input("Confirm Task Creation (Y or N)? ").capitalize() == "Y":
                    if self.taskVerification(newTransientTask) == False:
                        print("Sorry, unable to create task. Possible incorrect data or overlapping with another task.")
                    else:
                        self._tasksList.append(newTransientTask)
                        print("Task added to the schedule!")
                    input("Press enter to exit...")
                else:
                    print("Task was not created.")
            elif option == "3":
                # anti-task
                printHeader("Create Anti Task")

                taskName = taskDate = taskStartTime = taskDuration = None
                try:
                    while not self.nameVerification(taskName):
                        taskName = input("Enter the Task Name: ")
                    while not self.dateVerification(taskDate):
                        taskDate = int(input("Enter the Start Date of the Task (YYYYMMDD): "))
                    while not self.timeVerification(taskStartTime):
                        taskStartTime = float(input("Enter the Start Time of the Task (0 - 23.75): "))
                    while not self.durationVerification(taskDuration):
                        taskDuration = float(input("Enter the Duration Time of the Task (0 - 23.75): "))
                except ValueError:
                    continue

                newAntiTask = AntiTask(taskName, taskDuration, taskStartTime, taskDate)
                newAntiTask.displayTask()

                if input("Confirm Task Creation (Y or N)? ").capitalize() == "Y":
                    if not self.taskVerification(newAntiTask):
                        print("Sorry, unable to create task. Possible incorrect data or overlapping with another task.")
                    else:
                        self._tasksList.append(newAntiTask)
                        print("Task added to the schedule!")
                    input("Press enter to exit...")
                else:
                    print("Task was not created.")
            elif option == "4":
                running = False
            else:
                print("Invalid option")    
                continue

    def findTask(self) -> None:
        """User search task by name.
        If found, display the task else display not found"""
        running = True
        while running:
            printHeader("Find Task")
            name_input = input("Enter the name of the task to find (empty to exit): ")
            if name_input == "":
                return
            else:
                for task in self._tasksList:
                    if task.getName() == name_input:
                        task.displayTask()
                        input("Press enter to exit...")
                        running = False
                        break
                else:
                    print(f"No task with name: {name_input} is found.")
        

    def deleteTask(self) -> None:
        """User select task to delete using task name.
        If found, validate if delete anti-task would create conflict,
        also delete recurring task and its anti-task together"""
        running = True
        while running:
            printHeader("Delete Task")
            name_input = input("Enter the name of the task to delete (empty to exit): ")
            if name_input == "":
                return
            else:
                for task in self._tasksList:
                    if task.getName() == name_input:
                        task.displayTask()
                        if isinstance(task, TransientTask):
                            if input("Type 'Y' to confirmed delete:") == 'Y':
                                self._tasksList.remove(task)
                        elif isinstance(task, RecurringTask):
                            if input("Any anti task associated with this task will also be deleted.\nType 'Y' to confirmed delete:") == 'Y':
                                for anti_task in self._tasksList:
                                    if (isinstance(anti_task, AntiTask) and 
                                    anti_task.getDate() >= task.getStartDate() and anti_task.getDate() <= task.getEndDate() and
                                    task.getDuration() == anti_task.getDuration and task.getStartTime() == anti_task.getStartTime()):
                                        self._tasksList.remove(anti_task)
                                        break
                                self._tasksList.remove(task)
                        else:
                            #Implementation
                            anti_task_temp = AntiTask(task.getName(), task.getDuration(), task.getStartTime(), task.getDate()) # will store this task in temp variable
                            self._tasksList.remove(task) # task is removed from the list
                            counter = 0 # counts how many task will cause a conflict if anti task is deleted
                            for anyTask in self._tasksList: 
                                if self.overlapVerification(anyTask):
                                    ++counter
                                    print("%s", anyTask.getName())
                            if counter > 0:
                                print(CONFLICT_ERROR)
                                print("These %d task(s) will cause conflict if %s anti-task is deleted\n", counter, anti_task_temp.getName())
                            else:
                                if input("This task is about to be deleted. Type 'Y' to confirmed delete") != 'Y':
                                    self._tasksList.append(anti_task_temp)
                        running = False
                        input("Press enter to exit")
                        break

                else:
                    print(f"No task with name: {name_input} is found.")
        

    def editTask(self) -> None:
        """User select task to edit using task name.
        If found, editor display the current attributes of the task
        and ask user to edit the attributes."""
        running = True
        while running:
            printHeader("Edit Task")

            name_input = input("Enter the name of the task to edit (empty to exit): ")
            if name_input == "":
                return 
            else:
                for task in self._tasksList:
                    if task.getName() == name_input:
                        print(task)
                        input("Press enter to exit...")
                        # todo edit here, check conflict still
                        running = False
                        break
                else:
                    print(f"No task with name: {name_input} is found ")

    def writeToFile(self, default=False) -> None:
        """Default is to write to default file path.
        otherwise, ask user for file name, check validity,
        and write schedule to the file using JSON format.
        Default is to do all, but user can specify for day, week, month and its start date.
        @param default: True if default file path is use, otherwise 
            ask for user input
        """
        if default:
            file_path = self._defaultFilePath

            # file verification
            if not self.fileVerification(file_path):
                open(file_path, 'w').close()

            # dumps json to file
            with open(file_path, "w") as file:
                file.write(json.dumps(self._tasksList, indent=4, cls=TaskEncoder))
        else:
            print(DAY_WEEK_MONTH_MENU)
            duration_input = input("Enter options number: ")
            if duration_input == "1":
                duration = "day"
            elif duration_input == "2":
                duration = "week"
            elif duration_input == "3":
                duration = "month"
            else:
                return
            file_path = input("Enter a file path with extension: ")

            start_date = None
            while not self.dateVerification(start_date):
                start_date_input = input("Enter a start date in YYYYMMDD format (all for all, empty to exit): ")
                try:
                    start_date = int(start_date_input)
                except ValueError:
                    print("Invalid date format")
                    return
                if start_date_input == "":
                    return
                
            
            # processing and sorting tasks to write to file
            result_task_list = []
            antitasks_list = []

            # time range
            start_year = start_date // 10000
            start_month = (start_date // 100) % 100
            start_day = start_date % 100
            end_year = start_year
            end_month = start_month
            end_day = start_day
            if duration == "week":
                end_day = start_day + 7
                if end_month in [1, 3, 5, 7, 8, 10, 12]:
                    if end_day > 31:
                        end_day = end_day - 31
                        end_month += 1
                elif end_month in [4, 6, 9, 11]:
                    if end_day > 30:
                        end_day = end_day - 30
                        end_month += 1
                elif end_month == 2:
                    if start_year % 4 == 0:
                        if end_day > 29:
                            end_day = end_day - 29
                            end_month += 1
                    else:
                        if end_day > 28:
                            end_day = end_day - 28
                            end_month += 1
                if end_month > 12:
                    end_month = end_month - 12
                    end_year += 1
                
            elif duration == "month":
                end_month += 1
                if end_month > 12:
                    end_month = end_month - 12
                    end_year += 1            
            

            # remove recurring task that's cancel out with anti-task
            for task in self._tasksList:
                if isinstance(task, AntiTask):
                    antitasks_list.append(task)
            
            for task in self._tasksList:
                if isinstance(task, RecurringTask):
                    if task.getFrequency() == 1:
                        # daily
                        counter = 1
                        for day in range(start_date, end_year * 10000 + end_month * 100 + end_day):
                            if self.dateVerification(day):
                                result_task_list.append(RecurringTask(task.getName() + str(counter),
                                    task.getDuration(), task.getStartTime(), task.getType(),
                                    day, day, 1))
                            counter += 1
                    else:
                        # weekly
                        counter = 1
                        for day in range(start_date, end_year * 10000 + end_month * 100 + end_day, 7):
                            if self.dateVerification(day):
                                result_task_list.append(RecurringTask(task.getName() + str(counter),
                                    task.getDuration(), task.getStartTime(), task.getType(),
                                    day, day, 1))
                            counter += 1
                elif isinstance(task, TransientTask):
                    result_task_list.append(task)

            # todo sorting

            # dumps processed tasks to file
            with open(file_path, "w") as file:
                file.write(json.dumps(result_task_list, indent=4, cls=TaskEncoder))
            

    def readFromFile(self, default=False) -> bool:
        """Default is to read from default file path.
        otherwise, ask user for file name, check validity,
        and read schedule to the file using JSON format.
        Need to check task information before store the data.
        Default is to do all, but user can specify for day, week, month and its start date.
        @param default: True if default file path is use, otherwise 
        ask for user input
        @return True if read successfully, anaything else False
        """
        if default:
            file_path = self._defaultFilePath
        else:
            file_path = input("Enter file path: ")
        
        if not self.fileVerification(file_path):
            return False
        json_string = open(file_path, 'r').read()
        if not self.jsonVerification(json_string):
            return False

        # file exists and in json format
        # load in date in pss
        data = json.loads(json_string)
        # loop through data to determine if it can be load in pss
        for task in data:
            task_name = task.get('Name', None)
            task_duration = task.get('Duration', None)
            task_start_time = task.get('StartTime', None)
            task_type = task.get('Type', "Cancellation")
            
            task_start_date = None
            task_end_date = None
            task_frequency = None
            task_date = None

            # determine by the task_type, have different attributes
            new_task = None
            if task_type in RECURRING_TASKS:
                # recurring task
                task_start_date = task.get('StartDate', None)
                task_end_date = task.get('EndDate', None)
                task_frequency = task.get('Frequency', None)
                new_task = RecurringTask(task_name, task_duration,
                    task_start_time, task_type, task_start_date,
                    task_end_date, task_frequency)
            elif task_type in TRANSIENT_TASKS:
                # transient task
                task_date = task.get('Date', None)
                new_task = TransientTask(task_name, task_duration,
                    task_start_time, task_type, task_date)
            elif task_type in ANTI_TASKS:
                # anti-task, cancellation
                task_date = task.get('Date', None)
                new_task = AntiTask(task_name, task_duration,
                    task_start_time, task_date)
            else:
                # invalid task type, big no no
                pass

            # if task verified, load into pss
            if self.taskVerification(new_task):
                self._tasksList.append(new_task)
        
        return True

    def viewSchedule(self) -> None:
        """User input the start date and the period for the schedule.
        PSS sort and display all of the tasks, except for 
        recurring that's cancel out with anti-task
        """
        printHeader("View Schedule")
        print(DAY_WEEK_MONTH_MENU)
        duration_input = input("Enter options: ")
        if duration_input == "1":
            duration = "day"
        elif duration_input == "2":
            duration = "week"
        elif duration_input == "3":
            duration = "month"
        else:
            return

        start_date = None
        while not self.dateVerification(start_date):
            printHeader("View Schedule")
            start_date_input = input("Enter a start date in YYYYMMDD format (empty to exit): ")
            try:
                start_date = int(start_date_input)
            except ValueError:
                print("Invalid date format")
                return
            if start_date_input == "":
                return
                
            
        # processing and sorting tasks to write to file
        result_task_list = []
        antitasks_list = []

        # time range
        start_year = start_date // 10000
        start_month = (start_date // 100) % 100
        start_day = start_date % 100
        end_year = start_year
        end_month = start_month
        end_day = start_day
        if duration == "week":
            end_day = start_day + 7
            if end_month in [1, 3, 5, 7, 8, 10, 12]:
                if end_day > 31:
                    end_day = end_day - 31
                    end_month += 1
            elif end_month in [4, 6, 9, 11]:
                if end_day > 30:
                    end_day = end_day - 30
                    end_month += 1
            elif end_month == 2:
                if start_year % 4 == 0:
                    if end_day > 29:
                        end_day = end_day - 29
                        end_month += 1
                else:
                    if end_day > 28:
                        end_day = end_day - 28
                        end_month += 1
            if end_month > 12:
                end_month = end_month - 12
                end_year += 1
            
        elif duration == "month":
            end_month += 1
            if end_month > 12:
                end_month = end_month - 12
                end_year += 1            
        

        # remove recurring task that's cancel out with anti-task
        for task in self._tasksList:
            if isinstance(task, AntiTask):
                antitasks_list.append(task)
        
        for task in self._tasksList:
            if isinstance(task, RecurringTask):
                if task.getFrequency() == 1:
                    # daily
                    counter = 1
                    temp_end_date = end_year * 10000 + end_month * 100 + end_day
                    for day in range(start_date, temp_end_date):
                        if self.dateVerification(day):
                            result_task_list.append(RecurringTask(task.getName() + str(counter),
                                task.getDuration(), task.getStartTime(), task.getType(),
                                day, day, 1))
                        counter += 1
                else:
                    # weekly
                    counter = 1
                    temp_end_date = end_year * 10000 + end_month * 100 + end_day
                    for day in range(start_date, temp_end_date, 7):
                        if self.dateVerification(day) and task.getEndDate() > day:
                            result_task_list.append(RecurringTask(task.getName() + str(counter),
                                task.getDuration(), task.getStartTime(), task.getType(),
                                day, day, 1))
                        counter += 1
            elif isinstance(task, TransientTask):
                if task.getDate() >= start_date and task.getDate() <= end_year * 10000 + end_month * 100 + end_day:
                    result_task_list.append(task)
        
        for task in result_task_list:
            task.displayTask()
            print()
        input("Press enter to exit...")

    def fileVerification(self, file_path: str) -> bool:
        """Check if the file is exists or not"""
        try:
            with open(file_path, 'r') as file:
                return True
        except FileNotFoundError:
            return False

    def jsonVerification(self, json_string: str) -> bool:
        """Check if the string is in valid JSON format or not"""
        try:
            json.loads(json_string)
            return True
        except json.decoder.JSONDecodeError as err:
            return False

    def taskVerification(self, task: RecurringTask or TransientTask or AntiTask) -> bool:
        """ Check whether the task is valid or not.
        Time must be correct format, no conflic, name must be unique.
        """
        # check name uniqueness
        if not self.nameVerification(task.getName()):
            return False

        # check type
        if not self.typeVerification(task, task.getType()):
            return False

        # check duration
        if not self.durationVerification(task.getDuration()):
            return False

        # check time 
        if not self.timeVerification(task.getStartTime()):
            return False

        # type specific verification
        if isinstance(task, RecurringTask):
            # check start date and end date
            if not self.dateVerification(task.getStartDate()):
                return False
            if not self.dateVerification(task.getEndDate()):
                return False

            # check frequency
            if not self.frequencyVerification(task.getFrequency()):
                return False

            # check end date after start date
            if task.getEndDate() < task.getStartDate():
                return False
            
        elif isinstance(task, TransientTask):
            # check date
            if not self.dateVerification(task.getDate()):
                return False

        elif isinstance(task, AntiTask):
            # check date
            if not self.dateVerification(task.getDate()):
                return False
        else:
            return False

        # check overlap
        if not self.overlapVerification(task):
            return False

        return True
    
    def overlapVerification(self, task: RecurringTask or TransientTask or AntiTask) -> bool:
        """Pass in a task to check if it overlap with any other task in the schedule"""

        #comparing RecurringTasks against other tasks
        if isinstance(task, RecurringTask):
            #run through all other tasks
            for other_task in self._tasksList:
                #check if there is overlap between two recurring tasks
                if isinstance(other_task, RecurringTask):

                    #get the start and end date of recurring tasks
                    task_start_date = task.getPythonFormatedDate(task.getStartDate())
                    task_end_date = task.getPythonFormatedDate(task.getEndDate())
                    other_start_date = other_task.getPythonFormatedDate(other_task.getEndDate())
                    other_end_date = other_task.getPythonFormatedDate(other_task.getEndDate())

                    #check if dates are overlapping 
                    if (not((task_start_date < other_start_date and task_end_date < other_start_date)or
                        (task_start_date > other_end_date and task_end_date > other_end_date))):


                       #three cases where times can overlap on same day
                       if(((task.getFrequency() == 1 and other_task.getFrequency() == 1) and
                          (task.dateClassification(task.getStartDate()) == 
                           other_task.dateClassification(other_task.getStartDate()))) or #case 1: same frequency and same day of week
                          (task.getFrequency() == 1 and other_task.getFrequency() == 7) or #case 2: frequency 1 and frequency 7
                          (task.getFrequency() == 7 and other_task.getFrequency() == 1)):  #case 3: frequecny 7 and frequency 1

                            #get start and end times of both tasks
                            task_start_time = task.getStartTime()
                            task_end_time = task_start_time + task.getDuration()
                            other_start_time = other_task.getStartTime()
                            other_end_time = other_start_time + other_task.getDuration()
                            
                            #check if the times of the class overlap
                            if(not((task_start_time < other_start_time and task_end_time <= other_start_time)or
                                (task_start_time >= other_end_time and task_end_time > other_end_time))):
                                return False


                #checking if a recurring task overlaps a transient task 
                elif isinstance(other_task, TransientTask):

                    #get the start and end date of recurring tasks
                    task_start_date = task.getPythonFormatedDate(task.getStartDate())
                    task_end_date = task.getPythonFormatedDate(task.getEndDate())
                    other_date = other_task.getPythonFormatedDate(other_task.getDate())

                    #check if they could occur on the same day
                    if((task.dateClassification(task.getStartDate()) == 
                        other_task.dateClassification(other_task.getDate())) or
                        #can also occur on same day if there is RecurringTask everyday with a TransientTask in those dates
                        (task.getFrequency() == 7 and (task_start_date <= other_date and task_end_date >= other_date))):

                        #get start and end times of both tasks
                        task_start_time = task.getStartTime()
                        task_end_time = task_start_time + task.getDuration()
                        other_start_time = other_task.getStartTime()
                        other_end_time = other_start_time + other_task.getDuration()
                        
                        #check if the times of the class overlap
                        if(not((task_start_time < other_start_time and task_end_time <= other_start_time)or
                            (task_start_time >= other_end_time and task_end_time > other_end_time))):
                            return False
                
                #checking if a recurring task overlaps a transient task 
                elif isinstance(other_task, AntiTask):

                    #get the start and end date of recurring tasks
                    task_start_date = task.getPythonFormatedDate(task.getStartDate())
                    task_end_date = task.getPythonFormatedDate(task.getEndDate())
                    other_date = other_task.getPythonFormatedDate(other_task.getDate())

                    #check if they could occur on the same day
                    if((task.dateClassification(task.getStartDate()) == 
                        other_task.dateClassification(other_task.getDate())) or
                        #can also occur on same day if there is RecurringTask everyday with a AntiTask in those dates
                        (task.getFrequency() == 7 and (task_start_date <= other_date and task_end_date >= other_date))):

                        #get start and end times of both tasks
                        task_start_time = task.getStartTime()
                        task_end_time = task_start_time + task.getDuration()
                        other_start_time = other_task.getStartTime()
                        other_end_time = other_start_time + other_task.getDuration()
                        
                        #check if the times of the class overlap
                        if(not((task_start_time < other_start_time and task_end_time <= other_start_time)or
                            (task_start_time >= other_end_time and task_end_time > other_end_time))):
                            return False
          
        #Comparing TransientTasks against other tasks
        elif isinstance(task, TransientTask):
            for other_task in self._tasksList:
                #Check if Transient task overlaps with recurring task
                if isinstance(other_task, RecurringTask):

                    #get the start and end date of recurring tasks
                    task_date = task.getPythonFormatedDate(task.getDate())
                    other_task_start_date = other_task.getPythonFormatedDate(other_task.getStartDate())
                    other_task_end_date = other_task.getPythonFormatedDate(other_task.getEndDate())

                    #check if they could occur on the same day
                    if((task.dateClassification(task.getDate()) == 
                        other_task.dateClassification(other_task.getStartDate())) or
                        #can also occur on same day if there is Transient task in the time fram of a Recurring task everyday
                        (other_task.getFrequency() == 7 and (other_task_start_date <= task_date and other_task_end_date >= task_date))):

                        #check if there is an anti-task recurring task and transient at the same time
                        for anti_task in self._tasksList:
                            if isinstance(anti_task, AntiTask): 

                                #if there all three tasks exist at the same time
                                all_three_check = False
                                #get the date of the anti-task
                                anti_task_date = task.getPythonFormatedDate(task.getDate())

                                if((other_task.dateClassification(task_start_date) == 
                                    anti_task.dateClassification(anti_task.getDate())) or
                                    #can also occur on same day if there is RecurringTask everyday with an AntiTask in those dates
                                    (other_task.getFrequency() == 7 and (task_start_date <= anti_task_date and task_end_date >= anti_task_date))):

                                    #get start and end times of both tasks
                                    anti_task_start_time = anti_task.getStartTime()
                                    anti_task_end_time = task_start_time + anti_task.getDuration()
                                    other_start_time = other_task.getStartTime()
                                    other_end_time = other_start_time + other_task.getDuration()       

                                    #if it matches the start and end time of recurring task it is valid so we don't compare it to
                                    #a recurring task
                                    if(((anti_task_start_time == other_start_time) and
                                        (anti_task_end_time == other_end_time))):
                                        all_three_check = True
                                        break
                    
                    #if a Transient Task, Anti Task and Recurring Task happen at the same time skip the check
                    if(all_three_check):
                        continue

                    #get start and end times of both tasks
                    task_start_time = task.getStartTime()
                    task_end_time = task_start_time + task.getDuration()
                    other_start_time = other_task.getStartTime()
                    other_end_time = other_start_time + other_task.getDuration()
                    
                    #check if the times of the class overlap
                    if(not((task_start_time < other_start_time and task_end_time <= other_start_time)or
                        (task_start_time >= other_end_time and task_end_time > other_end_time))):
                        return False

                #check TransientTask against TransientTask      
                elif isinstance(other_task, TransientTask):
                    #check if they have the same date
                    if (task.getDate() == other_task.getDate()):
                        #get start and end times of both tasks
                        task_start_time = task.getStartTime()
                        task_end_time = task_start_time + task.getDuration()
                        other_start_time = other_task.getStartTime()
                        other_end_time = other_start_time + other_task.getDuration()
                        
                        #check if the times of the class overlap
                        if(not((task_start_time < other_start_time and task_end_time <= other_start_time)or
                            (task_start_time >= other_end_time and task_end_time > other_end_time))):
                            return False

                #we dont need to check if it occurs at the same time as an AntiTask because this is allowed
                '''
                elif isinstance(other_task, AntiTask):
                    pass
                '''

        #Comparing AntiTask agaisnt other tasks 
        elif isinstance(task, AntiTask):
            for other_task in self._tasksList:

                #Check AntiTask against RecurringTask
                if isinstance(other_task, RecurringTask):
                    #get the start and end date of recurring tasks
                    task_date = task.getPythonFormatedDate(task.getDate())
                    other_start_date = other_task.getPythonFormatedDate(other_task.getStartDate())
                    other_end_date = other_task.getPythonFormatedDate(other_task.getEndDate())

                    #check if they could occur on the same day
                    if((task.dateClassification(task.getDate()) == 
                        other_task.dateClassification(other_task.getStartDate())) or
                        #can also occur on same day if there is RecurringTask everyday with a AntiTask in those dates
                        (other_task.getFrequency() == 7 and (other_start_date <= task_date and other_end_date >= task_date))):

                        #get start and end times of both tasks
                        task_start_time = task.getStartTime()
                        task_end_time = task_start_time + task.getDuration()
                        other_start_time = other_task.getStartTime()
                        other_end_time = other_start_time + other_task.getDuration()
                        
                        #check if the times of the class overlap
                        if(not(task_start_time == other_start_time and task_end_time == other_end_time)):
                            return False

                #check AntiTask against TransientTask
                elif isinstance(other_task, TransientTask):
                    #check if they have the same date
                    if (task.getDate() == other_task.getDate()):
                        #get start and end times of both tasks
                        task_start_time = task.getStartTime()
                        task_end_time = task_start_time + task.getDuration()
                        other_start_time = other_task.getStartTime()
                        other_end_time = other_start_time + other_task.getDuration()
                        
                        #check if the times of the class overlap
                        if(not((task_start_time < other_start_time and task_end_time <= other_start_time)or
                            (task_start_time >= other_end_time and task_end_time > other_end_time))):
                            return False

                #check AntiTask against AntiTask            
                elif isinstance(other_task, AntiTask):
                    #check if they have the same date
                    if (task.getDate() == other_task.getDate()):
                        #get start and end times of both tasks
                        task_start_time = task.getStartTime()
                        task_end_time = task_start_time + task.getDuration()
                        other_start_time = other_task.getStartTime()
                        other_end_time = other_start_time + other_task.getDuration()
                        
                        #check if the times of the class overlap
                        if(not((task_start_time < other_start_time and task_end_time <= other_start_time)or
                            (task_start_time >= other_end_time and task_end_time > other_end_time))):
                            return False
        #If it is not one of these three classes return False
        else:
            return False

        #return true if it does not fail any of these tests
        return True

    def timeVerification(self, time: float) -> bool:
        """Check whether the time is valid or not.
        Time must be a positive number from 0 to 23.75
        round to nearest 15 mins (0.25)
        """
        if not time:
            return False
        temp_time: float = time * 100
        if temp_time % 25 != 0:
            return False
        if temp_time < 0 or temp_time > 2375:
            return False
        return True

    def nameVerification(self, task_name: str) -> bool:
        """Return True if name is unique, else False"""
        if task_name == "" or task_name == None:
            return False

        for task in self._tasksList:
            name = task.getName()
            if task_name == name:
                return False
        return True

    def durationVerification(self, task_duration: float) -> bool:
        """Check whether the duration is valid or not."""
        if not task_duration:
            return False
        temp_duration: float = task_duration * 100
        if temp_duration < 0 or temp_duration > 2375:
            return False
        return True

    def typeVerification(self, task: RecurringTask or TransientTask or AntiTask,
            type: str) -> bool:
        """Check whether the type is valid or not."""
        if not type:
            return False
        if isinstance(task, RecurringTask):
            if type not in RECURRING_TASKS:
                return False
        elif isinstance(task, TransientTask):
            if type not in TRANSIENT_TASKS:
                return False
        elif isinstance(task, AntiTask):
            if type not in ANTI_TASKS:
                return False
        else:
            return False
        return True
        
    def frequencyVerification(self, frequency: int) -> bool:
        """Check whether the frequency is valid or not."""
        if not frequency:
            return False
        if frequency not in FREQUENCIES:
            return False
        return True

    def dateVerification(self, date: int) -> bool:
        """Check if the date is valid or not
        Date format: YYYYMMDD
        month range from [01-12], day range from [01-last day of the month]
        @param type: recurring, transient or anti
        """
        # len 8 check
        if len(str(date)) != 8:
            return False
        
        # separate into year, month, day
        day = int(date % 100)
        month = int((date // 100) % 100)
        year = date // 10000
        

        if year % 4 == 0:
            if day not in range(1, 30):
                return False
        # year check
        # if we need to check year

        # month check
        if month not in range(1, 13):
            return False
        
        # day check
        if month in [1, 3, 5, 7, 8, 10, 12]:
            if day not in range(1, 32):
                return False
        elif month in [4, 6, 9, 11]:
            if day not in range(1, 31):
                return False
        else:
            if day not in range(1, 29):
                return False

        return True

    def generateSchedule() -> None:
        """Generate schedule for a period of time in json format,
        default is all"""
        pass

    def displaySchedule() -> None:
        """Display the schedule, used for view schedule"""
        pass
