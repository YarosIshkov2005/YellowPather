import tkinter as tk
from tkinter.messagebox import showinfo, showerror

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
        self.canonizer = self.callstack.path_canonize
        self.mdefs = self.callstack.framework
        self.insert_manager = self.callstack.insert_manager
        self.parser = self.callstack.parser_core
        self.path_manager = self.callstack.path_manager
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

        if self.is_parser_enabled(cmd):
            return

        if not self.app_state.is_parser_active:
            if self.program_mode(cmd):
                self.app_state.is_string_active = True

        if self.app_state.is_string_active:
            if cmd not in self.COMMANDS:
                parse_result = self.parser.call_detector(
                    cmd, self.path_manager.resource_path, self.path_manager.abs_paths
                )
                execute_result = self.parser.call_executer(
                    parse_result
                )
                if execute_result:
                    self.path_manager.absolute_path = self.path_manager.original_path
                    self.canonizer.canonizer('render')
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
            if cmd == 'cmd-parser:on':
                return True
            else:
                return False
        return None

    def is_parser_enabled(self, cmd: str):
        if cmd == 'cmd-parser:on' and self.app_state.is_parser_active:
            msg = f'{self.parser_name} has already been enabled'
            showinfo(title='Message:', message=msg, parent=self.root)
            self.app_gui.path_entry.focus()
            return True
        elif cmd == 'cmd-parser:off' and not self.app_state.is_parser_active:
            msg = f'{self.parser_name} has already been disabled'
            showinfo(title='Message:', message=msg, parent=self.root)
            self.app_gui.path_entry.focus()
            return True
        return False

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
                    self.path_manager.input_path = str(self.path_manager.original_path)
                    self.path_manager.absolute_path = self.path_manager.original_path
                    self.app_state.abs_path_reset = True

                self.app_gui.path_entry.config(foreground='#0000FF')

                self.insert_manager.insert_path(self.parser_name, 0, False)
                self.insert_manager.set_positions()

                self.canonizer.canonizer('render')
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

                self.app_gui.path_entry.config(foreground='#000000')

                self.insert_manager.insert_path(self.path_manager.root_path, 0, True)
                self.insert_manager.set_positions()

                self.canonizer.canonizer('render')
                return False
