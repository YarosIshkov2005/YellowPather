from tkinter import ttk

class SettingsGUI:
    def __init__(self, settings):
        self.settings = settings

        self.settings_window = None

    def widgets_container(self) -> None:
        """Creates container frame for settings widgets."""
        self.settings_frame_1 = ttk.Frame(self.settings_window)
        self.settings_frame_1.grid(row=0, column=0, padx=10, pady=10)

        self.settings_frame_2 = ttk.Frame(self.settings_window)
        self.settings_frame_2.grid(row=0, column=1, padx=10, pady=10)

        self.settings_frame_3 = ttk.Frame(self.settings_window)
        self.settings_frame_3.grid(row=1, column=0, padx=10, pady=10)

    def create_widgets(self) -> None:
        """Creates settings window widgets."""
        self.file_settings = ttk.Label(
            self.settings_frame_1,
            text='File settings:',
            font=('Helvetica', 9, 'bold')
        )
        self.file_settings.grid(row=0, column=0, padx=10, pady=10)

        self.open_button = ttk.Button(
            self.settings_frame_1,
            text='Open',
            state='disabled'
        )
        self.open_button.grid(row=1, column=0, padx=10, pady=10)

        self.exit_button = ttk.Button(
            self.settings_frame_1,
            text='Exit'
        )
        self.exit_button.grid(row=2, column=0, padx=10, pady=10)

        self.create_delete_rename = ttk.Label(
            self.settings_frame_2,
            text='Create / Delete / Rename:',
            font=('Helvetica', 9, 'bold')
        )
        self.create_delete_rename.grid(row=0, column=1, padx=5, pady=10)

        self.back_button = ttk.Button(
            self.settings_frame_2,
            text='<<<',
            width=11
        )
        self.back_button.grid(row=1, column=0, padx=5, pady=10)

        self.select_type = ttk.Label(
            self.settings_frame_2,
            text='    catalog    ',
            font=('Helvetica', 10, 'bold'),
            background='#002137',
            foreground='#FFFFFF',
            width=10
        )
        self.select_type.grid(row=1, column=1, padx=5, pady=10)

        self.next_button = ttk.Button(
            self.settings_frame_2,
            text='>>>',
            width=11
        )
        self.next_button.grid(row=1, column=2, padx=5, pady=10)

        self.create_button = ttk.Button(
            self.settings_frame_2,
            text='Create'
        )
        self.create_button.grid(row=2, column=0, padx=10, pady=10)

        self.delete_button = ttk.Button(
            self.settings_frame_2,
            text='Delete'
        )
        self.delete_button.grid(row=2, column=1, padx=5, pady=10)

        self.rename_button = ttk.Button(
            self.settings_frame_2,
            text='Rename'
        )
        self.rename_button.grid(row=2, column=2, padx=5, pady=10)
