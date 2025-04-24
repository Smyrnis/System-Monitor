
import customtkinter as ctk
import psutil
import threading
import time

BAT_PATH = "/sys/class/power_supply/BAT0"

def read_sys_file(path):
    try:
        with open(path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "N/A"
    
def build_power_tab(parent_frame, capacity_wh=50):
    # Main container frame
    frame = ctk.CTkFrame(parent_frame)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    battery_label = ctk.CTkLabel(frame, text="Battery: --%", font=("Arial", 18))
    battery_label.pack(pady=5)

    status_label = ctk.CTkLabel(frame, text="Status: --", font=("Arial", 16))
    status_label.pack(pady=5)

    watts_label = ctk.CTkLabel(frame, text="Power: -- W", font=("Arial", 16))
    watts_label.pack(pady=5)

    time_left_label = ctk.CTkLabel(frame, text="Time Remaining: --", font=("Arial", 16))
    time_left_label.pack(pady=5)

    def format_time(secs):
        if secs == psutil.POWER_TIME_UNLIMITED:
            return "Calculating..."
        elif secs == psutil.POWER_TIME_UNKNOWN or secs < 0:
            return "Unknown"
        else:
            hours = secs // 3600
            minutes = (secs % 3600) // 60
            return f"{int(hours)}h {int(minutes)}m"

    def update_loop():
        while True:
            battery = psutil.sensors_battery()
            percent = battery.percent
            charging = battery.power_plugged
            secs_left = battery.secsleft

            # Estimate power
            power = 0
            if secs_left > 0:
                if charging:
                    power = (100 - percent) / 100 * capacity_wh / (secs_left / 3600)
                else:
                    power = percent / 100 * capacity_wh / (secs_left / 3600)

            battery_label.configure(text=f"Battery: {percent:.1f}%")
            status_label.configure(text=f"Status: {'Charging' if charging else 'Discharging'}")
            watts_label.configure(text=f"Power: {power:.2f} W" if power > 0 else "Power: -- W")
            time_left_label.configure(text=f"Time Remaining: {format_time(secs_left)}")

            time.sleep(2)

    # Start background thread
    threading.Thread(target=update_loop, daemon=True).start()

    return None
