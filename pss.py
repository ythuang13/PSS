import json
from task import Task

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
        pass

    def findTask(self) -> None:
        """User search task by name.
        If found, display the task else display not found"""
        pass

    def deleteTask(self) -> None:
        """User select task to delete using task name.
        If found, validate if delete anti-task would create conflict,
        also delete recurring task and its anti-task together"""
        pass

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
            file.write(json.dumps(self._tasksList))

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
        if self.jsonVerification(json_string):
            # file exists and in json format
            # now load in date in pss
            data = json.loads(json_string)
            for task in data:
                task_name = task.get('Name', None)
                task_type = task.get('Type', None)

                # determine by the task_type, have different attributes

        else:
            return False
        
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

    def taskVerification(self, task: Task) -> bool:
        """ Check whether the task is valid or not.
        Time must be correct format, no conflic, name must be unique.
        """
        return True
    
    def timeVerification(self, time: float) -> bool:
        """Check whether the time is valid or not.
        Time must be a positive number from 0 to 23.75
        round to nearest 15 mins (0.25)
        """
        return True

    def nameVerification(self, task_name: str) -> bool:
        """Return True if name is uniqe, else False"""
        for task in self._tasksList:
            name = task.get("Name", None)
            if task_name == name:
                return False
        return True

    def dateVerification(self, date: float, task_type: str) -> bool:
        """Check if the date is valid or not
        Date format: YYYYMMDD
        month range from [01-12], day range from [01-last day of the month]
        end date must be later than start date.
        @param type: recurring, transient or anti
        """
        return True

    def generateSchedule() -> None:
        """Generate schedule for a period of time in json format,
        default is all"""
        pass

    def displaySchedule() -> None:
        """Display the schedule, used for view schedule"""
        pass
