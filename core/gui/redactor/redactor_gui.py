import tkinter as tk
from tkinter import ttk

class RedactorGUI:
    def __init__(self, file_redactor):
        self.file_redactor = file_redactor

        self.redactor_window = None
        
    def widgets_container(self) -> None:
        self.frame_1 = ttk.Frame(self.redactor_window, width=300, height=100)
        self.frame_1.pack(padx=5, pady=5)
        
        self.frame_2 = ttk.Frame(self.redactor_window, width=300, height=500)
        self.frame_2.pack(padx=5, pady=5)
        
        self.frame_3 = ttk.Frame(self.redactor_window, width=300, height=100)
        self.frame_3.pack(padx=5, pady=5)
        
    def create_widgets(self):
        self.icon_label = ttk.Label(
            self.frame_1
        )
        self.icon_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.lang_label = ttk.Label(
            self.frame_1,
            text='lang:',
            font=('Helvetica', 9, 'bold')
        )
        self.lang_label.grid(row=0, column=1, padx=10, pady=10)
        
        self.space_1 = ttk.Label(
            self.frame_1,
            text='        ',
            font=('Helvetica', 9, 'bold')
        )
        self.space_1.grid(row=0, column=2, padx=10, pady=10)
        
        self.file_label = ttk.Label(
            self.frame_1,
            text='name:',
            font=('Helvetica', 9, 'bold')
        )
        self.file_label.grid(row=0, column=3, padx=10, pady=10)
        
        self.space_2 = ttk.Label(
            self.frame_1,
            text='        ',
            font=('Helvetica', 9, 'bold')
        )
        self.space_2.grid(row=0, column=4, padx=10, pady=10)
        
        self.code_label = ttk.Label(
            self.frame_1,
            text='encode:',
            font=('Helvetica', 9, 'bold')
        )
        self.code_label.grid(row=0, column=5, padx=10, pady=10)
        
        self.text_widget = tk.Text(self.frame_2, width=70, height=15)
        self.text_widget.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        self.text_scrollbar_ver = tk.Scrollbar(self.frame_2, orient='vertical', command=self.text_widget.yview)
        self.text_scrollbar_ver.grid(row=0, column=1, padx=5, pady=5, sticky='ns')
        
        self.text_widget.config(yscrollcommand=self.text_scrollbar_ver.set)
        
        self.text_scrollbar_horiz = tk.Scrollbar(self.frame_2, orient='horizontal', command=self.text_widget.xview)
        self.text_scrollbar_horiz.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        
        self.text_widget.config(xscrollcommand=self.text_scrollbar_horiz.set)
        
        self.frame_2.grid_rowconfigure(0, weight=1)
        self.frame_2.grid_columnconfigure(0, weight=1)
        
        self.exit_button = ttk.Button(self.frame_3, text='Exit')
        self.exit_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.clear_button = ttk.Button(self.frame_3, text='Clear')
        self.clear_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.save_button = ttk.Button(self.frame_3, text='Save')
        self.save_button.grid(row=0, column=2, padx=10, pady=10)
