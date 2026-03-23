import tkinter as tk
from tkinter import messagebox
from database import connect_db

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        tk.Label(root, text="Username").pack()
        self.username = tk.Entry(root)
        self.username.pack()

        tk.Label(root, text="Password").pack()
        self.password = tk.Entry(root, show="*")
        self.password.pack()

        tk.Button(root, text="Login", command=self.login).pack()
        tk.Button(root, text="Register", command=self.register).pack()

    def login(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",
                       (self.username.get(), self.password.get()))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Success", "Login Successful")
            self.root.destroy()
            import dashboard
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    def register(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s,%s)",
                       (self.username.get(), self.password.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "User Registered")