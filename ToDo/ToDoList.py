import tkinter as tk
from tkinter import ttk, font
from datetime import datetime

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Task Manager")
        self.root.geometry("500x600")
        
        self.root.configure(bg="#121211")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._configure_styles()
        
        self.tasks = []
        self.load_tasks()
        self.create_widgets()

    def _configure_styles(self):
        self.style.configure("TFrame", background="#121211")
        self.style.configure("TLabel", background="#121211", foreground="#ffffff")
        self.style.configure("TButton", background="#1e1e1e", foreground="#ffffff", borderwidth=0)
        self.style.map("TButton", background=[("active", "#2a2a2a")])
        self.style.configure("TEntry", fieldbackground="#1e1e1e", foreground="#ffffff", insertcolor="#ffffff")
        self.style.configure("Accent.TButton", background="#007acc", foreground="#ffffff")
        self.style.map("Accent.TButton", background=[("active", "#0098ff")])
        self.style.configure("Switch.TCheckbutton", background="#121211", foreground="#ffffff")

    def create_widgets(self):
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        title_label = ttk.Label(self.root, text="Task Manager", font=title_font)
        title_label.pack(pady=(20, 15))
        
        input_frame = ttk.Frame(self.root)
        input_frame.pack(fill="x", padx=20)
        
        self.task_input = ttk.Entry(input_frame, font=("Helvetica", 12))
        self.task_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.task_input.bind("<Return>", lambda event: self.add_task())
        
        add_button = ttk.Button(input_frame, text="Add Task", command=self.add_task, style="Accent.TButton")
        add_button.pack(side="right")

        self.task_list_frame = ttk.Frame(self.root)
        self.task_list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(self.task_list_frame)
        scrollbar.pack(side="right", fill="y")

        self.task_list = tk.Canvas(self.task_list_frame, bg="#1e1e1e", highlightthickness=0)
        self.task_list.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.task_list.yview)
        self.task_list.config(yscrollcommand=scrollbar.set)

        self.tasks_frame = ttk.Frame(self.task_list)
        self.task_list.create_window((0, 0), window=self.tasks_frame, anchor="nw")

        self.stats_label = ttk.Label(self.root, text="", font=("Helvetica", 10))
        self.stats_label.pack(pady=5)

        self.update_task_list()

    def add_task(self):
        task = self.task_input.get()
        if task:
            self.tasks.append({
                "text": task,
                "completed": False,
                "created_at": datetime.now().isoformat()
            })
            self.task_input.delete(0, tk.END)
            self.update_task_list()
            self.save_tasks()

    def update_task_list(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        
        for i, task in enumerate(self.tasks):
            task_frame = ttk.Frame(self.tasks_frame)
            task_frame.pack(fill="x", pady=5)

            check_var = tk.BooleanVar(value=task["completed"])
            checkbox = ttk.Checkbutton(task_frame, text=task["text"], 
                                       variable=check_var, 
                                       command=lambda i=i, var=check_var: self.toggle_task_completion(i, var),
                                       style="Switch.TCheckbutton")
            checkbox.pack(side="left", padx=5)

            delete_button = ttk.Button(task_frame, text="🗑️", 
                                       command=lambda i=i: self.delete_task(i),
                                       style="Accent.TButton", width=3)
            delete_button.pack(side="right", padx=5)

            created_at = datetime.fromisoformat(task["created_at"]).strftime("%Y-%m-%d %H:%M")
            date_label = ttk.Label(task_frame, text=created_at, font=("Helvetica", 8))
            date_label.pack(side="right", padx=10)

        self.tasks_frame.update_idletasks()
        self.task_list.config(scrollregion=self.task_list.bbox("all"))
        self.update_statistics()

    def update_statistics(self):
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task["completed"])
        stats_text = f"Total tasks: {total_tasks} | Completed: {completed_tasks} | Remaining: {total_tasks - completed_tasks}"
        self.stats_label.config(text=stats_text)

    def toggle_task_completion(self, i, var):
        self.tasks[i]["completed"] = var.get()
        self.update_statistics()
        self.save_tasks()

    def delete_task(self, i):
        del self.tasks[i]
        self.update_task_list()
        self.save_tasks()

    def save_tasks(self):
        with open("tasks.txt", "w") as f:
            for task in self.tasks:
                task_text = f"{task['text']} | {task['completed']} | {task['created_at']}\n"
                f.write(task_text)

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as f:
                for line in f:
                    task_data = line.strip().split(" | ")
                    task_text = task_data[0]
                    task_completed = task_data[1] == "True"
                    task_created_at = task_data[2]
                    self.tasks.append({
                        "text": task_text,
                        "completed": task_completed,
                        "created_at": task_created_at
                    })
        except FileNotFoundError:
            pass

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    app.run()
