import tkinter as tk
from tkinter import messagebox
import os

FILE_NAME = 'tasks.txt'

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, 'r') as file:
        tasks = file.readlines()
    return [task.strip() for task in tasks]

def save_tasks(tasks):
    with open(FILE_NAME, 'w') as file:
        for task in tasks:
            file.write(task + '\n')

def add_task():
    task = task_entry.get()
    if task:
        tasks = load_tasks()
        tasks.append(f"INCOMPLETE:{task}")
        save_tasks(tasks)
        task_entry.delete(0, tk.END)
        update_task_list()
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

def delete_task():
    try:
        selected_task_index = task_listbox.curselection()[0]
        tasks = load_tasks()
        tasks.pop(selected_task_index)
        save_tasks(tasks)
        update_task_list()
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to delete.")

def edit_task():
    try:
        selected_task_index = task_listbox.curselection()[0]
        tasks = load_tasks()
        old_task = tasks[selected_task_index]
        new_task = task_entry.get()
        if new_task:
            tasks[selected_task_index] = f"{old_task.split(':')[0]}:{new_task}"
            save_tasks(tasks)
            task_entry.delete(0, tk.END)
            update_task_list()
        else:
            messagebox.showwarning("Warning", "You must enter a task.")
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to edit.")

def mark_task_completed():
    try:
        selected_task_index = task_listbox.curselection()[0]
        tasks = load_tasks()
        task = tasks[selected_task_index]
        if task.startswith("INCOMPLETE:"):
            tasks[selected_task_index] = f"COMPLETE:{task[11:]}"
            save_tasks(tasks)
            update_task_list()
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to mark as completed.")

def filter_tasks(filter_type):
    task_listbox.delete(0, tk.END)
    tasks = load_tasks()
    if filter_type == 'All':
        filtered_tasks = tasks
    elif filter_type == 'Completed':
        filtered_tasks = [task for task in tasks if task.startswith("COMPLETE:")]
    elif filter_type == 'Incomplete':
        filtered_tasks = [task for task in tasks if task.startswith("INCOMPLETE:")]
    
    for task in filtered_tasks:
        task_listbox.insert(tk.END, task.split(':', 1)[1])

def update_task_list():
    filter_tasks(filter_var.get())

# Create the main window
root = tk.Tk()
root.title("To-Do App")

# Create a frame for the entry and buttons
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Create the task entry
task_entry = tk.Entry(frame, width=40)
task_entry.grid(row=0, column=0, padx=5, pady=5)

# Create the add task button
add_button = tk.Button(frame, text="Add Task", command=add_task)
add_button.grid(row=0, column=1, padx=5, pady=5)

# Create the edit task button
edit_button = tk.Button(frame, text="Edit Task", command=edit_task)
edit_button.grid(row=1, column=0, padx=5, pady=5)

# Create the mark as completed button
complete_button = tk.Button(frame, text="Mark as Completed", command=mark_task_completed)
complete_button.grid(row=1, column=1, padx=5, pady=5)

# Create the delete task button
delete_button = tk.Button(frame, text="Delete Task", command=delete_task)
delete_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Create filter buttons
filter_var = tk.StringVar(value='All')
filter_all = tk.Radiobutton(root, text="Show All", variable=filter_var, value='All', command=lambda: filter_tasks('All'))
filter_all.pack(anchor=tk.W, padx=10)
filter_complete = tk.Radiobutton(root, text="Show Completed", variable=filter_var, value='Completed', command=lambda: filter_tasks('Completed'))
filter_complete.pack(anchor=tk.W, padx=10)
filter_incomplete = tk.Radiobutton(root, text="Show Incomplete", variable=filter_var, value='Incomplete', command=lambda: filter_tasks('Incomplete'))
filter_incomplete.pack(anchor=tk.W, padx=10)

# Create the listbox to display tasks
task_listbox = tk.Listbox(root, width=50, height=15)
task_listbox.pack(padx=10, pady=10)

# Load existing tasks
update_task_list()

# Run the Tkinter event loop
root.mainloop()
