import tkinter as tk

from tkinter import ttk

class SettingsGUI:
    def __init__(self, settings):
        self.settings = settings

        self.settings_window = None

    def widgets_container(self) -> None:
        """Creates container frame for settings widgets."""
        self.parent_frame = ttk.Frame(self.settings_window)
        self.parent_frame.pack(padx=10, pady=10, expand=True, fill='both')

        self.parent_frame.rowconfigure(0, weight=0)
        self.parent_frame.rowconfigure(1, weight=1)

        self.parent_frame.columnconfigure(0, weight=0)
        self.parent_frame.columnconfigure(1, weight=1)

        self.settings_frame_1 = tk.Frame(self.parent_frame, bg='#DBDBDB')
        self.settings_frame_1.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.settings_frame_2 = tk.Frame(self.parent_frame, bg='#DBDBDB')
        self.settings_frame_2.grid(row=0, column=1, padx=10, pady=10, sticky='e')

        self.settings_frame_3 = tk.Frame(self.parent_frame, bg='#DBDBDB')
        self.settings_frame_3.grid(row=1, column=0, padx=10, pady=10, sticky='w')

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
            width=12
        )
        self.back_button.grid(row=1, column=0, padx=5, pady=10)

        self.select_type = ttk.Label(
            self.settings_frame_2,
            text=f'    {self.settings._settings_manager.create_type}    ',
            font=('Helvetica', 10, 'bold'),
            background='#002137',
            foreground='#FFFFFF',
            width=11
        )
        self.select_type.grid(row=1, column=1, padx=5, pady=10)

        self.next_button = ttk.Button(
            self.settings_frame_2,
            text='>>>',
            width=12
        )
        self.next_button.grid(row=1, column=2, padx=5, pady=10)

        self.create_button = ttk.Button(
            self.settings_frame_2,
            text='Create',
            width=12
        )
        self.create_button.grid(row=2, column=0, padx=10, pady=10)

        self.delete_button = ttk.Button(
            self.settings_frame_2,
            text='Delete',
            width=12
        )
        self.delete_button.grid(row=2, column=1, padx=5, pady=10)

        self.rename_button = ttk.Button(
            self.settings_frame_2,
            text='Rename',
            width=12
        )
        self.rename_button.grid(row=2, column=2, padx=5, pady=10)

        self.sorter = ttk.Label(
            self.settings_frame_3,
            text='Sorter:',
            font=('Helvetica', 9, 'bold')
        )
        self.sorter.grid(row=0, column=1, padx=10, pady=10)

        self.left_button = ttk.Button(
            self.settings_frame_3,
            text='<<<',
            width=8
        )
        self.left_button.grid(row=1, column=0, padx=10, pady=10)

        self.sorting_type = ttk.Label(
            self.settings_frame_3,
            text=f"    {self.settings._settings_manager.states['sorting']}    ",
            font=('Helvetica', 10, 'bold'),
            background='#002137',
            foreground='#FFFFFF',
            width=12
        )
        self.sorting_type.grid(row=1, column=1, padx=10, pady=10)

        self.right_button = ttk.Button(
            self.settings_frame_3,
            text='>>>',
            width=8
        )
        self.right_button.grid(row=1, column=2, padx=10, pady=10)
