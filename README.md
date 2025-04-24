# System-Monitor

A system monitoring application build using CustomTkinter.This app provides real-time insights into your CPU, memory, disk, processes, and battery (if available)


Features

.CPU tab: View real-time CPU usage and stats.
.Memory Tab: Monitor RAM usage and memory performance.
.Disk Tab: Check storage space and disk I/O.
.Power Tab: Battery health and charge status (only shown on laptops or devices with a battery).
.Processes Tab: Lists currently running processes.

Requirements
.Python 3.7 +
.custometkinter
.psutil
.matplotlib

INSTALL DEPENDENCIES
    pip install customtkinter psutil matplotlib

File Structure

├── main.py                
├── stats/
│   ├── cpu_stats.py       # CPU tab logic
│   ├── memory_stats.py    # Memory tab logic
│   ├── disk_stats.py      # Disk tab logic
│   ├── power_stats.py     # Power tab logic
│   └── process_stats.py   # Processes tab logic


Running the App
    python main.py



Notes::
        The power tab is conditionally rendered only if a battery is detected using
                                        psutil.sensors_battery()


AUTHOR

Giannis Smyrnis
