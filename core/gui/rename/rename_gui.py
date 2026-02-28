from tkinter import ttk

class RenameGUI:
    def __init__(self, rename_window) -> None:
        self.rename_window = rename_window

    def widgets_container(self):
        self.rename_frame_1 = ttk.Frame(self.rename_window)
        self.rename_frame_1.pack(padx=10, pady=10, side='top')

        self.rename_frame_2 = ttk.Frame(self.rename_window)
        self.rename_frame_2.pack(padx=10, pady=10, side='bottom')

    def create_widgets(self):
        self.enter_label = ttk.Label(
            self.rename_frame_1,
            text='Name:',
            font=('Helvetica', 9, 'bold')
        )
        self.enter_label.grid(row=0, column=0, padx=10, pady=10)

        self.enter_field = ttk.Entry(
            self.rename_frame_1,
            width=25
        )
        self.enter_field.grid(row=0, column=1, padx=10, pady=10)

        self.cancel_button = ttk.Button(
            self.rename_frame_2,
            text='Cancel'
        )
        self.cancel_button.grid(row=0, column=0, padx=10, pady=10)

        self.space_label = ttk.Label(
            self.rename_frame_2,
            text='       '
        )
        self.space_label.grid(row=0, column=1, padx=10, pady=10)

        self.next_button = ttk.Button(
            self.rename_frame_2,
            text='Next'
        )
        self.next_button.grid(row=0, column=2, padx=10, pady=10)
