class AppState:
    """
    Manages application state across different modules.

    Tracks various boolean states for file manager and command parser
    functionality.
    """
    def __init__(self):
        """Initializes all application states to default values."""
        # FileManagerApp states
        # CommandParserInit states
        self.is_parser_active: bool = False
        self.is_string_active: bool = False
        self.root_path_detect: bool = False
        self.abs_path_reset: bool = False
        self.hide_command_message: bool = False
        self.resolve_work_main: bool = False
        self.no_message_show: bool = False
        self.control_enter_search: bool = False
        self.manual_input_mode: bool = False
        self.root_path_correct: bool = False
        self.root_path_inserted: bool = False
        self.path_not_correct: bool = False
        self.is_recursive_search: bool = False
        self.is_operation_canceled: bool = False
        self.is_search_executed: bool = False
        self.block_when_update: bool = False
        self.search_not_executed: bool = False
        self.reset_button_active: bool = False
        self.back_button_active: bool = False
        self.next_button_active: bool = False
        self.search_protect_enabled: bool = True
        self.insert_resource_name: bool = False
        self.is_root_directory: bool = True
        self.initial_search_now: bool = True
        self.toggle_button_active: bool = False
        self.search_button_active: bool = False
        self.settings_button_active: bool = False
        self.is_search_active: bool = False


class PermissionState:
    def __init__(self):
        self.hide_file_error: bool = False
        self.hide_access_error: bool = False

class SecureState:
    def __init__(self) -> None:
        self.hide_storage_error: bool = False
