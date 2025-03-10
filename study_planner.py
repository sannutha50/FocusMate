import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database import add_task, get_tasks, mark_task_completed, generate_study_plan, insert_study_plan, insert_user

# ------------------ TASK MANAGEMENT FUNCTIONS ------------------
def load_tasks():
    # Clear existing tasks in the Treeview
    for row in tree.get_children():
        tree.delete(row)
    # Retrieve tasks from the database and insert them into the Treeview
    tasks = get_tasks()
    for task in tasks:
        tree.insert("", "end", values=(task[0], task[1], task[2], task[3], task[4]))

def add_new_task():
    subject = subject_entry.get()
    task = task_entry.get()
    deadline = deadline_entry.get()
    priority = priority_var.get()
    
    if subject and task and deadline:
        add_task(subject, task, deadline, priority)
        load_tasks()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields for the task.")

def complete_selected_task():
    selected_item = tree.selection()
    if selected_item:
        task_id = tree.item(selected_item)['values'][0]
        print("Marking task", task_id, "as completed")  # Debug print
        mark_task_completed(task_id)
        load_tasks()


# ------------------ STUDY PLAN GENERATION FUNCTIONS ------------------
def generate_plan():
    study_goals = study_goals_text.get("1.0", tk.END).strip()
    if not study_goals:
        messagebox.showwarning("Input Error", "Please enter your study goals.")
        return
    # Generate study plan using the BERT-based function
    study_plan = generate_study_plan(study_goals)
    # Insert a sample user and then the study plan into the database
    user_id = insert_user("sample_user", "password123")
    if user_id is None:
        messagebox.showerror("User Error", "Failed to insert or retrieve user.")
        return
    insert_study_plan(user_id, study_goals, study_plan)
    messagebox.showinfo("Study Plan Generated", f"Study Plan:\n{study_plan}")
    # Clear the text widget after generation
    study_goals_text.delete("1.0", tk.END)

# ------------------ SET UP THE GUI ------------------
root = tk.Tk()
root.title("Study Planner")

# ----- Task Management Section -----
task_frame = tk.Frame(root)
task_frame.pack(pady=10)

tk.Label(task_frame, text="Subject").grid(row=0, column=0)
tk.Label(task_frame, text="Task").grid(row=0, column=1)
tk.Label(task_frame, text="Deadline (YYYY-MM-DD)").grid(row=0, column=2)
tk.Label(task_frame, text="Priority").grid(row=0, column=3)

subject_entry = tk.Entry(task_frame)
task_entry = tk.Entry(task_frame)
deadline_entry = tk.Entry(task_frame)
priority_var = tk.StringVar(value="Medium")
priority_menu = ttk.Combobox(task_frame, textvariable=priority_var, values=["High", "Medium", "Low"])

subject_entry.grid(row=1, column=0)
task_entry.grid(row=1, column=1)
deadline_entry.grid(row=1, column=2)
priority_menu.grid(row=1, column=3)

tk.Button(root, text="Add Task", command=add_new_task).pack(pady=5)

tree = ttk.Treeview(root, columns=("ID", "Subject", "Task", "Deadline", "Priority"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Subject", text="Subject")
tree.heading("Task", text="Task")
tree.heading("Deadline", text="Deadline")
tree.heading("Priority", text="Priority")
tree.pack(pady=10)

tk.Button(root, text="Mark as Completed", command=complete_selected_task).pack(pady=5)

load_tasks()

# ----- Separator -----
separator = tk.Label(root, text="--------------------------------------------")
separator.pack(pady=10)

# ----- Study Plan Generation Section -----
plan_frame = tk.Frame(root)
plan_frame.pack(pady=10)

tk.Label(plan_frame, text="Enter Study Goals for Study Plan:").pack()

study_goals_text = tk.Text(plan_frame, height=5, width=50)
study_goals_text.pack(pady=5)

tk.Button(plan_frame, text="Generate Study Plan", command=generate_plan).pack(pady=5)

root.mainloop()
