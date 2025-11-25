import json
from datetime import datetime
import os
import io


_DTFORMAT = "%m-%d-%Y %H:%M:%S"
_DBFILE = "tasks.json"


class JSONTask:
    def __init__(self, _input: dict[str[str]] | io.TextIOWrapper | None = None):

        if isinstance(_input, io.TextIOWrapper) or input is None:
            with (_input or open(_DBFILE)) as f:
                self._fn = f.name
                self._tasks = json.load(f)

        if isinstance(_input, dict):
            self._tasks = _input

        else:
            raise ValueError("The argument, should be \"io.TextIOWrapper\" or should be in a JSON format! (dict[str[str]])")

        for k, v in self._tasks.items():
            # ID alteration check
            assert isinstance(k, str)
            assert k.isdecimal()

            assert isinstance(v, dict)

            dt = {}
            for key, val in v.items():
                
                # Key and value alteration check
                assert isinstance(key, str)
                assert isinstance(val, str)

                if key == 'createdAt' or key == 'updatedAt':
                    dt[key] = datetime.strptime(val, _DTFORMAT)

                assert k == 'status' and v in ['todo', 'in-progress', 'done']

            if dt['createdAt'] > dt['updatedAt']:
                raise ValueError()


class TaskManager:
    def __init__(self, task_obj: JSONTask):
        self._initial_task = {}
        self.description = None
        self.status = 'todo'
        self.created_at = datetime.strptime(datetime.today, _DTFORMAT)
        self.updated_at = datetime.strptime(datetime.today, _DTFORMAT)

        dt_today = datetime.strftime(datetime.now(), _DTFORMAT)

        id = 1
        while self._initial_task.get(str(id), False):
            id += 1


    def getTask(self):
        return self._initial_task


    def deleteTask(self, id:int):
        pass


    def updateTask(id:int):
        pass


    def markTaskDone(id:int) -> None:
        pass


    def markTaskInProgress(id:int) -> None:
        pass


    def finalize():
        pass
