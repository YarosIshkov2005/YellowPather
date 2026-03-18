import tkinter as tk

from tkinter import ttk

class SettingsGUI:
    def __init__(self, settings):
        self.settings = settings

        self.settings_window = None

    def widgets_container(self) -> None:
        """Creates container frame for settings widgets."""
        self.parent_frame = tk.Frame(self.settings_window)
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

        self.search_settings = ttk.Label(
            self.settings_frame_1,
            text='Search settings:',
            font=('Helvetica', 9, 'bold')
        )
        self.search_settings.grid(row=0, column=1, padx=10, pady=10)

        self.render_settings = ttk.Label(
            self.settings_frame_1,
            text='Render settings:',
            font=('Helvetica', 9, 'bold')
        )
        self.render_settings.grid(row=0, column=2, padx=10, pady=10)

        self.open_button = tk.Button(
            self.settings_frame_1,
            text='Open',
            font=('Helvetica', 9, 'bold'),
            state='disabled',
            cursor='hand2',
            width=10
        )
        self.open_button.grid(row=1, column=0, padx=10, pady=10)

        self.radiobutton_1 = tk.Radiobutton(
            self.settings_frame_1,
            indicatoron=False,
            text='Protected',
            value='Protected',
            cursor='hand2',
            font=('SegoeUI', 9, 'bold'),
            width=10
        )
        self.radiobutton_1.grid(row=1, column=1, padx=10, pady=10)

        self.radiobutton_2 = tk.Radiobutton(
            self.settings_frame_1,
            indicatoron=False,
            text='Changed',
            value='Changed',
            cursor='hand2',
            font=('SegoeUI', 9, 'bold'),
            width=10
        )
        self.radiobutton_2.grid(row=2, column=1, padx=10, pady=10)

        self.radiobutton_3 = tk.Radiobutton(
            self.settings_frame_1,
            indicatoron=False,
            text='Insert name',
            value='Insert name',
            cursor='hand2',
            font=('SegoeUI', 9, 'bold'),
            width=10
        )
        self.radiobutton_3.grid(row=1, column=2, padx=10, pady=10)

        self.radiobutton_4 = tk.Radiobutton(
            self.settings_frame_1,
            indicatoron=False,
            text="Don't insert",
            value="Don't insert",
            cursor='hand2',
            font=('SegoeUI', 9, 'bold'),
            width=10
        )
        self.radiobutton_4.grid(row=2, column=2, padx=10, pady=10)

        self.exit_button = tk.Button(
            self.settings_frame_1,
            text='Exit',
            font=('Helvetica', 9, 'bold'),
            cursor='hand2',
            width=10
        )
        self.exit_button.grid(row=2, column=0, padx=10, pady=10)

        self.create_delete_rename = ttk.Label(
            self.settings_frame_2,
            text='Create / Delete / Rename:',
            font=('Helvetica', 9, 'bold')
        )
        self.create_delete_rename.grid(row=0, column=1, padx=5, pady=10)

        self.back_button = tk.Button(
            self.settings_frame_2,
            text='Back',
            font=('Helvetica', 9, 'bold'),
            cursor='hand2',
            width=12
        )
        self.back_button.grid(row=1, column=0, padx=5, pady=10)

        self.select_type = tk.Label(
            self.settings_frame_2,
            text=f'    {self.settings._settings_manager.create_type}    ',
            font=('Helvetica', 10, 'bold'),
            background='#002137',
            foreground='#FFFFFF',
            width=11
        )
        self.select_type.grid(row=1, column=1, padx=5, pady=10)

        self.next_button = tk.Button(
            self.settings_frame_2,
            text='Next',
            font=('Helvetica', 9, 'bold'),
            cursor='hand2',
            width=12
        )
        self.next_button.grid(row=1, column=2, padx=5, pady=10)

        self.create_button = tk.Button(
            self.settings_frame_2,
            text='Create',
            font=('Helvetica', 9, 'bold'),
            cursor='hand2',
            width=12
        )
        self.create_button.grid(row=2, column=0, padx=10, pady=10)

        self.delete_button = tk.Button(
            self.settings_frame_2,
            text='Delete',
            font=('Helvetica', 9, 'bold'),
            cursor='hand2',
            width=12
        )
        self.delete_button.grid(row=2, column=1, padx=5, pady=10)

        self.rename_button = tk.Button(
            self.settings_frame_2,
            text='Rename',
            font=('Helvetica', 9, 'bold'),
            cursor='hand2',
            width=12
        )
        self.rename_button.grid(row=2, column=2, padx=5, pady=10)

        self.sorting = ttk.Label(
            self.settings_frame_3,
            text='Sorting:',
            font=('Helvetica', 9, 'bold')
        )
        self.sorting.grid(row=0, column=1, padx=10, pady=10)

        self.left_button = tk.Button(
            self.settings_frame_3,
            text='Back',
            font=('Helvetica', 9, 'bold'),
            cursor='hand2',
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

        self.right_button = tk.Button(
            self.settings_frame_3,
            text='Next',
            font=('Helvetica', 9, 'bold'),
            cursor='hand2',
            width=8
        )
        self.right_button.grid(row=1, column=2, padx=10, pady=10)
