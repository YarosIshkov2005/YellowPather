import os

import tkinter as tk
from tkinter.messagebox import showerror

from pathlib import Path
from typing import List

import traceback

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
        self.counters = self.globals['insert']
        self.canonizer = self.callstack.path_canonize
        self.catalog_detector = self.callstack.catalog_detector
        self.input_manager = self.callstack.input_manager
        self.path_manager = self.callstack.path_manager
        self.path_analyzer = self.callstack.path_analyzer
        self.mdefs = self.callstack.framework
        self.search = self.callstack.search_manager
        self.select_state = self.callstack.select_state
        self.secure_manager = self.callstack.secure_manager
        self.select_position = self.callstack.select_position
        self.reset_manager = self.callstack.reset_manager
        self.update_positions = self.callstack.update_positions

    def marker_up(self):
        """Moves the selector up one item."""
        current = self.globals['positions']['index']
        if current > 0:
            self.app_gui.select_window.select_clear(current)
            current -= 1
        else:
            return

        if not self.app_state.toggle_button_active:
            self.app_state.toggle_button_active = True

        self.globals['positions']['index'] = current
        self.canonizer.canonizer('current')

    def marker_select(self, event=None):
        """Highlights or removes the selected item: Select/Drop."""
        current = self.globals['positions']['index']
        selected_path = None
            
        if self.path_manager.abs_paths:
            selected_path = self.path_manager.abs_paths[current]
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
        current = self.globals['positions']['index']
        if current < len(self.path_manager.short_names) -1:
            self.app_gui.select_window.select_clear(current)            
            current += 1
        else:
            return

        if not self.app_state.toggle_button_active:
            self.app_state.toggle_button_active = True

        self.globals['positions']['index'] = current
        self.canonizer.canonizer('current')

    def select_path(self, event=None):
        current = self.globals['positions']['index']
        selected_incide = self.app_gui.select_window.curselection()
        if selected_incide:
            current = selected_incide[0]

        if not self.app_state.toggle_button_active:
            self.app_state.toggle_button_active = True

        self.globals['positions']['index'] = current
        self.canonizer.canonizer('current')

    def reset_path(self):
        self.reset_manager.reset_path()
        if not self.app_state.is_parser_active:
            self.canonizer.canonizer('render')

    def directory_up(self) -> None:
        """Navigates to parent directory."""
        try:
            if self.app_state.manual_input_mode:
                if not self.input_manager.input_user_path():
                    return

            if self.path_analyzer.pattern_path_detector(self.path_manager.input_path):
                self.canonizer.canonizer('render')
                return

            if self.catalog_detector.root_directory_detector(
                self.path_manager.root_path, self.path_manager.input_path):
                self.app_gui.path_entry.delete(self.counters['root_position'], tk.END)
                self.button_state.update_search_state()
                return

            if not self.app_state.back_button_active:
                self.app_state.back_button_active = True
            self.canonizer.canonizer('render')
        except Exception as e:
            showerror(
                title='Yellow Pather Error 005:',
                message=f'{traceback.format_exc()}',
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

            if not self.app_state.next_button_active:
                self.app_state.next_button_active = True

            if self.app_state.is_root_directory:
                self.app_state.is_root_directory = False

            self.canonizer.canonizer('render')
        except Exception as e:
            showerror(
                title='Yellow Pather Error 005:',
                message=f'{traceback.format_exc()}',
                parent=self.root
            )
