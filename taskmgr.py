import json
from datetime import datetime
import io


DTFORMAT = "%m-%d-%Y %H:%M:%S"
DBFILE = "tasks.json"
TASK_STATUS = ['todo', 'in-progress', 'done']
TASK_PARS = ['description', 'status', 'updatedAt', 'createdAt']


class JSONTask:
    def __init__(self, _input: dict[str, dict[str, str]] | io.TextIOWrapper | None = None):
        self.fn = DBFILE

        if isinstance(_input, io.TextIOWrapper) or _input is None:
            with (_input or open(DBFILE)) as f:
                self.fn = f.name
                try:
                    self.__tasks = json.load(f)
                except json.decoder.JSONDecodeError:
                    self.__tasks = {}

        elif isinstance(_input, dict):
            self.__tasks = _input

        else:
            raise ValueError("The argument, should be \"io.TextIOWrapper\" or should be in a JSON format! \"dict[str, [str]]\"")
        
        if not(self.validate_alteration(self.__tasks)):
            raise ValueError(f'The file {self.fn}, has been altered!')


    @staticmethod
    def validate_alteration(tasks: dict[str, dict[str]]):
        for k, v in tasks.items():
            # ID alteration check
            if not(isinstance(k, str) and k.isdecimal() and isinstance(v, dict)):
                return True

            dt = {}
            for key, val in v.items():

                # Key and value alteration check
                if not(isinstance(key, str) and isinstance(val, str) and key in TASK_PARS) \
                    or key == 'status' and val not in TASK_STATUS:
                    return False

                if key == 'createdAt' or key == 'updatedAt':
                    dt[key] = datetime.strptime(val, DTFORMAT)
                
            if dt['createdAt'] > dt['updatedAt']:
                return False
        return True


    def getTasks(self):
        return self.__tasks


class TaskManager:
    def __init__(self, task: JSONTask):
        self.__task_obj = task
        self.__tasks = self.__task_obj.getTasks()
        self.__changes = False
        self.__dt_today = datetime.strftime(datetime.now(), DTFORMAT)

        self.id = 1
        while self.__tasks.get(str(self.id), False):
            self.id += 1
        self.id = str(self.id)


    def addTask(self, description:str) -> None:
        self.__tasks[self.id] = {
            'description': description,
            'status': 'todo',
            'createdAt': self.__dt_today,
            'updatedAt': self.__dt_today
        }
        self.__changes = True


    def getTasks(self) -> None:
        return self.__tasks


    def deleteTask(self, id:int) -> bool:
        if self.__tasks.get(str(id)):
            del self.__tasks[str(id)]
            self.__changes = True
            return True
        return False


    def updateTask(self, id:int, description:str) -> bool:
        if self.__tasks.get(str(id)):
            self.__tasks[str(id)]['description'] = description
            self.__tasks[str(id)]['updatedAt'] = self.__dt_today
            self.__changes = True
            return True
        return False


    def markTaskDone(self, id:int) -> bool:
        if self.__tasks.get(str(id)):
            self.__tasks[str(id)]['status'] = 'done'
            self.__changes = True
            return True
        return False


    def markTaskInProgress(self, id:int) -> bool:
        if self.__tasks.get(str(id)):
            self.__tasks[str(id)]['status'] = 'in-progress'
            self.__changes = True
            return True
        return False


    def finalize(self) -> bool:
        if self.__tasks and self.__task_obj.validate_alteration(self.__tasks) and self.__changes:
                with open(self.__task_obj.fn, 'w') as f:
                    json.dump(self.__tasks, f, indent=4, sort_keys=True)
                return True
        return False
