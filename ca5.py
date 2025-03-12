import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Destination prices
destination_prices = {
    "Paris": 200,
    "New York": 300,
    "Tokyo": 250,
    "London": 220,
    "Sydney": 270
}

# Database Connection
def connect_db():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="root")
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS travel_db")
        cursor.execute("USE travel_db")
        cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                            id INT AUTO_INCREMENT PRIMARY KEY, 
                            name VARCHAR(255), 
                            contact VARCHAR(255), 
                            email VARCHAR(255), 
                            age INT, 
                            destination VARCHAR(255), 
                            date VARCHAR(255), 
                            tickets INT, 
                            total_cost FLOAT)''')
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Save Booking to Database
def save_to_db(name, contact, email, age, destination, date, tickets, total_cost):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO bookings (name, contact, email, age, destination, date, tickets, total_cost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (name, contact, email, age, destination, date, tickets, total_cost))
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            conn.close()

# Update Total Cost Calculation
def calculate_total(*args):
    try:
        num_tickets = int(tickets_var.get())
        destination = destination_var.get()
        ticket_price = destination_prices.get(destination, 0)
        total_cost = num_tickets * ticket_price
        total_label.config(text=f"Cost per Ticket: ${ticket_price}\nTotal Cost: ${total_cost:.2f}")
        total_var.set(str(total_cost))  # Store total cost
    except ValueError:
        total_label.config(text="Total Cost: $0.00")

# Submit Booking
def submit_details():
    name, contact, email, age = name_var.get(), contact_var.get(), email_var.get(), age_var.get()
    destination, date, tickets, total_cost = destination_var.get(), date_var.get(), tickets_var.get(), total_var.get()
    
    if not all([name, contact, email, age, destination, date, tickets]):
        messagebox.showerror("Error", "Please fill in all fields")
        return

    details_table.insert("", tk.END, values=(name, contact, email, age, destination, date, tickets, f"${float(total_cost):.2f}"))
    save_to_db(name, contact, email, age, destination, date, tickets, float(total_cost))
    messagebox.showinfo("Success", "Booking Successful!")
    reset_fields()

# Reset Fields
def reset_fields():
    name_var.set("")
    contact_var.set("")
    email_var.set("")
    age_var.set("")
    destination_var.set("")
    date_var.set("")
    tickets_var.set("1")
    total_var.set("0")
    total_label.config(text="Total Cost: $0.00")

# UI Setup
root = tk.Tk()
root.title("Travel Booking System")
root.geometry("550x500")
root.configure(bg="#87CEEB")

# Variables
name_var, contact_var, email_var, age_var = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
destination_var, date_var, tickets_var, total_var = tk.StringVar(), tk.StringVar(), tk.StringVar(value="1"), tk.StringVar(value="0")
tickets_var.trace("w", calculate_total)
destination_var.trace("w", calculate_total)

def next_page(current, next_frame):
    current.pack_forget()
    next_frame.pack(pady=20)

# First Page (User Details)
page1 = tk.Frame(root, bg="#87CEEB")
tk.Label(page1, text="Enter Your Details", bg="#87CEEB", font=("Arial", 14, "bold")).pack()
tk.Label(page1, text="Name:", bg="#87CEEB").pack()
tk.Entry(page1, textvariable=name_var).pack(pady=5)
tk.Label(page1, text="Contact:", bg="#87CEEB").pack()
tk.Entry(page1, textvariable=contact_var).pack(pady=5)
tk.Label(page1, text="Email:", bg="#87CEEB").pack()
tk.Entry(page1, textvariable=email_var).pack(pady=5)
tk.Label(page1, text="Age:", bg="#87CEEB").pack()
tk.Entry(page1, textvariable=age_var).pack(pady=5)
tk.Button(page1, text="Next", command=lambda: next_page(page1, page2), bg="#4682B4", fg="white").pack(pady=10)
page1.pack(pady=20)

# Second Page (Destination Selection)
page2 = tk.Frame(root, bg="#87CEEB")
tk.Label(page2, text="Select Destination:", bg="#87CEEB").pack()
ttk.Combobox(page2, textvariable=destination_var, values=list(destination_prices.keys())).pack(pady=5)
tk.Button(page2, text="Next", command=lambda: next_page(page2, page3), bg="#4682B4", fg="white").pack(pady=10)
tk.Button(page2, text="Back", command=lambda: next_page(page2, page1), bg="#4682B4", fg="white").pack()

# Third Page (Date & Tickets)
page3 = tk.Frame(root, bg="#87CEEB")
tk.Label(page3, text="Enter Travel Date:", bg="#87CEEB").pack()
tk.Entry(page3, textvariable=date_var).pack(pady=5)
tk.Label(page3, text="Number of Tickets:", bg="#87CEEB").pack()
tk.Entry(page3, textvariable=tickets_var).pack(pady=5)
tk.Button(page3, text="Next", command=lambda: next_page(page3, page4), bg="#4682B4", fg="white").pack(pady=10)
tk.Button(page3, text="Back", command=lambda: next_page(page3, page2), bg="#4682B4", fg="white").pack()

# Fourth Page (Cost Calculation)
page4 = tk.Frame(root, bg="#87CEEB")
total_label = tk.Label(page4, text="Total Cost: $0.00", bg="#87CEEB")
total_label.pack()
tk.Button(page4, text="Next", command=lambda: next_page(page4, last_page), bg="#4682B4", fg="white").pack(pady=10)
tk.Button(page4, text="Back", command=lambda: next_page(page4, page3), bg="#4682B4", fg="white").pack()

# Last Page with Details and Submit Button
last_page = tk.Frame(root, bg="#87CEEB")
details_table = ttk.Treeview(last_page, columns=("Name", "Contact", "Email", "Age", "Destination", "Date", "Tickets", "Total Cost"), show="headings")
details_table.pack()
tk.Button(last_page, text="Submit", command=submit_details, bg="#4682B4", fg="white").pack(pady=10)

root.mainloop()
