import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database import connect_db
from charts import show_pie_chart
from export import export_csv

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker Dashboard")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f4f6f9")

        # Variables
        self.amount = tk.StringVar()
        self.category = tk.StringVar()
        self.desc = tk.StringVar()

        # ---------------- TITLE ----------------
        title = tk.Label(root, text="Expense Tracker", font=("Segoe UI", 22, "bold"), bg="#f4f6f9", fg="#2c3e50")
        title.pack(pady=10)

        # ---------------- MAIN FRAME ----------------
        main_frame = tk.Frame(root, bg="#f4f6f9")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ---------------- LEFT PANEL (FORM) ----------------
        form_frame = tk.Frame(main_frame, bg="white", bd=2, relief="ridge")
        form_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(form_frame, text="Add Expense", font=("Segoe UI", 14, "bold"), bg="white").pack(pady=10)

        tk.Label(form_frame, text="Amount", bg="white").pack(anchor="w", padx=10)
        tk.Entry(form_frame, textvariable=self.amount).pack(padx=10, pady=5, fill="x")

        tk.Label(form_frame, text="Category", bg="white").pack(anchor="w", padx=10)
        self.category_box = ttk.Combobox(form_frame, textvariable=self.category, state="readonly")
        self.category_box['values'] = ("Food", "Transport", "Bills", "Shopping", "Other")
        self.category_box.pack(padx=10, pady=5, fill="x")

        tk.Label(form_frame, text="Date", bg="white").pack(anchor="w", padx=10)
        self.date = DateEntry(form_frame)
        self.date.pack(padx=10, pady=5, fill="x")

        tk.Label(form_frame, text="Description", bg="white").pack(anchor="w", padx=10)
        tk.Entry(form_frame, textvariable=self.desc).pack(padx=10, pady=5, fill="x")

        tk.Button(form_frame, text="Add", bg="#27ae60", fg="white", command=self.add).pack(pady=5, fill="x", padx=10)
        tk.Button(form_frame, text="Update", bg="#2980b9", fg="white", command=self.update).pack(pady=5, fill="x", padx=10)
        tk.Button(form_frame, text="Delete", bg="#c0392b", fg="white", command=self.delete).pack(pady=5, fill="x", padx=10)

        # 🔥 NEW FEATURE BUTTONS
        tk.Button(form_frame, text="Show Chart", bg="#8e44ad", fg="white", command=self.show_chart).pack(pady=5, fill="x", padx=10)
        tk.Button(form_frame, text="Export CSV", bg="#16a085", fg="white", command=self.export_data).pack(pady=5, fill="x", padx=10)

        # ---------------- RIGHT PANEL (TABLE) ----------------
        table_frame = tk.Frame(main_frame, bg="white", bd=2, relief="ridge")
        table_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Amount", "Category", "Date", "Desc"),
            show="headings"
        )

        for col in ("ID", "Amount", "Category", "Date", "Desc"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.select)

        # ---------------- BOTTOM SUMMARY ----------------
        bottom_frame = tk.Frame(root, bg="#f4f6f9")
        bottom_frame.pack(fill="x")

        self.total = tk.Label(bottom_frame, text="Total: 0", font=("Segoe UI", 14, "bold"), bg="#f4f6f9", fg="#27ae60")
        self.total.pack(pady=10)

        self.selected = None
        self.load()

    # ---------------- ADD ----------------
    def add(self):
        if not self.amount.get() or not self.category.get():
            messagebox.showerror("Error", "Amount and Category required")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (amount, category, date, description) VALUES (%s,%s,%s,%s)",
            (self.amount.get(), self.category.get(), self.date.get_date(), self.desc.get())
        )
        conn.commit()
        conn.close()

        self.clear_fields()
        self.load()

    # ---------------- LOAD ----------------
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

        self.total.config(text=f"Total: {total}")
        conn.close()

    # ---------------- SELECT ----------------
    def select(self, event):
        row = self.tree.focus()
        data = self.tree.item(row, 'values')

        if data:
            self.selected = data[0]
            self.amount.set(data[1])
            self.category.set(data[2])
            self.date.set_date(data[3])
            self.desc.set(data[4])

    # ---------------- UPDATE ----------------
    def update(self):
        if not self.selected:
            messagebox.showwarning("Warning", "Select a record first")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE expenses SET amount=%s, category=%s, date=%s, description=%s WHERE id=%s",
            (self.amount.get(), self.category.get(), self.date.get_date(), self.desc.get(), self.selected)
        )
        conn.commit()
        conn.close()

        self.clear_fields()
        self.load()

    # ---------------- DELETE ----------------
    def delete(self):
        if not self.selected:
            messagebox.showwarning("Warning", "Select a record first")
            return

        confirm = messagebox.askyesno("Confirm", "Delete this expense?")
        if confirm:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id=%s", (self.selected,))
            conn.commit()
            conn.close()

            self.clear_fields()
            self.load()

    # ---------------- CHART FUNCTION ----------------
    def show_chart(self):
        try:
            show_pie_chart()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- EXPORT FUNCTION ----------------
    def export_data(self):
        try:
            export_csv()
            messagebox.showinfo("Success", "Data exported to expenses.csv")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- CLEAR ----------------
    def clear_fields(self):
        self.amount.set("")
        self.category.set("")
        self.desc.set("")
        self.selected = None
