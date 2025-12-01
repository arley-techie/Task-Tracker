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
    args = sys.argv

    if len(args) == 1 or 'help' in args:
        printHelp()
        return 0
    
    reasons = lambda opt: [
        f'Adding a new task is complete! (ID: {opt})',
        f'Deleting a task is complete! (ID: {opt})',
        f'Updating a task is complete! (ID: {opt})',
        f'ID #{opt} is not in the task list!',
        f'Marking as a "done" is complete! (ID: {opt})',
        f'Marking as "in-progress" is complete! (ID: {opt})',
        f'Command "{opt}" is not found!']
    
    reason_code = lambda opt, code: {k+100:v for k,v in enumerate(reasons(opt))}[code]
    
    args = args[1:]
    commands = ['add', 'update', 'delete', 'list', 'mark-in-progress', 'mark-done', 'help']
    rc = 0
    tasks = taskmgr.JSONTask()
    tmgr = taskmgr.TaskManager(tasks)
    x = False


    if args[0] in commands:
        if args[0] == 'add':
            tmgr.addTask(args[1])
            rc = (reason_code(tmgr.id, 100), 0)


        elif args[0] == 'delete':
            x = int(not(tmgr.deleteTask(args[1])))
            rc = (reason_code(args[1], 103 if x else 101), x)


        elif args[0] == 'update':
            x = not(tmgr.updateTask(args[1], args[2]))
            rc = (reason_code(args[1], 103 if x else 102), x)


        elif args[0] == 'list':
            t = tasks.getTasks()
            if len(args) == 2 and args[1] in taskmgr.TASK_STATUS:
                t = {k:v for k,v in t.items() if v['status'] == args[1]}
            
            if not(t):
                print("No task is in the list!")
                return 0

            for k,v in t.items():
                print(f'ID: "{k}"')
                print(f'  Description: "{v['description']}"')
                print(f'  Status: "{v['status']}"')
                print(f'  Created Since: "{v['createdAt']}"')
                print(f'  Updated Since: "{v['updatedAt']}"\n')
            
            return 0


        elif args[0] == 'mark-in-progress':
            x = int(not(tmgr.markTaskInProgress(args[1])))
            rc = (reason_code(args[1], 103 if x else 105), x)


        elif args[0] == 'mark-done':
            x = int(not(tmgr.markTaskDone(args[1])))
            rc = (reason_code(args[1], 103 if x else 104), x)


        elif args[0] == 'help':
            printHelp()
            return 0

    else:
        rc = (reason_code(args[0], 103), 1)

    if not(tmgr.finalize()):
        raise RuntimeError

    print(rc[0])

    return int(rc[1])

if __name__ == "__main__":
    sys.exit(main())