from tkinter.messagebox import showerror

from pathlib import Path
from typing import List

class CommandParserCore:
    """
    Command parser initialization class.

    Manages command parser module loading and directory structure
    for command parsing functionality.
    """

    def __init__(self, globals, callstack) -> None:
        """Initializes CommandParserInit with managers."""
        self.globals = globals
        self.callstack = callstack

        self.root = self.globals['root']
        self.command_detector = self.callstack.command_detector
        self.command_executer = self.callstack.command_executer

    def load_resources(self, parent_path: Path) -> None:
        """Creates command parser directory structure."""
        if not self.command_detector:
            showerror(
                title='Yellow Pather Error 001:',
                message='Import Error: Failed to import command parser modules',
                parent=self.root
            )
        if not self.command_executer:
            showerror(
                title='Yellow Pather Error 001:',
                message='Import Error: Failed to import command parser modules',
                parent=self.root
            )

    def call_detector(self, cmd: str, root: Path, paths: List[Path]) -> bool:
        """
        Calls command detector module.

        Args:
            cmd: Command string to parse.
            root: Root window.
            paths: Available paths for command.

        Returns:
            True if command detection successful.
        """
        if not self.command_detector:
            self.show_error()
            return False
            
        if not hasattr(self, 'command_detector'):
            self.show_error()
            return

        return self.command_detector.parse_command_structure(cmd, root, paths)

    def call_executer(self, parameters: str) -> bool:
        """
        Calls command executor module.

        Args:
            parameters: Command parameters to execute.

        Returns:
            True if command execution successful.
        """
        if not self.command_executer:
            self.show_error()
            return False

        if not hasattr(self, 'command_executer'):
            self.show_error()
            return False

        return self.command_executer.command_executer(parameters)

    def show_error(self):
        """Shows module not found error."""
        showerror(
            title='Yellow Pather Error 015:',
            message="Module Error: The operation was canceled. The module was not found",
            parent=self.root
        )
