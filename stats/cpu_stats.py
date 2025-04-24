import psutil
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import numpy as np
import math

core_count = psutil.cpu_count(logical=True)
core_histories = [deque([0] * 60, maxlen=60) for _ in range(core_count)]
x_vals = np.arange(60)

def build_cpu_tab(frame):
    cols = min(4, core_count)
    rows = math.ceil(core_count / cols)

    fig, axs = plt.subplots(rows, cols, figsize=(3 * cols, 1.8 * rows), squeeze=False)
    fig.patch.set_facecolor("#2b2b2b")  # Dark background for the figure
    for ax in axs.flat:
        ax.set_facecolor("#2b2b2b")

    lines = []
    usage_texts = []

    for idx in range(rows * cols):
        row = idx // cols
        col = idx % cols
        ax = axs[row][col]

        if idx < core_count:
            ax.set_ylim(0, 100)
            ax.set_xlim(0, 59)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(True, linestyle="--", linewidth=0.3, color="gray")
            ax.set_title(f"Core {idx}", fontsize=8, color="white")
            line, = ax.plot(x_vals, list(core_histories[idx]), color="tab:blue", linewidth=1)
            lines.append(line)

            # Add usage text below graph
            usage_text = ax.text(
                30, -15,  # x=middle, y=just below the graph
                "Usage: 0%", 
                fontsize=10, 
                color="white", 
                ha="center"
            )
            usage_texts.append(usage_text)
        else:
            ax.axis("off")

    fig.tight_layout(pad=1.0)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def update():
        usage = psutil.cpu_percent(percpu=True)
        for i, val in enumerate(usage):
            core_histories[i].append(val)
            lines[i].set_ydata(core_histories[i])
            usage_texts[i].set_text(f"Usage: {val:.1f}%")
        canvas.draw()
        return frame.after(1000, update)

    return update()
