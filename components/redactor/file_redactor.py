import traceback
import tkinter as tk
from tkinter.messagebox import showinfo, showerror, askyesno

from functools import lru_cache
from charset_normalizer import from_bytes
from PIL import Image, ImageTk

class FileRedactorCore:
    def __init__(self, globals, redactor) -> None:
        self.globals = globals
        self.redactor = redactor

        self.root = self.globals['root']
        self.app_gui = self.redactor.app_gui
        self.app_render = self.redactor.app_render
        self.path_manager = self.redactor.path_manager
        self.settings = self.redactor.settings

        self.settings_window = None
        self.redactor_window = None
        
        self.icons_path = None
        self.icon_image = None
        self.file_path = None
        
        self.icon_paths = {}
        self.file_extensions = self.globals['extensions']
        
        self.ICON_FILES = {
            'Unknown': 'unknown_icon.png',
            'BIN': 'bin_icon.png',
            'C': 'clang_icon.png',
            'C++': 'cpp_icon.png',
            'C#': 'csharp_icon.png',
            'CSS': 'css_icon.png',
            'CSV': 'csv_icon.png',
            'DOC': 'doc_icon.png',
            'DOCX': 'docx_icon.png',
            'ENC': 'enc_icon.png',
            'HTML': 'html_icon.png',
            'Java': 'java_icon.png',
            'JavaScript': 'js_icon.png',
            'JAR': 'jar_icon.png',
            'JSON': 'json_icon.png',
            'Kotlin': 'kotlin_icon.png',
            'LOG': 'log_icon.png',
            'PDF': 'pdf_icon.png',
            'Python': 'python_icon.png',
            'TXT': 'text_icon.png',
            'XML': 'xml_icon.png'
        }

        self._redactor_gui = self.redactor_gui
        self._redactor_events = self.redactor_events

    @property
    @lru_cache(maxsize=None)
    def redactor_gui(self):
        from core.gui.redactor.redactor_gui import RedactorGUI
        return RedactorGUI(file_redactor=self)

    @property
    @lru_cache(maxsize=None)
    def redactor_events(self):
        from core.events.redactor.redactor_events import RedactorEvents
        return RedactorEvents(file_redactor=self, redactor_gui=self._redactor_gui)
        
    def create_window(self, window) -> None:
        if self.redactor_window and self.redactor_window.winfo_exists():
            self.redactor_window.lift()
            return
        
        self.redactor_window = tk.Toplevel(window)
        self.redactor_window.title('File Redactor')
        self.redactor_window.resizable(False, False)
        
        self.redactor_window.transient(window)
        self.redactor_window.grab_set()
        
        self.redactor_window.protocol('WM_DELETE_WINDOW', self.close_window)
        
        self._redactor_gui.redactor_window = self.redactor_window
        self._redactor_gui.widgets_container()
        self._redactor_gui.create_widgets()
        self._redactor_events.bind_events()
        self.load_icon_images()

    def control_clear_button(self, event=None):
        current_text = self._redactor_gui.text_widget.get(1.0, tk.END)
        if len(current_text) > 1:
            self._redactor_gui.clear_button.config(state='normal')
        else:
            self._redactor_gui.clear_button.config(state='disabled')
                
    def load_icon_images(self):
        try:
            for image in self.icons_path.iterdir():
                image_name = image.name
                image_path = str(image)
                if not image_path.startswith('.') and image_path.endswith('.png'):
                    self.icon_paths[image_name] = image
        except Exception as e:
            error_msg = f"""Load icon error: {str(e)}\n\n{traceback.format_exc()}"""
            showerror(title='Error:', message=error_msg, parent=self.redactor_window)
        
    def set_icon_image(self):
        try:
            icon_text = ''
            error_text = ''
            lang_name = ''
            encoding = ''

            languages = self.file_extensions.get('languages', None)
            if languages is None:
                icon_text = '?'
                error_text = 'Unknown'
                
            text_files = self.file_extensions.get('text', None)
            if text_files is None:
                error_text = 'Unknown'
                
            others = self.file_extensions.get('others', None)
            if others is None:
                error_text = 'Unknown'
                
            error_icon = self.icon_paths.get('unknown_icon.png', None)
            if error_icon is None:
                error_text = 'Unknown'
            
            file_suffix = self.file_path.suffix
            if file_suffix not in languages:
                if error_icon is None:
                    self._redactor_gui.icon_label.config(text=icon_text)
                    self._redactor_gui.lang_label.config(text=error_text)

            if file_suffix in languages:
                lang_name = languages.get(f'{file_suffix}', None)
            elif file_suffix in text_files:
                lang_name = text_files.get(f'{file_suffix}', None)
            else:
                lang_name = others.get(f'{file_suffix}', None)
                
            if lang_name is None:
                lang_name = 'Unknown'
                        
            icon_name = self.ICON_FILES.get(lang_name, None)
            icon_path = self.icon_paths.get(icon_name, 'Unknown_icon.png')
            
            open_icon = Image.open(icon_path)
            resize_icon = open_icon.resize((150, 150), Image.LANCZOS)
            self.icon_image = ImageTk.PhotoImage(resize_icon)
            self._redactor_gui.icon_label.config(image=self.icon_image)
            
            self._redactor_gui.lang_label.config(text=f'language / file: {lang_name}')
            
            file_name = self.file_path.name            
            self._redactor_gui.file_label.config(text=f'name: {file_name}')

            encoding = self.encode_detector(self.file_path)
                                
            self._redactor_gui.code_label.config(text=f'encoding: {encoding}')
            self.load_file_data(self.file_path, encoding)
        except Exception as e:
            error_msg = f"""Load icon image error: {str(e)}\n\n{traceback.format_exc()}"""
            showerror(title='Error:', message=error_msg, parent=self.redactor_window)

    def encode_detector(self, file_path):
        with open(file_path, 'rb') as file:
            data = file.read(10240)
                
            result = from_bytes(data)
            if result:
                encoding = result.best().encoding
            else:        
                encoding = 'utf-8'
                
            return encoding
        
    def read_file_data(self, file_path, encoding):
        try:
            if file_path.suffix == '.bin':
                with open(file_path, 'rb') as file:
                    return file.read()
                    
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                    return file.read()
            except Exception as e:
                error_msg = f'Cannot read file with any encoding {str(e)}\n\n{traceback.format_exc()}'
                showerror(title='Yellow Pather Error 010:', message=error_msg, parent=self.redactor_window)
                return 'No data loaded.'
        except Exception as e:
            error_msg = f"""Read data error: {str(e)}\n\n{traceback.format_exc()}"""
            showerror(title='Yellow Pather Error 010:', message=error_msg, parent=self.redactor_window)
            return 'No data loaded.'
                        
    def load_file_data(self, file_path, encoding):
        try:
            if file_path is None:
                return

            self._redactor_gui.text_widget.delete(1.0, tk.END)
                
            data = self.read_file_data(file_path, encoding)
            if not data:
                showerror(
                    title='Yellow Pather Error 010:',
                    message='File Error: failed to load data. Try changing the file encoding',
                    parent=self.redactor_window
                )
                return
            self._redactor_gui.text_widget.insert(tk.END, data)
        except Exception as e:
            error_msg = f"""Read data error: {str(e)}\n\n{traceback.format_exc()}"""
            showerror(title='Yellow Pather Error 010:', message=error_msg, parent=self.redactor_window)

    def clear_file_data(self):
        self._redactor_gui.text_widget.delete(1.0, tk.END)
        self.control_clear_button()

    def save_file_data(self):
        try:
            current_text = self._redactor_gui.text_widget.get(1.0, tk.END)
            if len(current_text) <= 1:
                info_msg = f"""Null file '{self.file_path.name}' will be deleted\n\nClear file data?"""
                result = askyesno(
                    title='Null file:', 
                    message=info_msg, 
                    parent=self.redactor_window
                )
                if not result:
                    return
                
                self.file_path.unlink(missing_ok=True)
                showinfo(
                    title='File deleted:',
                    message=f"'{self.file_path.name}' deleted",
                    parent=self.redactor_window
                )
                self.file_path = None
                self.path_manager.selected_path = None

                self.settings.control_open_button()
                self.settings._settings_manager.type_count = 0
                self.settings._settings_manager.select_create_type()

                if self.app_gui.select_button.cget('text') == 'Drop':
                    self.app_gui.select_button.config(text='Select')

                self.app_render.update_select_window()
                self.close_window()
                return

            encoding = self.encode_detector(self.file_path)

            try:
                if self.file_path.suffix == '.bin':
                    with open(self.file_path, 'wb') as file:
                        file.write(current_text)
                    
                with open(self.file_path, 'w', encoding=encoding) as file:
                    file.write(current_text)
            except Exception as e:
                showerror(
                    title='Yellow Pather Error 004:', 
                    message=f"Permission Error: '{e}'",
                    parent=self.redactor_window
                )
                return
                
            showinfo(
                title='File saved:',
                message=f"'{self.file_path.name}' saved",
                parent=self.redactor_window
            )

            self.app_render.update_select_window()

            self.path_manager.absolute_path = self.file_path.parent

        except Exception as e:
            error_msg = f"""Delete error: {str(e)}\n\n{traceback.format_exc()}"""
            showerror(title='Yellow Pather Error 010:', message=error_msg, parent=self.redactor_window)
                                
    def close_window(self) -> None:
        if self.redactor_window and self.redactor_window.winfo_exists():
            self.redactor_window.grab_release()
            self.redactor_window.destroy()
            self.redactor_window = None

        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.grab_set()
            self.settings_window.lift()
            self.settings_window.focus_force()
        elif self.root.winfo_exists():
            self.root.lift()
            self.root.focus_force()
            self.app_gui.path_entry.focus()
