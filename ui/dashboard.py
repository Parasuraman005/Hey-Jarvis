
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

        # ---------------------------------
        # WINDOW CONFIGURATION
        # ---------------------------------

        ctk.set_appearance_mode("dark")

        self.title("J.A.R.V.I.S - AI Assistant")
        self.geometry("1200x750")
        self.minsize(950, 600)

        self.configure(
            fg_color=THEME["background"]
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

        # ---------------------------------
        # APPLICATION STATE
        # ---------------------------------

        self.is_running = False
        self.is_muted = False
        self.closing = False

        self.bridge = None

        if assistant_runner is not None:
            self.bridge = AssistantBridge(
                assistant_runner
            )

        # ---------------------------------
        # BUILD USER INTERFACE
        # ---------------------------------

        self.create_header()
        self.create_main_layout()
        self.create_footer()

        # Start dashboard event processing
        self.after(100, self.process_events)

    # =====================================
    # HEADER
    # =====================================

    def create_header(self):

        self.header = ctk.CTkFrame(
            self,
            fg_color=THEME["sidebar"],
            corner_radius=12,
            height=85
        )

        self.header.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        self.header.pack_propagate(False)

        self.header.grid_columnconfigure(
            0,
            weight=1
        )

        # JARVIS title

        self.title_label = ctk.CTkLabel(
            self.header,
            text="J.A.R.V.I.S",
            font=FONT["heading"],
            text_color=THEME["primary"]
        )

        self.title_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(12, 0)
        )

        self.subtitle_label = ctk.CTkLabel(
            self.header,
            text="PERSONAL AI VOICE ASSISTANT",
            font=FONT["small"],
            text_color=THEME["muted"]
        )

        self.subtitle_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=22,
            pady=(0, 10)
        )

        # System status

        self.system_status = ctk.CTkLabel(
            self.header,
            text="SYSTEM READY",
            font=("Segoe UI", 12, "bold"),
            text_color=THEME["success"]
        )

        self.system_status.grid(
            row=0,
            column=1,
            rowspan=2,
            sticky="e",
            padx=25
        )

    # =====================================
    # MAIN DASHBOARD LAYOUT
    # =====================================

    def create_main_layout(self):

        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.main_frame.grid_columnconfigure(
            0,
            weight=3
        )

        self.main_frame.grid_columnconfigure(
            1,
            weight=2
        )

        self.main_frame.grid_rowconfigure(
            0,
            weight=1
        )

        # ---------------------------------
        # LEFT PANEL
        # ---------------------------------

        self.left_panel = ctk.CTkFrame(
            self.main_frame,
            fg_color=THEME["sidebar"],
            corner_radius=15
        )

        self.left_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        self.left_panel.grid_columnconfigure(
            0,
            weight=1
        )

        self.left_panel.grid_rowconfigure(
            1,
            weight=1
        )

        # Voice assistant heading

        self.voice_heading = ctk.CTkLabel(
            self.left_panel,
            text="VOICE ASSISTANT",
            font=FONT["subheading"],
            text_color=THEME["text"]
        )

        self.voice_heading.pack(
            pady=(20, 5)
        )

        # Voice visualizer

        self.visualizer = VoiceVisualizer(
            self.left_panel
        )

        self.visualizer.pack(
            fill="x",
            pady=10
        )

        # Voice status

        self.voice_status = ctk.CTkLabel(
            self.left_panel,
            text="Ready to start",
            font=FONT["body"],
            text_color=THEME["muted"]
        )

        self.voice_status.pack(
            pady=5
        )

        # Response display

        self.response_label = ctk.CTkLabel(
            self.left_panel,
            text="Hello! How can I assist you?",
            font=FONT["body"],
            text_color=THEME["text"],
            wraplength=500,
            justify="center"
        )

        self.response_label.pack(
            fill="x",
            padx=20,
            pady=15
        )

        # ---------------------------------
        # CONTROL BUTTONS
        # ---------------------------------

        self.button_frame = ctk.CTkFrame(
            self.left_panel,
            fg_color="transparent"
        )

        self.button_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.button_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        self.start_button = ctk.CTkButton(
            self.button_frame,
            text="START JARVIS",
            command=self.start_jarvis,
            fg_color=THEME["success"],
            hover_color="#16A34A",
            text_color="#FFFFFF",
            height=42,
            font=("Segoe UI", 12, "bold")
        )

        self.start_button.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5
        )

        self.stop_button = ctk.CTkButton(
            self.button_frame,
            text="STOP JARVIS",
            command=self.stop_jarvis,
            fg_color=THEME["danger"],
            hover_color="#DC2626",
            text_color="#FFFFFF",
            height=42,
            font=("Segoe UI", 12, "bold"),
            state="disabled"
        )

        self.stop_button.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5
        )

        self.mute_button = ctk.CTkButton(
            self.button_frame,
            text="MUTE",
            command=self.toggle_mute,
            fg_color=THEME["primary"],
            hover_color="#0284C7",
            text_color="#FFFFFF",
            height=42,
            font=("Segoe UI", 12, "bold"),
            state="disabled"
        )

        self.mute_button.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=5
        )

        # ---------------------------------
        # RIGHT PANEL
        # ---------------------------------

        self.right_panel = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.right_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        self.right_panel.grid_columnconfigure(
            0,
            weight=1
        )

        self.right_panel.grid_rowconfigure(
            1,
            weight=1
        )

        # System monitor

        self.monitor = SystemMonitor(
            self.right_panel
        )

        self.monitor.pack(
            fill="x",
            pady=(0, 12)
        )

        # Conversation panel

        self.chat = ChatPanel(
            self.right_panel
        )

        self.chat.pack(
            fill="both",
            expand=True
        )

    # =====================================
    # FOOTER
    # =====================================

    def create_footer(self):

        self.footer = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=35
        )

        self.footer.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        self.footer_label = ctk.CTkLabel(
            self.footer,
            text="J.A.R.V.I.S  |  OFFLINE AI ASSISTANT",
            font=FONT["small"],
            text_color=THEME["muted"]
        )

        self.footer_label.pack(
            side="left"
        )

        self.version_label = ctk.CTkLabel(
            self.footer,
            text="PHASE 7 DASHBOARD",
            font=FONT["small"],
            text_color=THEME["muted"]
        )

        self.version_label.pack(
            side="right"
        )

    # =====================================
    # START JARVIS
    # =====================================

    def start_jarvis(self):

        if self.closing:
            return

        if self.bridge is None:

            self.show_error(
                "Assistant runner is not connected. "
                "Launch using run_dashboard.py."
            )

            return

        if self.bridge.is_running():
            return

        try:

            self.bridge.start()

            self.is_running = True

            self.start_button.configure(
                state="disabled"
            )

            self.stop_button.configure(
                state="normal"
            )

            self.mute_button.configure(
                state="normal"
            )

            self.voice_status.configure(
                text="Starting JARVIS..."
            )

            self.system_status.configure(
                text="INITIALIZING",
                text_color=THEME["warning"]
            )

            self.visualizer.set_state(
                "initializing"
            )

        except Exception as error:

            self.show_error(str(error))

    # =====================================
    # STOP JARVIS
    # =====================================

    def stop_jarvis(self):

        if self.bridge is None:
            return

        if not self.bridge.is_running():
            return

        self.bridge.stop()

        self.voice_status.configure(
            text="Stopping JARVIS..."
        )

        self.system_status.configure(
            text="STOPPING",
            text_color=THEME["warning"]
        )

        self.visualizer.set_state(
            "stopping"
        )

        self.stop_button.configure(
            state="disabled"
        )

    # =====================================
    # MUTE / UNMUTE
    # =====================================

    def toggle_mute(self):

        if self.bridge is None:
            return

        if not self.bridge.is_running():
            return

        self.is_muted = not self.is_muted

        try:

            self.bridge.set_muted(
                self.is_muted
            )

            if self.is_muted:

                self.mute_button.configure(
                    text="UNMUTE",
                    fg_color=THEME["warning"],
                    hover_color="#D97706"
                )

            else:

                self.mute_button.configure(
                    text="MUTE",
                    fg_color=THEME["primary"],
                    hover_color="#0284C7"
                )

        except Exception as error:

            self.is_muted = not self.is_muted
            self.show_error(str(error))

    # =====================================
    # EVENT PROCESSING
    # =====================================

    def process_events(self):

        if self.closing:
            return

        if self.bridge is not None:

            while True:

                event_data = self.bridge.get_event()

                if event_data is None:
                    break

                event = event_data.get("event")
                data = event_data.get("data")

                # -----------------------------
                # STATUS EVENT
                # -----------------------------

                if event == "status":

                    self.visualizer.set_state(data)

                    status_text = {
                        "initializing": "INITIALIZING",
                        "standby": "SYSTEM READY",
                        "waiting": "WAITING FOR WAKE WORD",
                        "listening": "LISTENING",
                        "thinking": "PROCESSING",
                        "speaking": "SPEAKING",
                        "stopping": "STOPPING",
                        "stopped": "STOPPED"
                    }

                    self.voice_status.configure(
                        text=status_text.get(
                            data,
                            str(data).upper()
                        )
                    )

                    if data in ("standby", "waiting"):

                        self.system_status.configure(
                            text="SYSTEM READY",
                            text_color=THEME["success"]
                        )

                    elif data == "initializing":

                        self.system_status.configure(
                            text="INITIALIZING",
                            text_color=THEME["warning"]
                        )

                    elif data == "stopped":

                        self.system_status.configure(
                            text="SYSTEM STOPPED",
                            text_color=THEME["muted"]
                        )

                    elif data == "stopping":

                        self.system_status.configure(
                            text="STOPPING",
                            text_color=THEME["warning"]
                        )

                # -----------------------------
                # USER MESSAGE
                # -----------------------------

                elif event == "user_message":

                    self.chat.add_message(
                        "YOU",
                        str(data)
                    )

                # -----------------------------
                # ASSISTANT MESSAGE
                # -----------------------------

                elif event == "assistant_message":

                    self.chat.add_message(
                        "JARVIS",
                        str(data)
                    )

                    self.response_label.configure(
                        text=str(data)
                    )

                # -----------------------------
                # ERROR EVENT
                # -----------------------------

                elif event == "error":

                    self.show_error(
                        str(data)
                    )

            # -----------------------------
            # CHECK RUNNING STATE
            # -----------------------------

            if not self.bridge.is_running():

                self.is_running = False
                self.is_muted = False

                self.start_button.configure(
                    state="normal"
                )

                self.stop_button.configure(
                    state="disabled"
                )

                self.mute_button.configure(
                    state="disabled",
                    text="MUTE",
                    fg_color=THEME["primary"],
                    hover_color="#0284C7"
                )

        self.after(
            100,
            self.process_events
        )

    # =====================================
    # ERROR DISPLAY
    # =====================================

    def show_error(self, message):

        self.visualizer.set_state(
            "error"
        )

        self.voice_status.configure(
            text="An error occurred"
        )

        self.response_label.configure(
            text=str(message),
            text_color=THEME["danger"]
        )

        self.system_status.configure(
            text="SYSTEM ERROR",
            text_color=THEME["danger"]
        )

    # =====================================
    # SAFE APPLICATION CLOSING
    # =====================================

    def on_close(self):

        if self.closing:
            return

        self.closing = True

        if self.bridge is not None:

            if self.bridge.is_running():

                self.bridge.stop()

                self.voice_status.configure(
                    text="Stopping JARVIS before closing..."
                )

                self._wait_for_shutdown()
                return

        self.destroy()

    def _wait_for_shutdown(self):

        if self.bridge is not None and self.bridge.is_running():

            self.after(
                100,
                self._wait_for_shutdown
            )

        else:
            self.destroy()


# =========================================
# STANDALONE TEST
# =========================================

if __name__ == "__main__":

    app = JarvisDashboard()
    app.mainloop()
