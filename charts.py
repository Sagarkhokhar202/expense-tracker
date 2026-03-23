import matplotlib.pyplot as plt
from database import connect_db

def show_pie_chart():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    categories = [d[0] for d in data]
    amounts = [d[1] for d in data]

    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title("Category-wise Expenses")
    plt.show()