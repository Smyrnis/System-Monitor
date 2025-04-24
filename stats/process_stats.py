import psutil
import customtkinter as ctk
from tkinter import ttk

def build_processes_tab(frame):
    # Determine system appearance mode and set a matching background color
    appearance_mode = ctk.get_appearance_mode()  # returns "Light" or "Dark"
    system_bg_color = "#F0F0F0" if appearance_mode == "Light" else "#2B2B2B"
    text_color = "black" if appearance_mode == "Light" else "white"

    # Set the frame background (customtkinter uses fg_color)
    frame.configure(fg_color=system_bg_color)

    # Configure Treeview style to match the theme
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background=system_bg_color,
                    fieldbackground=system_bg_color,
                    foreground=text_color)  # 👈 Changed to white in dark mode

    # Define columns
    columns = ("PID", "Name", "CPU %", "Memory %")
    tree = ttk.Treeview(frame, columns=columns, show='headings')

    # Create headings
    for col in columns:
        tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
        tree.column(col, anchor="center", stretch=True)
    tree.pack(fill='both', expand=True, padx=10, pady=10)

    # Update process list
    def update():
        for row in tree.get_children():
            tree.delete(row)
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                tree.insert("", "end", values=(
                    proc.info['pid'],
                    proc.info['name'],
                    f"{proc.info['cpu_percent']:.1f}",
                    f"{proc.info['memory_percent']:.1f}"
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        frame.after(2000, update)  # Refresh every 2s

    # Sort columns
    def sort_column(tv, col, reverse):
        data = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            data.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            data.sort(key=lambda t: t[0], reverse=reverse)
        for index, (val, k) in enumerate(data):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: sort_column(tv, col, not reverse))

    update()
