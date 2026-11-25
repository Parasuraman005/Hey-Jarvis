
import psutil
import customtkinter as ctk


class SystemMonitor(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            fg_color="#122238",
            corner_radius=12
        )

        self.cpu_label = ctk.CTkLabel(
            self,
            text="CPU: --%"
        )

        self.ram_label = ctk.CTkLabel(
            self,
            text="RAM: --%"
        )

        self.battery_label = ctk.CTkLabel(
            self,
            text="BATTERY: --"
        )

        for widget in (
            self.cpu_label,
            self.ram_label,
            self.battery_label
        ):
            widget.pack(anchor="w", padx=15, pady=8)

        self.update_stats()

    def update_stats(self):

        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()

        self.cpu_label.configure(
            text=f"CPU: {cpu}%"
        )

        self.ram_label.configure(
            text=f"RAM: {ram}%"
        )

        battery_text = (
            f"{battery.percent}%"
            if battery else "Unavailable"
        )

        self.battery_label.configure(
            text=f"BATTERY: {battery_text}"
        )

        self.after(2000, self.update_stats)
