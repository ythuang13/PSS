class Task:
    def __init__(self, name: str, duration: float, startTime: float):
        self._name = name
        self._duration = duration
        self._start_time = startTime
    
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
    
    def getDate(self) -> int:
        return self._date

    def displayTask(self) -> None:
        pass
    