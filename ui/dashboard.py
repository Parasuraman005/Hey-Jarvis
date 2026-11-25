if event == "status":
    self.visualizer.set_state(data)

    if data in ("standby", "waiting", "stopped"):
        self.system_status.configure(
            text="SYSTEM READY"
        )

    elif data == "error":
        self.system_status.configure(
            text="SYSTEM ERROR"
        )

elif event == "user_message":
    self.chat.add_message("YOU", data)

elif event == "assistant_message":
    self.chat.add_message("JARVIS", data)
    self.response_label.configure(text=data)

elif event == "error":
    self.show_error(data)