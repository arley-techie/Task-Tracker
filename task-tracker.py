import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Task Tracker", 
                                     prog="task-tracker", 
                                     usage="task-tracker [options]",
                                     epilog="Author: arleydev")
    parser.add_argument("add", help="Add a new task")
    parser.add_argument("delete", help="Delete a task")
    parser.add_argument("update", help="Update a task")
    parser.add_argument("list", help="List all tasks")
    parser.add_argument("mark-in-progress", help="Mark a task as in progress")
    parser.add_argument("mark-done", help="Mark a task as completed")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    
    args = parser.parse_args()

    if args.add:
        print(f"Adding task: {args.add}")
    elif args.delete:
        print(f"Deleting task: {args.delete}")
    elif args.update:
        print(f"Updating task: {args.update}")
    elif args.list:
        print("Listing all tasks...")
    elif args.mark_in_progress:
        print(f"Marking task as in progress: {args.mark_in_progress}")
    elif args.mark_done:
        print(f"Marking task as completed: {args.mark_done}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()