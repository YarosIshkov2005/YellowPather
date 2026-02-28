# Standard libraries
import re

# Third-party libraries
from tkinter.messagebox import showerror

# Local modules
from typing import Optional, List, Dict, Tuple, Any
from pathlib import Path


class CommandDetectorCore:
    """Class of command parser."""

    def __init__(self, root, commands) -> None:
        self.root = root
        self.MODE_COMMANDS = commands if commands is not None else ()

        self.MAX_ARGUMENTS: int = 10
        self.MIN_ARGUMENTS: int = 4

        self.KEYWORDS: Tuple[str] = ('copy', 'move', 'rename', 'to')
        self.COMMANDS: Tuple[str] = ('copy', 'move', 'rename')

        self.KEYWORD_ALIASES: Dict[str] = {
            'cp': 'copy',
            'copyto': 'copy',
            'mv': 'move',
            'moveto': 'move',
            '->': 'to',
            '>>': 'to',
            '»»': 'to',
            'into': 'to'
        }

    def tokenize_command(self, cmd: str) -> list:
        """
        Generate tokens for check.

        Args:
            cmd: User command

        Returns:
            List[str]: Tokens or empty list on error
        """
        try:
            pattern = r'("([^"]*)"|\'([^\']*)\'|(->|>>|»»|\b(?!\d)\w+\b))'
            user_data = cmd.strip()

            if not user_data:
                return []

            matches = re.findall(pattern, user_data)
            tokens = []

            for match in matches:
                full_match, double_quoted, single_quoted, unquoted = match
                if double_quoted:
                    tokens.append(double_quoted)
                elif single_quoted:
                    tokens.append(single_quoted)
                elif unquoted:
                    cleaned = re.sub(r'[^\w\->>»]', '', unquoted)
                    if cleaned and cleaned.strip():
                        tokens.append(cleaned)

            if not tokens:
                return []

            for i, token in enumerate(tokens):
                if token in self.KEYWORD_ALIASES:
                    tokens[i] = self.KEYWORD_ALIASES[token]

            arguments = len(tokens)

            if arguments >= self.MIN_ARGUMENTS and arguments <= self.MAX_ARGUMENTS:
                try:
                    has_valid_command = tokens[0] in self.COMMANDS
                    has_to_keyword = 'to' in tokens
                    to_position = tokens.index('to') if has_to_keyword else -1
                    has_sources = to_position > 1
                    has_destination = to_position < len(tokens) - 1

                    if (has_valid_command and has_to_keyword and has_sources
                            and has_destination):
                        return tokens
                    else:
                        showerror(
                            title='Yellow Pather Error 014:',
                            message=f"Invalid command structure '{user_data}'",
                            parent=self.root
                        )
                        return []
                except ValueError:
                    showerror(
                        title='Yellow Pather Error 014:',
                        message=f"Missing 'to' keyword in '{user_data}'",
                        parent=self.root
                    )
                    return []
            else:
                error_msg = (
                    f"Incomplete command: '{user_data}'. "
                    f"Requires from {self.MIN_ARGUMENTS} to {self.MAX_ARGUMENTS} "
                    f"arguments, got {arguments}"
                )
                showerror(
                    title='Yellow Pather Error 014:',
                    message=error_msg,
                    parent=self.root
                )
                return []
        except Exception as e:
            showerror(
                title='Yellow Pather Error 014:',
                message=f'Parser crash: {str(e)}',
                parent=self.root
            )
            return []

    def parse_command_structure(
        self,
        cmd: str,
        root: Path,
        paths: List[Path]
    ) -> Optional[Dict[str, Any]]:
        """
        Process commands.

        Args:
            cmd: User command
            root: Root path
            paths: Paths for work

        Returns:
            Dict with keys: command, source, destination, root, paths,
            or None in case of an error, or switching commands (cmd-parser:off)
        """
        try:
            if cmd in self.MODE_COMMANDS:
                return None

            tokens = self.tokenize_command(cmd)

            if not tokens:
                return None

            command = tokens[0]
            to_index = tokens.index('to')

            sources = tokens[1:to_index]
            destination = tokens[to_index + 1]

            root_str = str(root)
            paths_str = [str(path) for path in paths if path]

            return {
                'command': command,
                'sources': sources,
                'destination': destination,
                'root': root_str,
                'paths': paths_str
            }
        except Exception as e:
            showerror(
                title='Yellow Pather Error 014:',
                message=f'{e}',
                parent=self.root
            )
            return None
