import sys
import taskmgr


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

GitHub: arley-techie
""")

def main():
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
    commands = ['add', 'update', 'delete', 'list', 'mark-in-progress', 'mark-done', 'help']
    tasks = taskmgr.JSONTask()
    tmgr = taskmgr.TaskManager(tasks)
    
    if args[0] in commands:
        if args[0] == 'add':
            tmgr.addTask(args[1])
            print(reason_code(id, 100))

        elif args[0] == 'delete':
            tmgr.deleteTask(args[1])
            print(reason_code(id, 101))

        elif args[0] == 'update':
            tmgr.updateTask(args[1], args[2])

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