# Task-Tracker
### A command-line interface (CLI) application for efficient task management. This tool helps users organize and track their tasks through simple command-line operations. All tasks are persistently stored in a JSON file for easy access and modification.

## Features
- Add new tasks with automatic 'todo' status assignment
- Delete tasks when they're no longer needed
- Update existing task details
- List all tasks with their current status
- Mark tasks as 'in-progress' or 'done'
- Simple and intuitive command-line interface
- Persistent storage using JSON format

## Task Status Workflow
- todo: Initial status for newly created tasks (default)
- in-progress: Tasks currently being worked on
- done: Successfully completed tasks

## Data Storage
Tasks are stored in 'tasks.json' in the following format:

```
{
    id: {
        "description": "Task description",
        "status": "todo|in-progress|done"
        "createdAt": "%datetime%"
        "updatedAt": "%datetime%"
    }
}
```

## Example 
```
python task-cli.py add "New Task"        # Add a new task
python task-cli.py delete 1              # Remove task #1
python task-cli.py update 1 "Updated"    # Modify task #1
python task-cli.py list                  # Show all tasks
python task-cli.py mark-in-progress 1    # Mark task #1 as in progress
python task-cli.py mark-done 1           # Mark task #1 as completed
```

#### GitHub: [arley-techie](https://github.com/arley-techie)
