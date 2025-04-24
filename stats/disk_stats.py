import psutil
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import numpy as np
import re

x_vals = np.arange(60)

def build_disk_tab(frame):
    disks_frame = ctk.CTkScrollableFrame(frame)
    disks_frame.pack(fill="both", expand=True, padx=10, pady=10)

    disk_graphs = {}  # {disk_name: {'read_hist': ..., 'write_hist': ..., 'lines': ...}}

    fig_dict = {}  # Holds canvas widgets for drawing

    # Initial setup for each disk
    io_counters = psutil.disk_io_counters(perdisk=True)
    for disk_name in io_counters:
        if disk_name.startswith("loop") or disk_name.startswith("ram"):
            continue
        if re.match(r"(.*\d+)p\d+$", disk_name) or re.match(r"[a-z]+\d+$", disk_name):
            continue
        # Skip loop devices and RAM disks
        disk_box = ctk.CTkFrame(disks_frame)
        disk_box.pack(fill="x", pady=10)

        title = ctk.CTkLabel(disk_box, text=f"Device: {disk_name}", font=("Arial", 15, "bold"))
        title.pack(anchor="w", padx=10)

        read_hist = deque([0] * 60, maxlen=60)
        write_hist = deque([0] * 60, maxlen=60)

        fig, ax = plt.subplots(figsize=(6, 2.2))
        fig.patch.set_facecolor("#2b2b2b")  # Set figure background to match system theme
        ax.set_facecolor("#2b2b2b")  # Set axes background to match system theme
        ax.set_ylim(0, 1024**2 * 100)  # ~100MB/s
        ax.set_xlim(0, 59)
        ax.set_ylabel("Bytes/s", fontsize=9, color="white")
        ax.grid(True, linestyle="--", linewidth=0.3, color="gray")
        ax.tick_params(axis='both', labelsize=8, colors="white")

        line_r, = ax.plot(x_vals, read_hist, label="Read", color="tab:blue")
        line_w, = ax.plot(x_vals, write_hist, label="Write", color="tab:orange")
        ax.legend(loc="upper right", fontsize=8, facecolor="#2b2b2b", edgecolor="gray", labelcolor="white")

        canvas = FigureCanvasTkAgg(fig, master=disk_box)
        canvas.get_tk_widget().pack(fill="x", padx=10)

        # Add a label below the graph for read/write speeds
        speed_label = ctk.CTkLabel(disk_box, text="Read Speed: 0 MB/s | Write Speed: 0 MB/s", font=("Arial", 12))
        speed_label.pack(pady=5)

        disk_graphs[disk_name] = {
            'read_hist': read_hist,
            'write_hist': write_hist,
            'line_r': line_r,
            'line_w': line_w,
            'canvas': canvas,
            'last': io_counters[disk_name],
            'speed_label': speed_label
        }

        def on_mouse_wheel(event, disks_frame):
            if event.delta:
                disks_frame.yview_scroll(-1 if event.delta > 0 else 1, "units")
            else:
                disks_frame.yview_scroll(-1 if event.num == 5 else 1, "units")
    disks_frame.bind("<MouseWheel>", lambda event, disks_frame=disks_frame: on_mouse_wheel(event, disks_frame))
    def update():
        current_counters = psutil.disk_io_counters(perdisk=True)
        for disk_name, stats in current_counters.items():
            if disk_name not in disk_graphs:
                continue  # Might have unplugged etc

            disk = disk_graphs[disk_name]
            last = disk['last']

            # Calculate deltas
            read_delta = stats.read_bytes - last.read_bytes
            write_delta = stats.write_bytes - last.write_bytes

            # Convert deltas to MB/s
            read_speed = read_delta / (1024 * 1024)  # Convert to MB
            write_speed = write_delta / (1024 * 1024)  # Convert to MB

            # Update histories
            disk['read_hist'].append(read_delta)
            disk['write_hist'].append(write_delta)

            # Update plots
            disk['line_r'].set_ydata(disk['read_hist'])
            disk['line_w'].set_ydata(disk['write_hist'])
            disk['canvas'].draw()

            # Update the speed label
            disk['speed_label'].configure(
                text=f"Read Speed: {read_speed:.2f} MB/s | Write Speed: {write_speed:.2f} MB/s"
            )

            # Store current for next delta calc
            disk['last'] = stats

        return frame.after(1000, update)
        

    return update()