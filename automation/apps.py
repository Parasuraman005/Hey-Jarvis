
import subprocess
import os
import shutil


class AppController:

    def __init__(self):
        self.apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "command prompt": "cmd.exe",
            "powershell": "powershell.exe",
            "task manager": "taskmgr.exe",
            "file explorer": "explorer.exe",
        }

        self.apps.update({
            "chrome": os.path.expandvars(
                r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"
            ),
            "vs code": "code",
            "visual studio code": "code",
        })

    def open_app(self, app_name):

        app_name = app_name.lower().strip()

        executable = self.apps.get(app_name)

        if not executable:
            return f"I don't know how to open {app_name} yet."

        try:
            if os.path.isabs(executable):
                if not os.path.exists(executable):
                    return f"{app_name} is not installed at the configured path."

                subprocess.Popen([executable])
            else:
                path = shutil.which(executable)

                if not path:
                    return f"I couldn't find {app_name} on this computer."

                subprocess.Popen([path])

            return f"Opening {app_name}."

        except Exception as error:
            return f"Unable to open {app_name}: {error}"
