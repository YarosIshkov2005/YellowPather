import traceback
from functools import wraps
from tkinter.messagebox import showerror

class ErrorHandler:
    def __init__(self):
        pass
                
    #Метод обработки ошибок:
    @staticmethod
    def handle_errors(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                showerror(
                    title='Error:',
                    message=f'{func.__name__}: {traceback.format_exc()}'
                )
                return None
        return wrapper
