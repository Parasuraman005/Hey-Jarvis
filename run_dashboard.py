
import customtkinter as ctk

from main import run_assistant
from ui.dashboard import JarvisDashboard


def main():

    ctk.set_appearance_mode("dark")

    app = JarvisDashboard(
        assistant_runner=run_assistant
    )

    app.mainloop()


if __name__ == "__main__":
    main()
