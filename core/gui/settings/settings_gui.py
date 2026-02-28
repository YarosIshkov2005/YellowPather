from tkinter import ttk

class SettingsGUI:
    def __init__(self, settings):
        self.settings = settings

        self.settings_window = None

    def widgets_container(self) -> None:
        """Creates container frame for settings widgets."""
        self.settings_frame = ttk.Frame(self.settings_window)
        self.settings_frame.pack(anchor='center')

    def create_widgets(self) -> None:
        """Creates settings window widgets."""
        self.settings_label_1 = ttk.Label(
            self.settings_frame,
            text='File settings:',
            font=('Helvetica', 9, 'bold')
        )
        self.settings_label_1.grid(row=0, column=0, padx=10, pady=10)

        self.space_label_2 = ttk.Label(
            self.settings_frame,
            text='    '
        )
        self.space_label_2.grid(row=0, column=1, padx=10, pady=10)

        self.settings_label_3 = ttk.Label(
            self.settings_frame,
            text='Create New:',
            font=('Helvetica', 9, 'bold')
        )
        self.settings_label_3.grid(row=0, column=2, padx=10, pady=10)
       
        self.open_button = ttk.Button(
            self.settings_frame,
            text='Open',
            state='disabled'
        )
        self.open_button.grid(row=1, column=0, padx=10, pady=10)

        self.back_button = ttk.Button(
            self.settings_frame,
            text='<',
            width=5
        )
        self.back_button.grid(row=1, column=1, padx=10, pady=10)

        self.select_type = ttk.Label(
            self.settings_frame,
            text='    catalog    ',
            font=('Helvetica', 10, 'bold'),
            background='#002137',
            foreground='#FFFFFF',
            width=10
        )
        self.select_type.grid(row=1, column=2, padx=10, pady=10)

        self.next_button = ttk.Button(
            self.settings_frame,
            text='>',
            width=5
        )
        self.next_button.grid(row=1, column=3, padx=10, pady=10)

        self.create_button = ttk.Button(
            self.settings_frame,
            text='Create'
        )
        self.create_button.grid(row=1, column=4, padx=10, pady=10)
       
        self.space_label_1 = ttk.Label(
            self.settings_frame,
            text='        ',
            font=('Helvetica', 3, 'bold')
        )
        self.space_label_1.grid(row=2, column=0, padx=10, pady=10)
       
        self.settings_label_2 = ttk.Label(
            self.settings_frame,
            text='Exit:',
            font=('Helvetica', 9, 'bold')
        )
        self.settings_label_2.grid(row=3, column=0, padx=10, pady=10)
       
        self.exit_button = ttk.Button(
            self.settings_frame,
            text='Exit'
        )
        self.exit_button.grid(row=4, column=0, padx=10, pady=10)
