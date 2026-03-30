import tkinter as tk

class AppGUI:
   def __init__(self, globals):
        self.globals = globals
        self.root = self.globals['root']
      
   def widgets_container(self) -> None:
        """Creates container frames for UI widgets."""
        self.frame_search = tk.Frame(self.root, bg='#DBDBDB')
        self.frame_search.pack(padx=10, pady=10)
        
        self.frame_scroll = tk.Frame(self.root, bg='#DBDBDB')
        self.frame_scroll.pack(padx=10, pady=10)

        self.frame_select = tk.Frame(self.root, bg='#DBDBDB')
        self.frame_select.pack(padx=10, pady=10)

        self.frame_elements = tk.Frame(self.root, bg='#DBDBDB')
        self.frame_elements.pack(padx=10, pady=10)

   def create_interface(self) -> None:
        """Creates user interface with all widgets."""
        # Search panel
        self.path_label = tk.Label(
            self.frame_search,
            text='Path:',
            font=('Helvetica', 10, 'bold'),
            bg='#DBDBDB',
        )
        self.path_label.grid(row=0, column=0, padx=10, pady=10)
       
        self.path_entry = tk.Entry(
            self.frame_search, 
            width=75, 
            bd=0, 
            highlightcolor='#A2A2A2', 
            highlightthickness=1,
            font=('Arial', 9, 'italic')
        )
        self.path_entry.grid(row=0, column=1, padx=10, pady=10)
       
        self.search_button = tk.Button(
            self.frame_search,
            text='Search',
            state='disabled',
            width=10,
            bd=0,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            cursor='hand2'
        )
        self.search_button.grid(row=0, column=2, padx=10, pady=10)
       
        self.update_button = tk.Button(
            self.frame_search,
            text='Update',
            state='disabled',
            width=10,
            bd=0,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            cursor='hand2'
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
       
        self.reset_button = tk.Button(
            self.frame_search,
            text='Reset',
            width=10,
            bd=0,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            cursor='hand2'
        )
        self.reset_button.grid(row=1, column=2, padx=10, pady=10)
       
        self.up_button = tk.Button(
            self.frame_scroll,
            text='Up',
            width=10,
            state='disabled',
            bd=0,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            cursor='hand2'
        )
        self.up_button.grid(row=0, column=3, padx=10, pady=10)
       
        self.select_button = tk.Button(
            self.frame_scroll,
            text='Select',
            state='disabled',
            width=10,
            bd=0,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            cursor='hand2'
        )
        self.select_button.grid(row=0, column=4, padx=10, pady=10)
       
        self.down_button = tk.Button(
            self.frame_scroll,
            text='Down',
            width=10,
            state='disabled',
            bd=0,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            cursor='hand2'
        )
        self.down_button.grid(row=0, column=5, padx=10, pady=10)
       
        # Main list window
        self.select_window = tk.Listbox(
            self.frame_select,
            selectmode='browse',
            background='SystemButtonFace',
            selectbackground='blue',
            width=110,
            height=15,
            bd=0,
            highlightthickness=0,
            cursor='hand2',
            activestyle='none'
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

        self.elements_label = tk.Label(
            self.frame_elements,
            text='',
            font=('Helvetica', 10, 'bold'),
            bg='#DBDBDB'
        )
        self.elements_label.grid(row=0, column=0, padx=10, pady=10)

        self.current_label = tk.Label(
            self.frame_elements,
            text='',
            font=('Helvetica', 10, 'bold'),
            bg='#DBDBDB'
        )
        self.current_label.grid(row=0, column=1, padx=10, pady=10)
       
        # Control panel
        self.back_button = tk.Button(
            self.frame_scroll,
            text='Back',
            state='disabled',
            width=10,
            bd=0,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            cursor='hand2'
        )
        self.back_button.grid(row=0, column=0, padx=10, pady=10)
       
        self.next_button = tk.Button(
            self.frame_scroll,
            text='Next',
            state='disabled',
            width=10,
            bd=0,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            cursor='hand2'
        )
        self.next_button.grid(row=0, column=1, padx=10, pady=10)
       
        self.settings_button = tk.Button(
            self.frame_scroll,
            text='Settings',
            state='disabled',
            width=10,
            bd=0,
            bg='#C2C2C2',
            activebackground='#C2C2C2',
            cursor='hand2'
        )
        self.settings_button.grid(row=0, column=2, padx=10, pady=10)
