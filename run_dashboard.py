from main import run_assistant
from ui.dashboard import JarvisDashboard


if __name__ == "__main__":
    app = JarvisDashboard(
        assistant_runner=run_assistant
    )
    app.mainloop()