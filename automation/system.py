
import psutil
import platform
import os
import subprocess


class SystemController:

    def get_system_info(self):

        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(os.environ.get("SystemDrive", "C:") + "\\")

        cpu = psutil.cpu_percent(interval=1)

        return {
            "os": platform.system(),
            "computer": platform.node(),
            "processor": platform.processor(),
            "cpu_usage": f"{cpu}%",
            "total_ram": f"{memory.total / (1024**3):.2f} GB",
            "used_ram": f"{memory.used / (1024**3):.2f} GB",
            "available_ram": f"{memory.available / (1024**3):.2f} GB",
            "ram_usage": f"{memory.percent}%",
            "disk_usage": f"{disk.percent}%",
        }

    def get_battery(self):

        battery = psutil.sensors_battery()

        if battery is None:
            return "Battery information is unavailable."

        return (
            f"Battery level is {battery.percent} percent."
        )

    def lock_pc(self):

        try:
            subprocess.Popen(["rundll32.exe", "user32.dll,LockWorkStation"])
            return "Locking your computer."

        except Exception as error:
            return f"Unable to lock computer: {error}"
