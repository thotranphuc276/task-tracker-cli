#!/usr/bin/env python3

import sys
import os
import json
import datetime

json_file = 'tasks.json'

class Task:
    def __init__(self, id, description, status, created_at, updated_at, completed_at):
        self.id = id
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.completed_at = completed_at

    def __str__(self):
        return f"{self.id}. {self.description} ({self.status})"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            description=data['description'],
            status=data['status'],
            created_at=datetime.datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None,
            completed_at=datetime.datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None
        )

def create_file():
    if not os.path.exists(json_file):
        with open(json_file, 'w') as f:
            json.dump([], f)

create_file()
tasks = []
if os.path.exists(json_file):
    with open(json_file, 'r') as f:
        tasks_data = json.load(f)
        tasks = [Task.from_dict(task) for task in tasks_data]

args = sys.argv[1:]

commands = ['add', 'update', 'delete', 'list', 'mark-done', 'mark-in-progress']

command = args[0]

if command not in commands:
    print(f"Invalid command: {command}")
    sys.exit(1)

def add_task(task_description):
    task = Task(id=len(tasks) + 1, description=task_description, status='todo', created_at=datetime.datetime.now(), updated_at=datetime.datetime.now(), completed_at=None)
    tasks.append(task)
    print(f"Task added: {task_description}")
    return task

def list_tasks(status=None):
    if status:
        return [task for task in tasks if task.status == status]
    else:
        return tasks

def update_task(task_id, task_description):
    task = tasks[int(task_id) - 1]
    task.description = task_description
    task.updated_at = datetime.datetime.now()
    print(f"Task updated: {task_description}")
    return task

def delete_task(task_id):
    tasks.pop(int(task_id) - 1)
    print(f"Task deleted: {task_id}")
    return tasks

def mark_task_done(task_id):
    task = tasks[int(task_id) - 1]
    task.status = 'done'
    task.completed_at = datetime.datetime.now()
    print(f"Task marked as done: {task_id}")
    return task

def mark_task_in_progress(task_id):
    task = tasks[int(task_id) - 1]
    task.status = 'in-progress'
    task.updated_at = datetime.datetime.now()
    print(f"Task marked as in progress: {task_id}")
    return task

if __name__ == '__main__':

    if command == 'add':
        add_task(args[1])
    elif command == 'list':
        status = args[1] if len(args) > 1 else None
        tasks_to_show = list_tasks(status)
        if not tasks_to_show:
            print("No tasks found.")
        else:
            for task in tasks_to_show:
                print(task)
    elif command == 'update':
        update_task(args[1], args[2])
    elif command == 'delete':
        delete_task(args[1])
    elif command == 'mark-done':
        mark_task_done(args[1])
    elif command == 'mark-in-progress':
        mark_task_in_progress(args[1])
    else:
        print(f"Invalid command: {command}")
        sys.exit(1)

    with open(json_file, 'w') as f:
        json.dump([task.to_dict() for task in tasks], f)
