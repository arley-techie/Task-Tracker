import json
from datetime import datetime
import os
import io


_DTFORMAT = "%m-%d-%Y %H:%M:%S"
_DBFILE = "tasks.json"
_TASK_STATUS = ['todo', 'in-progress', 'done']


class JSONTask:
    def __init__(self, _input: dict[str, dict[str, str]] | io.TextIOWrapper | None = None):

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

                assert key == 'status' and val in _TASK_STATUS

            if dt['createdAt'] > dt['updatedAt']:
                raise ValueError()


    def select(self, target: int | list[int | str] | str | None = None, strict=False) -> dict[str, dict[str, str]] | dict[str, dict[str, str]] | None:
        out = {}

        if target is None or not(target):
            return self._tasks

        if isinstance(target, str):
            return {k:v for k, v in self._tasks.items() if v['status'] == target}

            # The difference of stricted and non-stricted:
            #   stricted:       It gives an error, if the target is not exist in the task
            #   non-stricted:   It only considers the existing id, based on the 
            #                   given argument, otherwise None (if nothing was found)

        elif isinstance(target, int):
            return self._tasks.get(self._tasks)

        if isinstance(strict, bool) and strict:
            if isinstance(target, list):
                for i in target:
                    out[str(target)] = self._tasks[str(target)]
                return out

        elif not(strict):
            if isinstance(target, list):
                return {k:self._tasks[k] for k in target if self._tasks.get(str(k))} or None

        elif not(isinstance(strict, bool)):
            raise TypeError()


class TaskManager:
    def __init__(self, task_obj: JSONTask):
        self._initial_task = task_obj
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
