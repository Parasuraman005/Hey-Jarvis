
import customtkinter as ctk


class VoiceVisualizer(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            fg_color="transparent"
        )

        self.state_label = ctk.CTkLabel(
            self,
            text="STANDBY",
            font=("Segoe UI", 18, "bold")
        )

        self.state_label.pack(pady=10)

        self.circle = ctk.CTkLabel(
            self,
            text="◉",
            font=("Segoe UI", 100),
            text_color="#0EA5E9"
        )

        self.circle.pack()

    def set_state(self, state):

        states = {
            "standby": ("STANDBY", "#64748B", "◉"),
            "listening": ("LISTENING", "#22C55E", "◎"),
            "thinking": ("THINKING", "#F59E0B", "◈"),
            "speaking": ("SPEAKING", "#0EA5E9", "◉"),
            "error": ("ERROR", "#EF4444", "×"),
        }

        label, color, symbol = states.get(
            state,
            states["standby"]
        )

        self.state_label.configure(
            text=label,
            text_color=color
        )

        self.circle.configure(
            text=symbol,
            text_color=color
        )
