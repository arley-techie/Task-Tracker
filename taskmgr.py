import json
from datetime import datetime
import io


_DTFORMAT = "%m-%d-%Y %H:%M:%S"
_DBFILE = "tasks.json"
_TASK_STATUS = ['todo', 'in-progress', 'done']


class JSONTask:
    def __init__(self, _input: dict[str, dict[str, str]] | io.TextIOWrapper | None = None):
        self._fn = _DBFILE

        if isinstance(_input, io.TextIOWrapper) or _input is None:
            with (_input or open(_DBFILE)) as f:
                self._fn = f.name
                self._tasks = json.load(f)

        elif isinstance(_input, dict):
            self._tasks = _input

        else:
            raise ValueError("The argument, should be \"io.TextIOWrapper\" or should be in a JSON format! (dict[str, [str]])")

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
                assert key in ['description', 'status', 'updatedAt', 'createdAt']

                if key == 'createdAt' or key == 'updatedAt':
                    dt[key] = datetime.strptime(val, _DTFORMAT)
                
                elif key == 'status' and val not in _TASK_STATUS:
                    raise ValueError()
                
            if dt['createdAt'] > dt['updatedAt']:
                raise ValueError()


    def getTasks(self):
        return self._tasks


class TaskManager:
    def __init__(self, task: JSONTask):
        self.__task = task
        self.__initial_task = task.getTasks()
        self.__dt_today = datetime.strftime(datetime.now(), _DTFORMAT)

        self.__id = 1
        while self.__initial_task.get(str(self.__id), False):
            self.__id += 1
        self.__id = str(id)


    def addTask(self, description):
        self.__initial_task[self.__id] = {
            'description': description,
            'status': 'todo',
            'createdAt': self.__dt_today,
            'updatedAt': self.__dt_today
        }


    def getTasks(self):
        return self.__initial_task


    def deleteTask(self, id:int):
        del self.__initial_task[str(id)]


    def updateTask(self, id:int, description):
        self.__initial_task[str(id)]['description'] = description
        self.__initial_task[str(id)]['updateAt'] = self.__dt_today


    def markTaskDone(self, id:int) -> None:
        self.__initial_task[str(id)]['status'] = 'done'


    def markTaskInProgress(self, id:int) -> None:
        self.__initial_task[str(id)]['status'] = 'in-progress'


    def finalize(self):
        with open(self.__task._fn, 'a') as f:
            json.dump(self.__initial_task, f)
