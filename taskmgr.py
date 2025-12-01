import json
from datetime import datetime
import io


__DTFORMAT = "%m-%d-%Y %H:%M:%S"
__DBFILE = "tasks.json"
__TASK_STATUS = ['todo', 'in-progress', 'done']
__TASK_PARS = ['description', 'status', 'updatedAt', 'createdAt']


class JSONTask:
    def __init__(self, _input: dict[str, dict[str, str]] | io.TextIOWrapper | None = None):
        self.fn = __DBFILE

        if isinstance(_input, io.TextIOWrapper) or _input is None:
            with (_input or open(__DBFILE)) as f:
                self.fn = f.name
                self.__tasks = json.load(f)

        elif isinstance(_input, dict):
            self.__tasks = _input

        else:
            raise ValueError("The argument, should be \"io.TextIOWrapper\" or should be in a JSON format! (dict[str, [str]])")
        
        if not(self.validate_alteration(self.__tasks)):
            raise ValueError(f'The file {self.fn}, has been altered!')


    @staticmethod
    def validate_alteration(tasks):
        for k, v in tasks.items():
            # ID alteration check
            if not(isinstance(k, str) and k.isdecimal() and isinstance(v, dict)):
                return True

            dt = {}
            for key, val in v.items():

                # Key and value alteration check
                if not(isinstance(key, str) and isinstance(val, str) and key in __TASK_STATUS):
                    return False

                if key == 'createdAt' or key == 'updatedAt':
                    dt[key] = datetime.strptime(val, __DTFORMAT)
                
            if dt['createdAt'] > dt['updatedAt']:
                raise ValueError()
        return True


    def getTasks(self):
        return self.__tasks


class TaskManager:
    def __init__(self, task: JSONTask):
        self.__task_obj = task
        self.__tasks = self.__task_obj.getTasks()
        self.__changes = False
        self.__dt_today = datetime.strftime(datetime.now(), __DTFORMAT)

        self.__id = 1
        while self.__tasks.get(str(self.__id), False):
            self.__id += 1
        self.__id = str(id)


    def addTask(self, description):
        self.__tasks[self.__id] = {
            'description': description,
            'status': 'todo',
            'createdAt': self.__dt_today,
            'updatedAt': self.__dt_today
        }
        self.__changes = True

    def getTasks(self):
        return self.__tasks


    def deleteTask(self, id:int):
        self.__changes = True
        del self.__tasks[str(id)]


    def updateTask(self, id:int, description):
        self.__tasks[str(id)]['description'] = description
        self.__tasks[str(id)]['updateAt'] = self.__dt_today
        self.__changes = True


    def markTaskDone(self, id:int) -> None:
        self.__tasks[str(id)]['status'] = 'done'
        self.__changes = True


    def markTaskInProgress(self, id:int) -> None:
        self.__tasks[str(id)]['status'] = 'in-progress'
        self.__changes = True


    def finalize(self):
        if self.__tasks:
            if self.__task_obj.validate_alteration(self.__tasks) and self.__changes:
                with open(self.__task.fn, 'a') as f:
                    json.dump(self.__tasks, f, indent=4, sort_keys=True)
                return True
        return False
