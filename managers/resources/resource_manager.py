class ResourceManager:
    def __init__(self, perms_state, app_perms) -> None:
        self.perms_state = perms_state
        self.app_perms = app_perms

    def is_resource_exists(self, check_path):
        if not self.perms_state.hide_file_error:
            self.perms_state.hide_file_error = True

        if not self.app_perms.path_not_exists(check_path):
            if self.perms_state.hide_file_error:
                self.perms_state.hide_file_error = False
            return True

        if self.perms_state.hide_file_error:
            self.perms_state.hide_file_error = False
        return False

    def is_resource_file(self, check_path):
        if not self.perms_state.hide_file_error:
            self.perms_state.hide_file_error = True

        if self.app_perms.path_is_file(check_path):
            if self.perms_state.hide_file_error:
                self.perms_state.hide_file_error = False
            return True

        if self.perms_state.hide_file_error:
            self.perms_state.hide_file_error = False
        return False

    def is_resource_permitted(self, check_path):
        if not self.perms_state.hide_access_error:
            self.perms_state.hide_access_error = True

        if self.app_perms.check_perms(check_path):
            if self.perms_state.hide_access_error:
                self.perms_state.hide_access_error = False
            return True

        if self.perms_state.hide_access_error:
            self.perms_state.hide_access_error = False
        return False
