import sqlite3
import tkinter as tk
from tkinter import messagebox

class ServiceProviderDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_file)

    def close(self):
        if self.conn:
            self.conn.close()

    def search_by_name(self, name):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                    SELECT * FROM service_providers
                    WHERE name LIKE ?
                    ORDER BY rating DESC
                ''', ('%' + name + '%',))
            rows = cursor.fetchall()
            self.print_results(rows)
        except sqlite3.Error as e:
            print(f"Error during search by name: {e}")

    def search_by_sector(self, sector, text_widget):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM service_providers
                WHERE sector = ?
                ORDER BY rating DESC
            ''', (sector,))
            rows = cursor.fetchall()
            self.print_results(rows, text_widget)
        except sqlite3.Error as e:
            print(f"Error during search by sector: {e}")

    def search_by_rating(self, text_widget):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                    SELECT * FROM service_providers
                    ORDER BY rating DESC
                ''')
            rows = cursor.fetchall()
            self.print_results(rows, text_widget)
        except sqlite3.Error as e:
            print(f"Error during search by rating: {e}")

    def search_by_price(self, text_widget):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                    SELECT * FROM service_providers
                    ORDER BY price ASC
                ''')
            rows = cursor.fetchall()
            self.print_results(rows, text_widget)
        except sqlite3.Error as e:
            print(f"Error during search by price: {e}")

    def search_by_distance(self, text_widget):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                    SELECT * FROM service_providers
                    ORDER BY distance ASC
                ''')
            rows = cursor.fetchall()
            self.print_results(rows, text_widget)
        except sqlite3.Error as e:
            print(f"Error during search by distance: {e}")

    def print_results(self, rows, text_widget):
        if not rows:
            text_widget.insert(tk.END, "No results found.\n")
        else:
            for row in rows:
                text_widget.insert(tk.END, str(row) + "\n")

    def search_by_name(self, name, text_widget):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM service_providers
                WHERE name LIKE ?
                ORDER BY rating DESC
            ''', ('%' + name + '%',))
            rows = cursor.fetchall()
            self.print_results(rows, text_widget)
        except sqlite3.Error as e:
            print(f"Error during search by name: {e}")

    # Modify the other search methods in a similar way...

def search(db, text_widget):
    search_criteria = criteria_var.get().lower()
    search_term = term_var.get()

    if not search_term:
        messagebox.showerror("Error", "Please enter a search term.")
        return

    text_widget.delete(1.0, tk.END)

    if search_criteria == "name":
        db.search_by_name(search_term, text_widget)
    elif search_criteria == "sector":
        db.search_by_sector(search_term, text_widget)
    elif search_criteria == "rating":
        db.search_by_rating(text_widget)
    elif search_criteria == "price":
        db.search_by_price(text_widget)
    elif search_criteria == "distance":
        db.search_by_distance(text_widget)
    else:
        messagebox.showerror("Error", "Invalid search criteria. Please enter 'name', 'sector', 'rating', 'price', or 'distance'.")

if __name__ == "__main__":
    try:
        db = ServiceProviderDatabase('database.db')
        db.connect()

        root = tk.Tk()
        criteria_var = tk.StringVar()
        term_var = tk.StringVar()

        tk.Label(root, text="Enter search criteria (name, sector, rating, price, distance): ").pack()
        tk.OptionMenu(root, criteria_var, "name", "sector", "rating", "price", "distance").pack()

        tk.Label(root, text="Enter the search term: ").pack()
        tk.Entry(root, textvariable=term_var).pack()

        results_text = tk.Text(root)
        results_text.pack()

        tk.Button(root, text="Search", command=lambda: search(db, results_text)).pack()

        root.mainloop()
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        if db:
            db.close()
