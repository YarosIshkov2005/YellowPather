import tkinter as tk

class SettingsGUI:
    def __init__(self, settings):
        self.settings = settings

        self.settings_window = None

    def widgets_container(self) -> None:
        """Creates container frame for settings widgets."""
        self.parent_frame = tk.Frame(self.settings_window)
        self.parent_frame.pack(padx=10, pady=10)

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
        self.file_settings = tk.Label(
            self.settings_frame_1,
            text='File settings:',
            font=('Helvetica', 9, 'bold')
        )
        self.file_settings.grid(row=0, column=0, padx=10, pady=10)

        self.search_settings = tk.Label(
            self.settings_frame_1,
            text='Search settings:',
            font=('Helvetica', 9, 'bold')
        )
        self.search_settings.grid(row=0, column=1, padx=10, pady=10)

        self.render_settings = tk.Label(
            self.settings_frame_1,
            text='Render settings:',
            font=('Helvetica', 9, 'bold')
        )
        self.render_settings.grid(row=0, column=2, padx=10, pady=10)

        self.open_button = tk.Button(
            self.settings_frame_1,
            text='Open',
            state='disabled',
            width=10,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            bd=0,
            cursor='hand2'
        )
        self.open_button.grid(row=1, column=0, padx=10, pady=10)

        self.radiobutton_1 = tk.Radiobutton(
            self.settings_frame_1,
            indicatoron=False,
            text='Protected',
            value='Protected',
            font=('SegoeUI', 9, 'bold'),
            width=10,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            bd=0,
            cursor='hand2'
        )
        self.radiobutton_1.grid(row=1, column=1, padx=10, pady=10)

        self.radiobutton_2 = tk.Radiobutton(
            self.settings_frame_1,
            indicatoron=False,
            text='Changed',
            value='Changed',
            font=('SegoeUI', 9, 'bold'),
            width=10,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            bd=0,
            cursor='hand2'
        )
        self.radiobutton_2.grid(row=2, column=1, padx=10, pady=10)

        self.radiobutton_3 = tk.Radiobutton(
            self.settings_frame_1,
            indicatoron=False,
            text='Insert name',
            value='Insert name',
            font=('SegoeUI', 9, 'bold'),
            width=10,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            bd=0,
            cursor='hand2'
        )
        self.radiobutton_3.grid(row=1, column=2, padx=10, pady=10)

        self.radiobutton_4 = tk.Radiobutton(
            self.settings_frame_1,
            indicatoron=False,
            text="Don't insert",
            value="Don't insert",
            font=('SegoeUI', 9, 'bold'),
            width=10,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            bd=0,
            cursor='hand2'
        )
        self.radiobutton_4.grid(row=2, column=2, padx=10, pady=10)

        self.exit_button = tk.Button(
            self.settings_frame_1,
            text='Exit',
            width=10,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            bd=0,
            cursor='hand2'
        )
        self.exit_button.grid(row=2, column=0, padx=10, pady=10)

        self.create_delete_rename = tk.Label(
            self.settings_frame_2,
            text='Create / Delete / Rename:',
            font=('Helvetica', 9, 'bold')
        )
        self.create_delete_rename.grid(row=0, column=1, padx=5, pady=10)

        self.back_button = tk.Button(
            self.settings_frame_2,
            text='Back',
            width=12,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            bd=0,
            cursor='hand2'
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
            width=12,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            bd=0,
            cursor='hand2'
        )
        self.next_button.grid(row=1, column=2, padx=5, pady=10)

        self.create_button = tk.Button(
            self.settings_frame_2,
            text='Create',
            width=12,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            bd=0,
            cursor='hand2'
        )
        self.create_button.grid(row=2, column=0, padx=10, pady=10)

        self.delete_button = tk.Button(
            self.settings_frame_2,
            text='Delete',
            width=12,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            bd=0,
            cursor='hand2'
        )
        self.delete_button.grid(row=2, column=1, padx=5, pady=10)

        self.rename_button = tk.Button(
            self.settings_frame_2,
            text='Rename',
            width=12,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            bd=0,
            cursor='hand2'
        )
        self.rename_button.grid(row=2, column=2, padx=5, pady=10)

        self.sorting = tk.Label(
            self.settings_frame_3,
            text='Sorting:',
            font=('Helvetica', 9, 'bold')
        )
        self.sorting.grid(row=0, column=1, padx=10, pady=10)

        self.left_button = tk.Button(
            self.settings_frame_3,
            text='Back',
            width=8,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            bd=0,
            cursor='hand2'
        )
        self.left_button.grid(row=1, column=0, padx=10, pady=10)

        self.sorting_type = tk.Label(
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
            width=8,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            bd=0,
            cursor='hand2'
        )
        self.right_button.grid(row=1, column=2, padx=10, pady=10)
