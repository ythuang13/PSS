from setting import ANTI_TASKS, FREQUENCIES, RECURRING_TASKS, TRANSIENT_TASKS


class Task:
    def __init__(self, name: str, duration: float, startTime: float):
        self._name = name
        self._duration = duration
        self._start_time = startTime
        assert type(self._name) == str
        assert type(self._duration) == float
        assert type(self._start_time) == float
    
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

        assert type(self._type) == str
        assert type(self._start_date) == int
        assert type(self._end_date) == int
        assert type(self._frequency) == int
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
        pass

class TransientTask(Task):
    def __init__(self, name: str, duration: float, startTime: float,
            type: str, date: int):
        super().__init__(name, duration, startTime)
        self._type = type
        self._date = date

        assert type(self._type) == str
        assert type(self._date) == int
        assert self._type in TRANSIENT_TASKS
    
    def getType(self) -> str:
        return self._type
    
    def getDate(self) -> int:
        return self._date

    def displayTask(self) -> None:
        pass
    
class AntiTask(Task):
    def __init__(self, name: str, duration: float, startTime: float,
            date: int):
        super().__init__(name, duration, startTime)
        self._date = date

        assert type(self._date) == int
        assert self._type in ANTI_TASKS
    
    def getDate(self) -> int:
        return self._date

    def displayTask(self) -> None:
        pass
    