class SelectPosition:
    def __init__(self, globals) -> None:
        self.globals = globals

    def pop_back_point(self):
        if len(self.globals['select']['points']) == 1:
            return self.globals['select']['points'][0]

        if self.globals['select']['points']:
            self.globals['select']['points'].pop()
            return self.globals['select']['points'][-1]

    def add_next_point(self, index: int = 0):
        self.globals['select']['points'].append(index)

    def reset_points(self):
        if self.globals['select']['points']:
            self.globals['select']['points'].clear()
            self.add_next_point(0)
