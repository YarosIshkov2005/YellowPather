import tkinter as tk
from tkinter import ttk

class AppGUI:
   def __init__(self, root):
       self.root = root
      
   def widgets_container(self) -> None:
        """Creates container frames for UI widgets."""
        self.frame_search = ttk.Frame(self.root)
        self.frame_search.pack(anchor='center')
        
        self.frame_scroll = ttk.Frame(self.root)
        self.frame_scroll.pack(anchor='center')

        self.frame_select = ttk.Frame(self.root)
        self.frame_select.pack(anchor='center')

        self.frame_elements = ttk.Frame(self.root)
        self.frame_elements.pack(anchor='center')

        self.frame_functions = ttk.Frame(self.root)
        self.frame_functions.pack(anchor='center')

   def create_interface(self) -> None:
        """Creates user interface with all widgets."""
        # Search panel
        self.path_label = ttk.Label(
            self.frame_search,
            text='Path:',
            font=('Helvetica', 10, 'bold')
        )
        self.path_label.grid(row=0, column=0, padx=10, pady=10)
       
        self.path_entry = ttk.Entry(self.frame_search)
        self.path_entry.grid(row=0, column=1, padx=10, pady=10)
       
        self.search_button = ttk.Button(
            self.frame_search,
            text='Search',
            state='disabled'
        )
        self.search_button.grid(row=0, column=2, padx=10, pady=10)
       
        self.update_button = ttk.Button(
            self.frame_search,
            text='Update',
            state='disabled'
        )
        self.update_button.grid(row=1, column=0, padx=10, pady=10)
       
        self.scrollbar_entry = tk.Scrollbar(
            self.frame_search,
            orient='horizontal',
            command=self.path_entry.xview
        )
        self.scrollbar_entry.grid(
            row=1, column=1, padx=10, pady=10, sticky='nsew'
        )
        self.path_entry['xscrollcommand'] = self.scrollbar_entry.set
       
        self.reset_button = ttk.Button(
            self.frame_search,
            text='Reset'
        )
        self.reset_button.grid(row=1, column=2, padx=10, pady=10)
       
        self.up_button = ttk.Button(
            self.frame_scroll,
            text='<',
            width=5,
            state='disabled'
        )
        self.up_button.grid(row=0, column=0, padx=10, pady=10)
       
        self.select_button = ttk.Button(
            self.frame_scroll,
            text='Select',
            state='disabled'
        )
        self.select_button.grid(row=0, column=1, padx=10, pady=10)
       
        self.down_button = ttk.Button(
            self.frame_scroll,
            text='>',
            width=5,
            state='disabled'
        )
        self.down_button.grid(row=0, column=2, padx=10, pady=10)
       
        # Main list window
        self.select_window = tk.Listbox(
            self.frame_select,
            selectmode='single',
            selectbackground='blue',
            width=35
        )
        self.select_window.grid(row=0, column=0, padx=10, pady=10)
       
        self.scrollbar_window = tk.Scrollbar(
            self.frame_select,
            orient='vertical',
            command=self.select_window.yview
        )
        self.scrollbar_window.grid(
            row=0, column=1, padx=10, pady=10, sticky='ns'
        )
        self.select_window['yscrollcommand'] = self.scrollbar_window.set

        self.elements_label = ttk.Label(
            self.frame_elements,
            text='',
            font=('Helvetica', 10, 'bold')
        )
        self.elements_label.grid(row=0, column=0, padx=10, pady=10)

        self.current_label = ttk.Label(
            self.frame_elements,
            text='',
            font=('Helvetica', 10, 'bold')
        )
        self.current_label.grid(row=0, column=1, padx=10, pady=10)
       
        # Control panel
        self.back_button = ttk.Button(
            self.frame_functions,
            text='Back',
            state='disabled'
        )
        self.back_button.grid(row=0, column=0, padx=10, pady=10)
       
        self.next_button = ttk.Button(
            self.frame_functions,
            text='Next',
            state='disabled'
        )
        self.next_button.grid(row=0, column=1, padx=10, pady=10)
       
        self.settings_button = ttk.Button(
            self.frame_functions,
            text='Settings',
            state='disabled'
        )
        self.settings_button.grid(row=0, column=2, padx=10, pady=10)
