import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Database connection
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="", 
            database="screen_time_db" 
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {err}")
        return None

# Load data from MySQL
def load_data():
    global df
    try:
        conn = connect_to_db()
        if conn:
            query = "SELECT * FROM screen_time"
            df = pd.read_sql(query, conn)
            df.set_index("date", inplace=True)
            df.index = pd.to_datetime(df.index)
            conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {str(e)}")

# Add new data to MySQL
def add_data():
    date = askstring("Input", "Enter Date (YYYY-MM-DD):")
    total_duration = askstring("Input", "Enter Total Duration (mins):")
    social_media = askstring("Input", "Enter Social Media (mins):")
    others = askstring("Input", "Enter Others (mins):")
    productivity = askstring("Input", "Enter Productivity (mins):")

    try:
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            query = f"""
                INSERT INTO screen_time (date, total_duration, social_media, others, productivity)
                VALUES ('{date}', {total_duration}, {social_media}, {others}, {productivity})
                ON DUPLICATE KEY UPDATE
                total_duration = {total_duration},
                social_media = {social_media},
                others = {others},
                productivity = {productivity}
            """
            cursor.execute(query)  # No parameters passed here
            conn.commit()
            conn.close()
            load_data()
            messagebox.showinfo("Success", "Data added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add data: {str(e)}")

# Plot Line Graph
def plot_line_graph():
    fig, ax = plt.subplots()
    data = filtered_df if not filtered_df.empty else df
    if data.empty:
        messagebox.showwarning("Warning", "No data available to plot.")
        return
    ax.plot(data.index, data['social_media'], label='Social Media (mins)')
    ax.plot(data.index, data['others'], label='Others (mins)')
    ax.plot(data.index, data['productivity'], label='Productivity (mins)')
    ax.set_title("Line Graph")
    ax.legend()
    show_plot(fig)

# Plot Bar Graph
def plot_bar_graph():
    fig, ax = plt.subplots()
    data = filtered_df if not filtered_df.empty else df
    if data.empty:
        messagebox.showwarning("Warning", "No data available to plot.")
        return
    ax.bar(data.index, data['social_media'], label='Social Media (mins)', color='skyblue')
    ax.bar(data.index, data['others'], label='Others (mins)', bottom=data['social_media'], color='orange')
    ax.bar(data.index, data['productivity'], label='Productivity (mins)', bottom=data['social_media'] + data['others'], color='green')
    ax.set_title("Bar Graph")
    ax.legend()
    show_plot(fig)

# Plot Pie Chart
def plot_pie_chart():
    fig, ax = plt.subplots()
    data = filtered_df if not filtered_df.empty else df
    if data.empty:
        messagebox.showwarning("Warning", "No data available to plot.")
        return
    latest_data = data.iloc[-1]
    labels = ['Social Media (mins)', 'Others (mins)', 'Productivity (mins)']
    values = [latest_data['social_media'], latest_data['others'], latest_data['productivity']]
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    ax.set_title("Pie Chart of Latest Data")
    show_plot(fig)

# Show the Matplotlib plot in Tkinter
def show_plot(fig):
    for widget in plot_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Filter data by date
def filter_data():
    global filtered_df
    start_date = pd.to_datetime(start_date_entry.get())
    end_date = pd.to_datetime(end_date_entry.get())
    filtered_df = df[(df.index >= start_date) & (df.index <= end_date)]
    update_table(filtered_df)

# Update the table with filtered data
def update_table(data):
    for row in tree.get_children():
        tree.delete(row)
    if data.empty:
        return
    for index, row in data.iterrows():
        tree.insert("", tk.END, values=[index.date(), row['total_duration'], row['social_media'],
                                         row['others'], row['productivity']])

# Main Application Window
root = tk.Tk()
root.title("Screen Time Dashboard")
root.geometry("1200x800")
root.configure(bg="#f0f0f0")

# Load initial data
load_data()

# Date Filter Frame
filter_frame = tk.Frame(root, bg="#f0f0f0")
filter_frame.pack(pady=10)

start_date_label = tk.Label(filter_frame, text="Start Date:", bg="#f0f0f0")
start_date_label.pack(side=tk.LEFT, padx=5)
start_date_entry = DateEntry(filter_frame)
start_date_entry.pack(side=tk.LEFT, padx=5)

end_date_label = tk.Label(filter_frame, text="End Date:", bg="#f0f0f0")
end_date_label.pack(side=tk.LEFT, padx=5)
end_date_entry = DateEntry(filter_frame)
end_date_entry.pack(side=tk.LEFT, padx=5)

filter_button = tk.Button(filter_frame, text="Filter", command=filter_data, bg="#4caf50", fg="white")
filter_button.pack(side=tk.LEFT, padx=5)

# Table Frame
table_frame = tk.Frame(root)
table_frame.pack(pady=10)

columns = ['Date', 'Total Duration', 'Social Media', 'Others', 'Productivity']
tree = ttk.Treeview(table_frame, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180)
tree.pack()

update_table(df)

# Plot Frame
plot_frame = tk.Frame(root)
plot_frame.pack(pady=10)

# Graph Buttons Frame
graph_frame = tk.Frame(root, bg="#f0f0f0")
graph_frame.pack(pady=10)

line_button = tk.Button(graph_frame, text="Line Graph", command=plot_line_graph, bg="#2196f3", fg="white")
line_button.pack(side=tk.LEFT, padx=5)

bar_button = tk.Button(graph_frame, text="Bar Graph", command=plot_bar_graph, bg="#ff9800", fg="white")
bar_button.pack(side=tk.LEFT, padx=5)

pie_button = tk.Button(graph_frame, text="Pie Chart", command=plot_pie_chart, bg="#9c27b0", fg="white")
pie_button.pack(side=tk.LEFT, padx=5)

# Add Data Button
add_data_button = tk.Button(root, text="Add Data", command=add_data, bg="#f44336", fg="white")
add_data_button.pack(pady=10)

# Handle closing the application
def on_closing():
    root.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

