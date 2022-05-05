from setting import ANTI_TASKS, FREQUENCIES, RECURRING_TASKS, TRANSIENT_TASKS
from json import JSONEncoder

class Task():
    def __init__(self, name: str, duration: float, startTime: float):
        self._name = name
        self._duration = duration
        self._start_time = startTime
        assert isinstance(self._name, str)
        assert isinstance(self._duration, float)
        assert isinstance(self._start_time, float)
    
    def getName(self) -> str:
        return self._name

    def getDuration(self) -> float:
        return self._duration
    
    def getStartTime(self) -> float:
        return self._start_time

    def displayTask(self) -> None:
        pass

class RecurringTask(Task):
    def __init__(self, name: str, duration: float, startTime: float,
            type: str, startDate: int, endDate: int, frequency: int):
        super().__init__(name, duration, startTime)
        self._type = type
        self._start_date = startDate
        self._end_date = endDate
        self._frequency = frequency

        assert isinstance(self._type, str)
        assert isinstance(self._start_date, int)
        assert isinstance(self._end_date, int)
        assert isinstance(self._frequency, int)
        assert self._start_date <= self._end_date
        assert self._frequency in FREQUENCIES
        assert self._type in RECURRING_TASKS
    
    def getType(self) -> str:
        return self._type
    
    def getStartDate(self) -> int:
        return self._start_date
    
    def getEndDate(self) -> int:
        return self._end_date
    
    def getFrequency(self) -> int:
        return self._frequency

    def displayTask(self) -> None:
        print(f"{self._name}: {self._type}, {'daily' if self._frequency == 1 else 'weekly'}")
        print(f"Date: {self._start_date} to {self._end_date}")
        print(f"Duration: {self._duration}")
        print(f"Start time: {self._start_time}")

class TransientTask(Task):
    def __init__(self, name: str, duration: float, startTime: float,
            type: str, date: int):
        super().__init__(name, duration, startTime)
        self._type = type
        self._date = date

        assert isinstance(self._type, str)
        assert isinstance(self._date, int)
        assert self._type in TRANSIENT_TASKS
    
    def getType(self) -> str:
        return self._type
    
    def getDate(self) -> int:
        return self._date

    def displayTask(self) -> None:
        print(f"{self._name}: {self._type}")
        print(f"Date: {self._date}")
        print(f"Duration: {self._duration}")
        print(f"Start time: {self._start_time}")
    
class AntiTask(Task):
    def __init__(self, name: str, duration: float, startTime: float,
            date: int):
        super().__init__(name, duration, startTime)
        self._date = date

        assert isinstance(self._date, int)
    
    def getDate(self) -> int:
        return self._date
    
    def getType(self) -> str:
        return "Cancellation"

    def displayTask(self) -> None:
        print(f"{self._name}: Cancellation")
        print(f"Date: {self._date}")
        print(f"Duration: {self._duration}")
        print(f"Start time: {self._start_time}")
    
class TaskEncoder(JSONEncoder):
    def default(self, o):
        result = {}
        if isinstance(o, RecurringTask):
            result["Name"] = o.getName()
            result["Type"] = o.getType()
            result["StartDate"] = o.getStartDate()
            result["StartTime"] = o.getStartTime()
            result["Duration"] = o.getDuration()
            result["EndDate"] = o.getEndDate()
            result["Frequency"] = o.getFrequency()
        elif isinstance(o, TransientTask):
            result["Name"] = o.getName()
            result["Type"] = o.getType()
            result["Date"] = o.getDate()
            result["StartTime"] = o.getStartTime()
            result["Duration"] = o.getDuration()
        elif isinstance(o, AntiTask):
            result["Name"] = o.getName()
            result["Type"] = o.getType()
            result["Date"] = o.getDate()
            result["StartTime"] = o.getStartTime()
            result["Duration"] = o.getDuration()

        return result