import tkinter as tk
from tkinter.messagebox import showerror

import os

from typing import Optional
from pathlib import Path

class CommandParserCore:
    def __init__(self, globals, callstack):
        self.globals = globals
        self.callstack = callstack

        self.root = self.globals['root']
        self.app_gui = self.callstack.app_gui
        self.app_state = self.callstack.app_state
        self.app_render = self.callstack.app_render
        self.button_state = self.callstack.button_state
        self.counters = self.globals['counters']
        self.COMMANDS = self.globals['commands']
        self.mdefs = self.callstack.framework
        self.parser = self.callstack.parser_core
        self.path_manager = self.callstack.path_manager
        self.search = self.callstack.search_manager
        self.select_position = self.callstack.select_position

        self.parser_name = 'cmd:/'

    def change_mode(self, string_path: str) -> bool:
        """
        Handles mode switching between cmd-parser:on and cmd-parser:off.

        Args:
            string_path: Current path string.

        Returns:
            True if normal mode, False if command mode active.
        """
        cmd = os.path.basename(string_path)
        if cmd == 'cmd-parser:on':
            if string_path not in self.COMMANDS:
                self.path_manager.original_path = Path(string_path).parent

        if not self.app_state.is_parser_active:
            if self.program_mode(cmd):
                self.app_state.is_string_active = True

        if self.app_state.is_string_active:
            if cmd not in self.COMMANDS:
                parse_result = self.parser.call_detector(
                    cmd, self.mdefs._mdefs_framework._pointer.catalog_path, self.path_manager.abs_paths
                )
                execute_result = self.parser.call_executer(
                    parse_result
                )
                if execute_result:
                    self.path_manager.absolute_path = self.path_manager.original_path
                    self.app_render.update_select_window()
                else:
                    if not self.app_state.hide_command_message:
                        showerror(
                            title='Yellow Pather Error 014:',
                            message=f"Command Error: Incorrect command: '{cmd}'",
                            parent=self.root
                        )
                    else:
                        self.app_state.hide_command_message = False
                    self.app_gui.path_entry.focus()
            else:
                self.parser_enable(cmd)
            return False
        return True

    def program_mode(self, cmd: str) -> Optional[bool]:
        """
        Determines program mode based on command.

        Args:
            cmd: Command string.

        Returns:
            True for cmd-parser:on mode, False for cmd-parser:off, None for other.
        """
        if cmd in self.COMMANDS:
            return cmd == 'cmd-parser:on'
        return None

    def parser_enable(self, cmd: str) -> bool:
        """
        Activates/deactivates command parser mode.

        Args:
            cmd: Command string (cmd-parser:on or cmd-parser:off).

        Returns:
            True if parser activated, False if deactivated.
        """
        if self.program_mode(cmd):
            if cmd == 'cmd-parser:on':
                if not self.app_state.is_parser_active:
                    self.app_state.is_parser_active = True

                if not self.app_state.abs_path_reset:
                    self.app_state.abs_path_reset = True

                self.app_gui.path_entry.delete(0, tk.END)
                self.app_gui.path_entry.insert(0, self.parser_name)
                self.app_gui.path_entry.config(foreground='#0000FF')
                self.app_gui.path_entry.focus()

                self.counters['root_position'] = self.app_gui.path_entry.index(tk.INSERT)
                self.counters['start_position'] = self.app_gui.path_entry.index(tk.INSERT)

                self.path_manager.absolute_path = self.path_manager.original_path

                self.app_render.update_select_window()
                self.button_state.update_search_state()

                self.select_position.select_position()
                self.path_manager.current_path = self.path_manager.absolute_path / self.select_position.relative_path

                self.button_state.control_select_button()

                self.button_state.control_back_button()
                self.button_state.control_next_button()

                self.button_state.control_settings_button()
                return True
        else:
            if cmd == 'cmd-parser:off':
                if self.app_state.is_parser_active:
                    self.app_state.is_parser_active = False
                    self.app_state.is_string_active = False

                if self.app_state.abs_path_reset:
                    self.path_manager.input_path = str(self.path_manager.original_path)
                    self.path_manager.absolute_path = self.path_manager.original_path
                    self.app_state.abs_path_reset = False

                navigation_path = str(self.path_manager.root_path)
                self.app_gui.path_entry.delete(0, tk.END)
                self.app_gui.path_entry.insert(0, navigation_path)
                self.app_gui.path_entry.config(foreground='#000000')
                self.app_gui.path_entry.focus()

                self.app_render.add_slash(navigation_path)

                self.counters['root_position'] = self.app_gui.path_entry.index(tk.INSERT)
                self.counters['start_position'] = self.app_gui.path_entry.index(tk.INSERT)

                if not self.path_manager.original_path.samefile(self.path_manager.root_path):
                    self.app_render.canonize_entered_path(self.path_manager.original_path)

                self.app_render.update_select_window()
                self.button_state.update_search_state()

                self.select_position.select_position()
                self.path_manager.current_path = self.path_manager.absolute_path / self.select_position.relative_path

                self.app_render.canonize_entered_path(self.path_manager.absolute_path)

                if self.app_state.is_recursive_search:
                    self.app_state.is_recursive_search = False

                self.button_state.control_select_button()

                self.button_state.control_back_button()
                self.button_state.control_next_button()

                self.button_state.control_settings_button()
                return False
