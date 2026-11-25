
import customtkinter as ctk
import queue

from ui.theme import THEME, FONT
from ui.chat_panel import ChatPanel
from ui.system_monitor import SystemMonitor
from ui.voice_visualizer import VoiceVisualizer
from ui.assistant_bridge import AssistantBridge


class JarvisDashboard(ctk.CTk):

    def __init__(self, assistant_runner=None):

        super().__init__()

        # =====================================
        # WINDOW CONFIGURATION
        # =====================================

        self.title("J.A.R.V.I.S - AI Assistant")
        self.geometry("1200x750")
        self.minsize(950, 600)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.configure(
            fg_color=THEME["background"]
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

        # =====================================
        # APPLICATION STATE
        # =====================================

        self.is_running = False
        self.is_muted = False
        self.closing = False

        self.bridge = None

        # =====================================
        # CREATE INTERFACE
        # =====================================

        self.create_header()
        self.create_dashboard()

        # =====================================
        # ASSISTANT BRIDGE
        # =====================================

        if assistant_runner is not None:

            self.bridge = AssistantBridge(
                assistant_runner
            )

        # =====================================
        # EVENT PROCESSING
        # =====================================

        self.process_events()

    # =========================================
    # HEADER
    # =========================================

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color=THEME["sidebar"],
            corner_radius=0,
            height=75
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        # Application name

        ctk.CTkLabel(
            header,
            text="◈  J.A.R.V.I.S",
            font=("Segoe UI", 24, "bold"),
            text_color=THEME["primary"]
        ).pack(
            side="left",
            padx=25
        )

        # System status

        self.system_status = ctk.CTkLabel(
            header,
            text="● SYSTEM READY",
            font=FONT["body"],
            text_color=THEME["success"]
        )

        self.system_status.pack(
            side="right",
            padx=25
        )

    # =========================================
    # MAIN DASHBOARD
    # =========================================

    def create_dashboard(self):

        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.content.grid_columnconfigure(
            0,
            weight=2
        )

        self.content.grid_columnconfigure(
            1,
            weight=1
        )

        self.content.grid_rowconfigure(
            0,
            weight=1
        )

        # =====================================
        # LEFT PANEL
        # =====================================

        left_panel = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        left_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        # Voice visualizer

        self.visualizer = VoiceVisualizer(
            left_panel
        )

        self.visualizer.pack(
            fill="x",
            pady=15
        )

        # Voice status

        self.voice_status = ctk.CTkLabel(
            left_panel,
            text="AWAITING YOUR COMMAND",
            font=("Segoe UI", 17, "bold"),
            text_color=THEME["secondary"]
        )

        self.voice_status.pack(
            pady=10
        )

        # Assistant response

        self.response_label = ctk.CTkLabel(
            left_panel,
            text="Hello! I am JARVIS. How can I help you?",
            font=FONT["body"],
            text_color=THEME["text"],
            wraplength=650
        )

        self.response_label.pack(
            pady=15
        )

        # =====================================
        # CONTROL BUTTONS
        # =====================================

        controls = ctk.CTkFrame(
            left_panel,
            fg_color="transparent"
        )

        controls.pack(pady=15)

        self.start_button = ctk.CTkButton(
            controls,
            text="START JARVIS",
            command=self.start_jarvis,
            width=150,
            height=42,
            fg_color=THEME["primary"]
        )

        self.start_button.grid(
            row=0,
            column=0,
            padx=6
        )

        self.stop_button = ctk.CTkButton(
            controls,
            text="STOP JARVIS",
            command=self.stop_jarvis,
            width=150,
            height=42,
            fg_color=THEME["danger"]
        )

        self.stop_button.grid(
            row=0,
            column=1,
            padx=6
        )

        self.mute_button = ctk.CTkButton(
            controls,
            text="MUTE",
            command=self.toggle_mute,
            width=100,
            height=42
        )

        self.mute_button.grid(
            row=0,
            column=2,
            padx=6
        )

        # =====================================
        # RIGHT PANEL
        # =====================================

        right_panel = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        right_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        # System monitor

        ctk.CTkLabel(
            right_panel,
            text="SYSTEM MONITOR",
            font=FONT["subheading"],
            text_color=THEME["text"]
        ).pack(
            anchor="w",
            pady=(5, 10)
        )

        self.monitor = SystemMonitor(
            right_panel
        )

        self.monitor.pack(
            fill="x",
            pady=5
        )

        # Conversation panel

        ctk.CTkLabel(
            right_panel,
            text="CONVERSATION",
            font=FONT["subheading"],
            text_color=THEME["text"]
        ).pack(
            anchor="w",
            pady=(20, 10)
        )

        self.chat = ChatPanel(
            right_panel
        )

        self.chat.pack(
            fill="both",
            expand=True
        )

    # =========================================
    # START JARVIS
    # =========================================

    def start_jarvis(self):

        if self.is_running:
            return

        if self.bridge is None:

            self.voice_status.configure(
                text="ASSISTANT RUNNER NOT CONNECTED",
                text_color=THEME["warning"]
            )

            return

        try:

            self.bridge.start()

            self.is_running = True

            self.start_button.configure(
                state="disabled"
            )

            self.voice_status.configure(
                text="INITIALIZING JARVIS...",
                text_color=THEME["secondary"]
            )

            self.system_status.configure(
                text="● STARTING",
                text_color=THEME["warning"]
            )

        except Exception as error:

            self.show_error(error)

    # =========================================
    # STOP JARVIS
    # =========================================

    def stop_jarvis(self):

        if self.bridge is not None:

            self.bridge.stop()

        self.is_running = False

        self.voice_status.configure(
            text="STOPPING JARVIS...",
            text_color=THEME["warning"]
        )

        self.stop_button.configure(
            state="disabled"
        )

    # =========================================
    # MUTE CONTROL
    # =========================================

    def toggle_mute(self):

        self.is_muted = not self.is_muted

        if self.is_muted:

            self.mute_button.configure(
                text="UNMUTE"
            )

        else:

            self.mute_button.configure(
                text="MUTE"
            )

        # Connect this state to your actual
        # TTS engine's mute control.

    # =========================================
    # EVENT PROCESSING
    # =========================================

    def process_events(self):

        if self.closing:
            return

        if self.bridge is not None:

            while True:

                try:

                    event = self.bridge.events.get_nowait()

                except queue.Empty:

                    break

                event_type = event.get("event")
                data = event.get("data")

                # STATUS EVENTS

                if event_type == "status":

                    state = str(data).lower()

                    self.voice_status.configure(
                        text=state.upper()
                    )

                    self.visualizer.set_state(
                        state
                    )

                    if state in ("standby", "stopped"):

                        self.system_status.configure(
                            text="● SYSTEM READY",
                            text_color=THEME["success"]
                        )

                    elif state == "error":

                        self.system_status.configure(
                            text="● SYSTEM ERROR",
                            text_color=THEME["danger"]
                        )

                # USER MESSAGE

                elif event_type == "user":

                    self.chat.add_message(
                        "YOU",
                        str(data)
                    )

                # JARVIS RESPONSE

                elif event_type == "response":

                    self.chat.add_message(
                        "JARVIS",
                        str(data)
                    )

                    self.response_label.configure(
                        text=str(data)
                    )

                # ERROR

                elif event_type == "error":

                    self.show_error(data)

                # RUNNER EXITED

                if not self.bridge.running:

                    self.is_running = False

                    self.start_button.configure(
                        state="normal"
                    )

                    self.stop_button.configure(
                        state="normal"
                    )

        self.after(
            100,
            self.process_events
        )

    # =========================================
    # ERROR HANDLER
    # =========================================

    def show_error(self, error):

        self.voice_status.configure(
            text="JARVIS ERROR",
            text_color=THEME["danger"]
        )

        self.visualizer.set_state("error")

        self.response_label.configure(
            text=str(error)
        )

        self.system_status.configure(
            text="● ERROR",
            text_color=THEME["danger"]
        )

    # =========================================
    # APPLICATION EXIT
    # =========================================

    def on_close(self):

        self.closing = True

        if self.bridge is not None:

            self.bridge.stop()

        self.destroy()


# =============================================
# APPLICATION ENTRY POINT
# =============================================

if __name__ == "__main__":

    app = JarvisDashboard()

    app.mainloop()
