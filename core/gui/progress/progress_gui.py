from tkinter import ttk

class ProgressGUI:
    def __init__(self, progress_window) -> None:
        self.progress_window = progress_window

    def widgets_container(self):
        self.frame_1 = ttk.Frame(self.progress_window)
        self.frame_1.pack(padx=10, pady=10, fill='x')

        self.frame_2 = ttk.Frame(self.progress_window)
        self.frame_2.pack(padx=10, pady=10, fill='x')

        self.frame_3 = ttk.Frame(self.progress_window)
        self.frame_3.pack(padx=10, pady=10, fill='x')

    def create_widgets(self):
        self.description_label = ttk.Label(self.frame_1, text='', font=('Helvetica', 10, 'bold'))
        self.description_label.grid(row=0, column=0, padx=10, pady=10)

        self.progress_bar = ttk.Progressbar(self.frame_2, orient='horizontal')
        self.progress_bar.grid(row=0, column=0, padx=10, pady=10)

        self.progress_label = ttk.Label(self.frame_3, text='', font=('Helvetica', 10, 'bold'))
        self.progress_label.grid(row=0, column=0, padx=10, pady=10)

        self.cancel_button = ttk.Button(self.frame_3, text='Cancel')
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10)
