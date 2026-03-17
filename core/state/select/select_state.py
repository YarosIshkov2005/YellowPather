from typing import List

class SelectPosition:
    def __init__(self, callstack) -> None:
        self.callstack = callstack
        
        self.app_gui = self.callstack.app_gui

        self.index: int = 0
        self.reset: int = 0
        self.current_position: int = 0
        self.index_list: List[str] = []

    def current_select(self):
        self.index = self.current_position

    def pop_back_point(self):
        if self.index_list:
            self.index_list.pop()

            if len(self.index_list) >= 1:
                self.current_position = self.index_list[-1]

    def add_next_point(self):
        self.current_position = self.reset
        self.index_list.append(self.index)

    def reset_points(self):
        if self.index_list:
            self.index_list.clear()
            self.current_select()
            self.add_next_point()
