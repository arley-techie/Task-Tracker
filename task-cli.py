import sys
import json
import os
import os.path
from datetime import datetime

"""
Task Tracker CLI Application

A command-line interface (CLI) application for efficient task management. This tool helps
users organize and track their tasks through simple command-line operations. All tasks
are persistently stored in a JSON file for easy access and modification.

Features:
- Add new tasks with automatic 'todo' status assignment
- Delete tasks when they're no longer needed
- Update existing task details
- List all tasks with their current status
- Mark tasks as 'in-progress' or 'done'
- Simple and intuitive command-line interface
- Persistent storage using JSON format

Task Status Workflow:
    - todo: Initial status for newly created tasks (default)
    - in-progress: Tasks currently being worked on
    - done: Successfully completed tasks

Data Storage:
    Tasks are stored in 'tasks.json' in the following format:
    {
        id: {
            "description": "Task description",
            "status": "todo|in-progress|done"
            "createdAt": %datetime%
            "updatedAt": %datetime%
        }
    }

Example:
    python task-cli.py add "New Task"        # Add a new task
    python task-cli.py delete 1              # Remove task #1
    python task-cli.py update 1 "Updated"    # Modify task #1
    python task-cli.py list                  # Show all tasks
    python task-cli.py mark-in-progress 1    # Mark task #1 as in progress
    python task-cli.py mark-done 1           # Mark task #1 as completed

Author: arleydev
GitHub: arley-techie
"""

def printHelp():
    print(f"""Task Tracker CLI Application

Usage: python {sys.argv[0]} [options]

Options:
    add [ID]                        Add a new task
    
    update [ID][new_description]    Update the description of a task
    
    delete [ID]                     Delete a task
    
    list [todo|in-progress|done]    List a task (default: list all of the task)
    
    mark-in-progress [ID]           Mark the task "in-progress"
    
    mark-done [ID]                  Mark the task "done"

    help                            Show the help message


Example:
    python task-cli.py add "New Task"
    python task-cli.py delete 1
    python task-cli.py update 1 "Updated"
    python task-cli.py list
    python task-cli.py mark-in-progress 1
    python task-cli.py mark-done 1

Author: arleydev
GitHub: arley-techie
""")

def main():
    writeTask = lambda curr_task, filename: json.dump(curr_task, open(filename, 'w'), indent=4, sort_keys=True)
    reason_code = lambda opt, code: [
        f'Adding a new task is complete! (ID: {opt})',
        f'Deleting a task is complete! (ID: {opt})',
        f'ID #{opt} is not in the task list!',
        f'Command "{opt}" is not found!',
    ][code-100]

    args = sys.argv

    if len(args) == 1 or 'help' in args:
        printHelp()
        return 0

    jsontask = 'tasks.json'
    args = args[1:]
    dt_today = datetime.strftime(datetime.now(), "%m-%d-%Y %H:%M:%S")
    status_list = ['todo', 'in-progress', 'done']
    commands = ['add', 'update', 'delete', 'list', 'mark-in-progress', 'mark-done', 'help']

    tasks = {}

    try:
        if os.path.exists(jsontask):
            tasks = json.load(open(jsontask, 'r'))
    except json.decoder.JSONDecodeError:
        pass
    
    if args[0] in commands:
        if args[0] == 'add':
            id = 0
            while tasks.get(str(id), False):
                id += 1

            tasks[str(id)] = {
                'description': args[1].strip(),
                'status': status_list[0],
                'createdAt': dt_today,
                'updatedAt': dt_today
            }

            writeTask(tasks, jsontask)
            print(reason_code(id, 100))

        elif args[0] == 'delete':
            if tasks.pop(args[1], False):
                writeTask(tasks, jsontask)
                print(reason_code(id, 101))
            else:
                print(reason_code(id, 102))
                return 1

        elif args[0] == 'update':
            try:
                tasks[args[1]]['description'] = args[2].strip()
                tasks[args[1]]['updatedAt'] = dt_today
                writeTask(tasks, jsontask)
            except KeyError:
                print(reason_code(id, 102))
                return 1

        elif args[0] == 'list':
            if len(args) == 1:
                for i in tasks:
                    print(f'ID: {i}')
                    print(f'  Description: "{(tasks[i]['description'])}"')
                    print(f'  Status: "{tasks[i]['status']}"')
                    print(f'  Created Since: "{tasks[i]['createdAt']}"')
                    print(f'  Updated Since: "{tasks[i]['updatedAt']}"\n')
            elif args[1] in status_list:
                for i in tasks:
                    if tasks[i]['status'] == args[1]:
                        print(f'ID: "{i}"')
                        print(f'  Description: "{tasks[i]['description']}"')
                        print(f'  Status: "{tasks[i]['status']}"')
                        print(f'  Created Since: "{tasks[i]['createdAt']}"')
                        print(f'  Updated Since: "{tasks[i]['updatedAt']}"\n')

        elif args[0] == 'mark-in-progress':
            try:
                tasks[args[1]]['status'] = status_list[1]
                writeTask(tasks, jsontask)
            except KeyError:
                print(reason_code(id, 102))
                return 1

        elif args[0] == 'mark-done':
            try:
                tasks[args[1]]['status'] = status_list[2]
                writeTask(tasks, jsontask)
            except KeyError:
                print(reason_code(id, 102))
                return 1
        elif args[0] == 'help':
            printHelp()
    else:
        print(reason_code(args[0], 103))

    return 0

if __name__ == "__main__":
    sys.exit(main())