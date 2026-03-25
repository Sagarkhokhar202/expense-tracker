import tkinter as tk
from tkinter import messagebox
from database import connect_db

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("720x480")
        self.root.configure(bg="#1e1e2f")

        # Center Frame (Card Style)
        card = tk.Frame(root, bg="#2b2b3c", bd=0)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Logo (Text-based)
        logo = tk.Label(card, text="🔐", font=("Arial", 40), bg="#2b2b3c", fg="#4CAF50")
        logo.pack(pady=(20, 5))

        title = tk.Label(card, text="Welcome Back", font=("Helvetica", 18, "bold"), bg="#2b2b3c", fg="white")
        title.pack(pady=(0, 15))

        # Username
        tk.Label(card, text="Username", bg="#2b2b3c", fg="#bbbbbb").pack(anchor="w", padx=30)
        self.username = tk.Entry(card, font=("Arial", 12), bd=0, bg="#3c3f58", fg="white", insertbackground="white")
        self.username.pack(padx=30, pady=5, ipady=6, fill="x")

        # Password
        tk.Label(card, text="Password", bg="#2b2b3c", fg="#bbbbbb").pack(anchor="w", padx=30)
        self.password = tk.Entry(card, show="*", font=("Arial", 12), bd=0, bg="#3c3f58", fg="white", insertbackground="white")
        self.password.pack(padx=30, pady=5, ipady=6, fill="x")

        # Buttons
        login_btn = tk.Button(card, text="Login", command=self.login,
                              bg="#4CAF50", fg="white", bd=0, padx=10, pady=8,
                              activebackground="#45a049", cursor="hand2")
        login_btn.pack(pady=(15, 5), ipadx=50)

        register_btn = tk.Button(card, text="Register", command=self.register,
                                 bg="#3c3f58", fg="white", bd=0, padx=10, pady=8,
                                 activebackground="#50536e", cursor="hand2")
        register_btn.pack(pady=(0, 20), ipadx=50)

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