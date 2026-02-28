import tkinter as tk

class NotificationWindow:
    def __init__(self, root) -> None:
        self.root = root

        self.notification_window: tk.Tk = None

    def create_window(self):
        self.notification_window = tk.Toplevel(self.root)
        self.notification_window.withdraw()
        self.notification_window.attributes('-topmost', True)

    def window_focus(self):
        self.notification_window.grab_set()

    def return_focus(self, window: tk.Tk):
        window.lift()
        window.grab_set()
        window.focus_force()
        self.notification_window.grab_release()
