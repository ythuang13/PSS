import json
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
            option = input("Enter task type: ")
            if option == "1":
                # recurring task
                pass
            elif option == "2":
                # transient task
                pass
            elif option == "3":
                # anti-task
                pass
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
            name_input = input("Enter name of the task to find (empty to exit): ")
            if name_input == "":
                return
            else:
                for task in self._tasksList:
                    if task.getName() == name_input:
                        print(task)
                else:
                    print("No task found")
        

    def deleteTask(self) -> None:
        """User select task to delete using task name.
        If found, validate if delete anti-task would create conflict,
        also delete recurring task and its anti-task together"""
        

    def editTask(self) -> None:
        """User select task to edit using task name.
        If found, editor display the current attributes of the task
        and ask user to edit the attributes."""
        pass

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
        else:
            file_path = input("Enter file path: ")

        # file verification
        if not self.fileVerification(file_path):
            return False
        
        # todo, user specify day

        # dumps json to file
        with open(file_path, "w") as file:
            file.write(json.dumps(self._tasksList, indent=4, cls=TaskEncoder))

        return True

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
        pass

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
        """Check if the task is overlap with other task or not"""
        if isinstance(task, RecurringTask):
            for other_task in self._tasksList:
                pass

        elif isinstance(task, TransientTask):
            for other_task in self._tasksList:
                if isinstance(other_task, RecurringTask):
                    pass
                elif isinstance(other_task, TransientTask):
                    if task.getDate() == other_task.getDate():
                        other_start_time = other_task.getStartTime()
                        other_end_time = other_start_time + other_task.getDuration()
                        task_start_time = task.getStartTime()
                        task_end_time = task_start_time + task.getDuration()
                        if task_start_time < other_start_time and task_end_time > other_start_time:
                            return False    
                        elif task_start_time > other_start_time and task_end_time <= other_end_time:
                            return False
                elif isinstance(other_task, AntiTask):
                    pass
        elif isinstance(task, AntiTask):
            # check for matchup with an instance of recurring task
            # only one anti-task can for one instance of recurring task
            for other_task in self._tasksList:
                if isinstance(other_task, RecurringTask):
                    pass
                elif isinstance(other_task, TransientTask):
                    pass
                elif isinstance(other_task, AntiTask):
                    pass
        else:
            return False

        return True

    def timeVerification(self, time: float) -> bool:
        """Check whether the time is valid or not.
        Time must be a positive number from 0 to 23.75
        round to nearest 15 mins (0.25)
        """
        temp_time: float = time * 100
        if temp_time % 25 != 0:
            return False
        if temp_time < 0 or temp_time > 2375:
            return False
        return True

    def nameVerification(self, task_name: str) -> bool:
        """Return True if name is uniqe, else False"""
        if task_name == "":
            return False

        for task in self._tasksList:
            name = task.getName()
            if task_name == name:
                return False
        return True

    def durationVerification(self, task_duration: float) -> bool:
        """Check whether the duration is valid or not."""
        temp_duration: float = task_duration * 100
        if temp_duration < 0 or temp_duration > 2375:
            return False
        return True

    def typeVerification(self, task: RecurringTask or TransientTask or AntiTask,
            type: str) -> bool:
        """Check whether the type is valid or not."""
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
