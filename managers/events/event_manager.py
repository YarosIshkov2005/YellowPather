class EventManager:
    def __init__(self, callstack) -> None:
        self.callstack = callstack

        self.canonizer = self.callstack.path_canonize

    def update_select_window(self):
        self.canonizer.canonizer('render')
        print('#')
