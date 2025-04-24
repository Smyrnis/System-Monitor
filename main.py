import customtkinter as ctk
from stats import cpu_stats, memory_stats, disk_stats, power_stats
from stats import process_stats
import psutil  # Added psutil import to check for battery



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TaskManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("system")

        self.title("System Monitor")
        self.geometry("800x650")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create the tabview and add initial tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.cpu_tab = self.tabview.add("CPU")
        self.memory_tab = self.tabview.add("Memory")
        self.disk_tab = self.tabview.add("Disk")
        self.process_tab = self.tabview.add("Processes")

        # Check if battery is available before adding the power tab
        if psutil.sensors_battery() is not None:
            self.power_tab = self.tabview.add("Power")
        else:
            self.power_tab = None  # Don't add the Power tab if no battery is found

        # Store after() IDs for cleanup
        self.after_ids = []

        self.build_ui()

        # Force the layout to update and redraw
        self.update_idletasks()  # Ensure all widgets are rendered
        self.geometry(self.geometry())  # Programmatically resize the window to fix layout issues

    def build_ui(self):
        # Add frames for better organization
        cpu_frame = ctk.CTkFrame(self.cpu_tab, corner_radius=10)
        cpu_frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(cpu_frame, text="CPU Usage", font=("Arial", 20, "bold")).pack(pady=10)

        memory_frame = ctk.CTkFrame(self.memory_tab, corner_radius=10)
        memory_frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(memory_frame, text="Memory Usage", font=("Arial", 20, "bold")).pack(pady=10)

        disk_frame = ctk.CTkFrame(self.disk_tab, corner_radius=10)
        disk_frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(disk_frame, text="Disk Usage", font=("Arial", 20, "bold")).pack(pady=10)

        process_frame = ctk.CTkFrame(self.process_tab, corner_radius=10)
        process_frame.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(process_frame, text="Running Processes", font=("Arial", 20, "bold")).pack(pady=10)

        # Build the tabs and store after() IDs
        self.after_ids.append(cpu_stats.build_cpu_tab(cpu_frame))
        self.after_ids.append(memory_stats.build_memory_tab(memory_frame))
        self.after_ids.append(disk_stats.build_disk_tab(disk_frame))
        self.after_ids.append(process_stats.build_processes_tab(process_frame))

        if self.power_tab is not None:
            power_frame = ctk.CTkFrame(self.power_tab, corner_radius=10)
            power_frame.pack(fill="both", expand=True, padx=10, pady=10)
            ctk.CTkLabel(power_frame, text="Power Information", font=("Arial", 20, "bold")).pack(pady=10)
            self.after_ids.append(power_stats.build_power_tab(power_frame))


    def start_update_loop(self):
        def update():
            if not self.winfo_exists():
                return
            print("Updating...")

            aid = self.after(1000, update)
            self.after_ids.append(aid)

        aid = self.after(1000, update)
        self.after_ids.append(aid)


    def on_closing(self):
        # Cancel all scheduled after() callbacks
        try:
            for aid in getattr(self, 'after_ids', []):
                    try:
                        self.after_cancel(aid)
                    except:
                        pass
            self.quit()  # Close the application
            self.grid_forget()  # Destroy the main window
        except:
            pass

if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()
