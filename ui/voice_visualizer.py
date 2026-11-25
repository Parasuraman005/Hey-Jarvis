
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

        self.state_label.pack(
            pady=(10, 0)
        )

        self.circle = ctk.CTkLabel(
            self,
            text="◉",
            font=("Segoe UI", 100),
            text_color="#0EA5E9"
        )

        self.circle.pack(
            pady=10
        )

        self.set_state("standby")

    def set_state(self, state):

        states = {
            "initializing": (
                "INITIALIZING",
                "#F59E0B",
                "◈"
            ),
            "standby": (
                "STANDBY",
                "#64748B",
                "◉"
            ),
            "waiting": (
                "WAITING FOR WAKE WORD",
                "#0EA5E9",
                "◉"
            ),
            "listening": (
                "LISTENING",
                "#22C55E",
                "◎"
            ),
            "thinking": (
                "THINKING",
                "#F59E0B",
                "◈"
            ),
            "speaking": (
                "SPEAKING",
                "#0EA5E9",
                "◉"
            ),
            "stopping": (
                "STOPPING",
                "#F59E0B",
                "◈"
            ),
            "stopped": (
                "STOPPED",
                "#64748B",
                "○"
            ),
            "error": (
                "ERROR",
                "#EF4444",
                "×"
            )
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
