class MainEvents:
    def __init__(self, root, app_gui, app_navigator, app_render, button_state, keyboard, path_analyzer, settings, update_gui) -> None:
        self.root = root
        self.app_gui = app_gui
        self.app_navigator = app_navigator
        self.app_render = app_render
        self.button_state = button_state
        self.keyboard = keyboard
        self.path_analyzer = path_analyzer
        self.settings = settings
        self.update_gui = update_gui

    def bind_events(self):
       self.root.bind('<Return>', self.keyboard.search_path_callback)
       self.root.bind('<Escape>', self.keyboard.reset_path_callback)
       self.root.bind('<Clear>', self.keyboard.marker_select_callback)

       self.root.bind('<Prior>', self.keyboard.marker_up_callback)
       self.root.bind('<Next>', self.keyboard.marker_down_callback)
       self.root.bind('<Home>', self.keyboard.directory_up_callback)
       self.root.bind('<End>', self.keyboard.directory_down_callback)

       self.root.bind('<Up>', self.keyboard.marker_up_callback)
       self.root.bind('<Down>', self.keyboard.marker_down_callback)
       self.root.bind('<Left>', self.keyboard.directory_up_callback)
       self.root.bind('<Right>', self.keyboard.directory_down_callback)

       self.root.bind('<F5>', self.keyboard.update_gui_callback)

       self.app_gui.path_entry.bind('<KeyPress>', self.app_render.protect_root_delete)
       self.app_gui.path_entry.bind('<ButtonRelease-1>', self.app_render.protect_root_path)
       self.app_gui.path_entry.bind('<KeyRelease>', self.button_state.control_search_button)
       self.app_gui.select_window.bind('<<ListboxSelect>>', self.app_navigator.select_path)
       
       self.app_gui.search_button.config(command=self.path_analyzer.search_path)
       self.app_gui.update_button.config(command=self.update_gui.update_gui)
       self.app_gui.reset_button.config(command=self.app_navigator.reset_path)
       self.app_gui.up_button.config(command=self.app_navigator.marker_up)
       self.app_gui.select_button.config(command=self.app_navigator.marker_select)
       self.app_gui.down_button.config(command=self.app_navigator.marker_down)
       self.app_gui.back_button.config(command=self.app_navigator.directory_up)
       self.app_gui.next_button.config(command=self.app_navigator.directory_down)
       self.app_gui.settings_button.config(command=self.settings.create_window)
