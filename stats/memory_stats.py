import psutil
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import numpy as np

memory_history = deque([0] * 60, maxlen=60)  # Store memory usage history
x_vals = list(range(60))  # X-axis values (0 to 59)

def build_memory_tab(frame):
    # Create the figure and axes
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor("#2b2b2b")  # Set figure background to match system theme
    ax.set_facecolor("#2b2b2b")  # Set axes background to match system theme

    # Configure the graph
    ax.set_ylim(0, 100)
    ax.set_xlim(0, 59)
    ax.set_title("Memory Usage", fontsize=12, color="white")
    ax.set_xlabel("Time", fontsize=10, color="white")
    ax.set_ylabel("Usage (%)", fontsize=10, color="white")
    ax.grid(True, linestyle="--", linewidth=0.3, color="gray")
    ax.tick_params(colors="white")

    # Create the line plot
    line, = ax.plot(x_vals, list(memory_history), color="tab:blue", linewidth=1)

    # Embed the graph in the Tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Add a label below the graph for memory usage details
    memory_label = ctk.CTkLabel(frame, text="", font=("Arial", 14))
    memory_label.pack(pady=10)

    # Update function to refresh the graph and label
    def update():
        memory = psutil.virtual_memory()
        memory_history.append(memory.percent)  # Add the latest memory usage to the history
        line.set_ydata(memory_history)  # Update the line's Y-axis data

        # Update the memory label with percentage and used/total memory
        used_memory = memory.used / (1024 * 1024 * 1024)  # Convert to GB
        total_memory = memory.total / (1024 * 1024 * 1024)  # Convert to GB
        memory_label.configure(
            text=f"Memory Usage: {memory.percent:.1f}% ({used_memory:.2f} GB / {total_memory:.2f} GB)"
        )

        canvas.draw()  # Redraw the canvas
        return frame.after(1000, update)  # Schedule the next update
       
    return update()  # Start the update loop
