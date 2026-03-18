import os

import tkinter as tk
from tkinter.messagebox import showerror

class AppNavigatorCore:
    def __init__(self, globals, callstack):
        self.globals = globals
        self.callstack = callstack

        self.root = self.globals['root']
        self.app_gui = self.callstack.app_gui
        self.app_state = self.callstack.app_state
        self.app_perms = self.callstack.app_perms
        self.app_render = self.callstack.app_render
        self.button_state = self.callstack.button_state
        self.counters = self.globals['counters']
        self.catalog_detector = self.callstack.catalog_detector
        self.input_manager = self.callstack.input_manager
        self.path_manager = self.callstack.path_manager
        self.path_analyzer = self.callstack.path_analyzer
        self.mdefs = self.callstack.framework
        self.search = self.callstack.search_manager
        self.select_state = self.callstack.select_state
        self.secure_manager = self.callstack.secure_manager
        self.select_position = self.callstack.select_position

        self.index: int = 0
        self.resource_index: int = self.app_render.current_index

    def marker_up(self):
        """Moves the selector up one item."""
        if self.index > 0:
            self.app_gui.select_window.select_clear(self.index)
            self.index -= 1

            self.current_index()

            self.select_position.selected_index = self.index
            self.select_position.select_position()
        else:
            return

        navigation_path = ''
        absolute_path = self.path_manager.abs_paths[self.index]
        if self.app_state.insert_resource_name:
            navigation_path = str(absolute_path.relative_to(self.path_manager.root_path))

        self.path_manager.input_path = str(absolute_path)
        self.path_manager.selected_path = None
        self.path_manager.current_path = None
        
        self.button_state.index = self.index
        self.button_state.control_up_button()
        self.button_state.control_select_button()
        self.button_state.control_down_button()

        self.button_state.control_next_button()

        self.app_gui.path_entry.delete(self.counters['start_position'], tk.END)
        self.app_gui.path_entry.insert(self.counters['start_position'], navigation_path)
        self.app_gui.path_entry.xview_moveto(1.0)
        self.app_gui.path_entry.focus()

        if absolute_path.is_dir() and self.app_state.insert_resource_name:
            self.app_render.add_slash(absolute_path)

        self.app_gui.select_window.see(self.index)
        self.app_gui.select_window.selection_set(self.index)

        self.app_gui.select_button.config(text='Select')
        self.app_gui.select_window.config(selectbackground='blue')

        self.select_state.current_position = self.index
        self.select_state.pop_back_point()
        self.select_state.current_select()
        self.select_state.add_next_point()

        self.app_render.index = self.index

    def marker_select(self, event=None):
        """Highlights or removes the selected item: Select/Drop."""
        selected_path = None
            
        if self.path_manager.abs_paths:
            selected_path = self.path_manager.abs_paths[self.index]
        else:
            selected_path = None

        if self.app_gui.select_button.cget('text') == 'Select':
            self.app_gui.select_button.config(text='Drop')
            self.app_gui.select_window.config(selectbackground='orange')
            self.path_manager.selected_path = selected_path
        else:
            self.app_gui.select_button.config(text='Select')
            self.app_gui.select_window.config(selectbackground='blue')
            self.path_manager.selected_path = None
        self.app_gui.path_entry.focus()

    def marker_down(self):
        """Moves selector down one item."""
        if self.index < len(self.path_manager.short_names) -1:
            self.app_gui.select_window.select_clear(self.index)            
            self.index += 1

            self.current_index()

            self.select_position.selected_index = self.index
            self.select_position.select_position()
        else:
            return

        navigation_path = ''
        absolute_path = self.path_manager.abs_paths[self.index]
        if self.app_state.insert_resource_name:
            navigation_path = str(absolute_path.relative_to(self.path_manager.root_path))

        self.path_manager.input_path = str(absolute_path)
        self.path_manager.selected_path = None
        self.path_manager.current_path = None

        self.button_state.index = self.index
        self.button_state.control_up_button()
        self.button_state.control_select_button()
        self.button_state.control_down_button()

        self.button_state.control_next_button()
                    
        self.app_gui.path_entry.delete(self.counters['start_position'], tk.END)
        self.app_gui.path_entry.insert(self.counters['start_position'], navigation_path)

        if absolute_path.is_dir() and self.app_state.insert_resource_name:
            self.app_render.add_slash(absolute_path)

        self.app_gui.select_window.see(self.index)
        self.app_gui.select_window.selection_set(self.index)

        self.app_gui.select_button.config(text='Select')
        self.app_gui.select_window.config(selectbackground='blue')

        self.app_gui.path_entry.xview_moveto(1.0)
        self.app_gui.path_entry.focus()

        self.select_state.current_position = self.index
        self.select_state.pop_back_point()
        self.select_state.current_select()
        self.select_state.add_next_point()

        self.app_render.index = self.index

    def select_path(self, event=None):
        selected_incide = self.app_gui.select_window.curselection()
        if selected_incide:
            self.index = selected_incide[0]

        self.current_index()

        self.select_position.selected_index = self.index
        self.select_position.select_position()

        navigation_path = ''
        absolute_path = self.path_manager.abs_paths[self.index]
        if self.app_state.insert_resource_name:
            navigation_path = str(absolute_path.relative_to(self.path_manager.root_path))

        self.path_manager.input_path = str(absolute_path)
        self.path_manager.selected_path = None
        self.path_manager.current_path = None

        self.button_state.index = self.index
        self.button_state.control_up_button()
        self.button_state.control_select_button()
        self.button_state.control_down_button()

        self.button_state.control_next_button()

        self.app_gui.path_entry.delete(self.counters['start_position'], tk.END)
        self.app_gui.path_entry.insert(self.counters['start_position'], navigation_path)

        if absolute_path.is_dir() and self.app_state.insert_resource_name:
            self.app_render.add_slash(absolute_path)

        self.app_gui.select_window.see(self.index)
        self.app_gui.select_window.selection_set(self.index)

        self.app_gui.select_button.config(text='Select')
        self.app_gui.select_window.config(selectbackground='blue')

        self.app_gui.path_entry.xview_moveto(1.0)
        self.app_gui.path_entry.focus()

        self.select_state.current_position = self.index
        self.select_state.pop_back_point()
        self.select_state.current_select()
        self.select_state.add_next_point()

        self.app_render.index = self.index

    def current_index(self):
        self.resource_index = self.index + 1
        elements_count = self.app_render.elements_count
        self.app_gui.current_label.config(
            text=f'Element: {self.resource_index}/{elements_count}')

    def reset_path(self) -> None:
        """Resets current path to root path."""
        if self.app_state.is_search_executed:
            self.app_state.is_search_executed = False

        self.current_index()

        if self.app_state.manual_input_mode:
            user_input = self.app_gui.path_entry.get()

            if len(user_input) == 0:
                showerror(
                    title='Yellow Pather Error 016:',
                    message='It is impossible to clear an empty line!',
                    parent=self.root
                )
                self.app_gui.path_entry.focus()
                return

            if (str(self.path_manager.absolute_path) + os.sep 
                in self.secure_manager.PATH_NAME.get('current')):
                return

            self.app_gui.path_entry.delete(0, tk.END)
            self.app_gui.path_entry.focus()

            self.select_state.reset_points()
            self.button_state.update_search_state()
            return

        if self.app_state.is_parser_active:
            self.app_gui.path_entry.delete(self.counters['root_position'], tk.END)
            self.app_gui.path_entry.focus()
            return

        if self.catalog_detector.root_directory_detector(
            self.path_manager.root_path, self.path_manager.absolute_path):
            self.app_gui.path_entry.focus()
            self.button_state.update_search_state()
            return

        if not self.app_state.reset_button_active:
            self.app_state.reset_button_active = True

        if self.app_state.is_recursive_search:
            self.app_state.is_recursive_search = False

        self.mdefs._mdefs_framework.mdefs_pointer('clear')
        self.mdefs._mdefs_framework.mdefs_pointer('root')

        self.path_analyzer.generate_points(self.path_manager.root_path)
        self.path_manager.absolute_path = self.path_manager.root_path

        self.search.add_paths()
        self.app_render.update_select_window()

        self.index = 0

        self.select_position.selected_index = self.index
        self.select_position.select_position()

        absolute_path = self.path_manager.abs_paths[self.index]
        navigation_path = str(absolute_path.relative_to(self.path_manager.root_path))

        self.path_manager.input_path = str(absolute_path)
        self.path_manager.selected_path = None
        self.path_manager.current_path = None

        self.button_state.index = self.index
        self.button_state.control_up_button()
        self.button_state.control_select_button()
        self.button_state.control_down_button()

        self.button_state.control_back_button()
        self.button_state.control_next_button()

        self.button_state.control_settings_button()

        self.button_state.update_search_state()

        self.app_gui.path_entry.delete(self.counters['root_position'], tk.END)
        self.app_gui.path_entry.insert(self.counters['root_position'], navigation_path)

        if absolute_path.is_dir():
            self.app_render.add_slash(absolute_path)

        self.app_gui.select_button.config(text='Select')
        self.app_gui.select_window.config(selectbackground='blue')

        self.app_gui.path_entry.xview_moveto(1.0)
        self.app_gui.path_entry.focus()

        self.select_state.current_position = self.index
        self.select_state.pop_back_point()
        self.select_state.current_select()
        self.select_state.add_next_point()

    def directory_up(self) -> None:
        """Navigates to parent directory."""
        try:
            self.mdefs._mdefs_framework.mdefs_pointer('pop')

            if self.app_state.manual_input_mode:
                if not self.input_manager.input_user_path():
                    return

            if self.path_analyzer.pattern_path_detector(self.path_manager.input_path):
                self.search.add_paths()
                self.app_render.update_select_window()
                return

            if self.catalog_detector.root_directory_detector(self.path_manager.root_path, self.path_manager.input_path):
                self.app_gui.path_entry.delete(self.counters['root_position'], tk.END)
                self.button_state.update_search_state()
                return

            if not self.app_state.back_button_active:
                self.app_state.back_button_active = True

            if self.app_state.is_search_executed:
                self.reset_path()
                return

            if not self.path_analyzer.points:
                return

            self.path_analyzer.points.pop()

            parent_path = self.path_manager.root_path
            for point in self.path_analyzer.points:
                parent_path /= point

            self.index = self.select_state.index_list[-1]

            self.path_analyzer.generate_points(parent_path)
            self.path_manager.input_path = str(parent_path)
            self.path_manager.absolute_path = parent_path
            self.path_manager.selected_path = None
            self.path_manager.current_path = None
            self.search.add_paths()

            self.button_state.index = self.index

            self.select_state.current_position = self.index
            self.select_state.pop_back_point()

            self.app_render.index = self.index
            self.app_render.update_select_window()
            self.app_render.canonize_entered_path(parent_path)
        except Exception as e:
            showerror(
                title='Yellow Pather Error 005:',
                message=f'{e}',
                parent=self.root
            )

    def directory_down(self) -> None:
        """Navigates into selected directory."""
        try:
            if self.app_state.manual_input_mode:
                if not self.input_manager.input_user_path():
                    return

            if self.path_analyzer.pattern_path_detector(self.path_manager.absolute_path):
                return

            absolute_path = self.path_manager.abs_paths[self.index]
            if not self.app_perms.check_permission(absolute_path):
                return

            if not self.app_state.next_button_active:
                self.app_state.next_button_active = True

            self.mdefs._mdefs_framework.mdefs_pointer('add')

            parent_path = self.path_manager.root_path
            for point in self.path_analyzer.points:
                parent_path /= point

            self.select_position.selected_index = self.index
            self.select_position.select_position()

            relative_path = self.select_position.relative_path
            parent_path = parent_path / relative_path

            self.path_analyzer.generate_points(parent_path)
            self.path_manager.input_path = str(parent_path)
            self.path_manager.absolute_path = parent_path
            self.path_manager.selected_path = None
            self.path_manager.current_path = None
            self.search.add_paths()

            self.select_state.current_position = self.index
            self.select_state.current_select()
            self.select_state.add_next_point()

            self.index = 0

            self.button_state.index = self.index

            self.app_render.index = self.index
            self.app_render.update_select_window()
            self.app_render.canonize_entered_path(parent_path)
        except Exception as e:
            showerror(
                title='Yellow Pather Error 005:',
                message=f'{e}',
                parent=self.root
            )
