import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database import connect_db

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("900x600")

        self.amount = tk.StringVar()
        self.category = tk.StringVar()
        self.desc = tk.StringVar()

        frame = tk.Frame(root)
        frame.pack()

        tk.Entry(frame, textvariable=self.amount).grid(row=0, column=1)
        tk.Entry(frame, textvariable=self.category).grid(row=1, column=1)
        self.date = DateEntry(frame)
        self.date.grid(row=2, column=1)
        tk.Entry(frame, textvariable=self.desc).grid(row=3, column=1)

        tk.Button(frame, text="Add", command=self.add).grid(row=4, columnspan=2)
        tk.Button(frame, text="Update", command=self.update).grid(row=5, columnspan=2)
        tk.Button(frame, text="Delete", command=self.delete).grid(row=6, columnspan=2)

        self.tree = ttk.Treeview(root, columns=("ID","Amount","Category","Date","Desc"), show="headings")
        for col in ("ID","Amount","Category","Date","Desc"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<ButtonRelease-1>", self.select)

        self.total = tk.Label(root, text="Total: 0")
        self.total.pack()

        self.selected = None
        self.load()

    def add(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (amount, category, date, description) VALUES (%s,%s,%s,%s)",
                       (self.amount.get(), self.category.get(), self.date.get_date(), self.desc.get()))
        conn.commit()
        conn.close()
        self.load()

    def load(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses")
        rows = cursor.fetchall()

        total = 0
        for r in rows:
            self.tree.insert("", tk.END, values=r)
            total += float(r[1])

            self.load()