
import customtkinter as ctk


class ChatPanel(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            fg_color="#122238",
            corner_radius=15
        )

        self.title = ctk.CTkLabel(
            self,
            text="CONVERSATION",
            font=("Segoe UI", 16, "bold")
        )

        self.title.pack(anchor="w", padx=15, pady=10)

        self.messages = ctk.CTkTextbox(
            self,
            height=220,
            wrap="word",
            font=("Segoe UI", 13)
        )

        self.messages.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=12
        )

        self.add_message(
            "JARVIS",
            "Hello! How can I assist you?"
        )

    def add_message(self, sender, message):

        self.messages.configure(state="normal")

        self.messages.insert(
            "end",
            f"\n{sender}: {message}\n"
        )

        self.messages.see("end")

        self.messages.configure(state="disabled")
