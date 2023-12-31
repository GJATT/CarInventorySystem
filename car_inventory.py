import tkinter as tk
import mysql.connector
from tkinter import ttk

# Establish connection to MySQL

mydb = mysql.connector.connect(
    host = localhost,
    user = root,
    password = Therock1998,
    database = UsedCarBusiness
)
my_cursor = mydb.cursor()

# Creating the main application window

root = tk.Tk()
root.title("Car Inventory Management System")

# Function to fetch and display data

def fetch_data():
    # Clear previous data
    for row in tree.get_children():
        tree.delete(row)

    # Fetch data from car table
    mycursor.execute("SELECT * FROM car")
    car = mycursor.fetchall()
    for c in car:
        tree.insert("", "end", values=c)

    # Fetch data from customer table
    mycursor.execute("SELECT * FROM customer ")
    customer = mycursor.fetchall()
    for c in customer:
        tree.insert("", "end", values=c)
        
# Create a treeview to display data

columns = ['License Plate Number', 'Model Year', 'Model', 'Type', 'Condition']
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.pack()

# Button to fetch and display data
fetch_button = tk.Button(root, text='Fetch Data', command=fetch_data)
fetch_button.pack()


# Run the GUI
root.mainloop()
