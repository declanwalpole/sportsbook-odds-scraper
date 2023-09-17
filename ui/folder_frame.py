from tkinter import Frame, Label, Button, StringVar
from tkinter import filedialog
from .constants import FOLDER_FRAME_TITLE, FOLDER_BUTTON_TEXT, FOLDER_SUBMIT_BUTTON_TEXT
from .styles import small_text_style, medium_text_style, primary_button_style, ternary_button_style


class FolderFrame(Frame):
    def __init__(self, master=None, next_frame_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.next_frame_callback = next_frame_callback
        self.folder_path = ""

        self.folder_display = StringVar()

        self.instruction_label = Label(
            self, text=FOLDER_FRAME_TITLE, **medium_text_style)

        self.folder_button = Button(
            self, text=FOLDER_BUTTON_TEXT, command=self.browse_folder, **ternary_button_style)

        self.folder_display_label = Label(
            self, textvariable=self.folder_display, **small_text_style)

        self.next_button = Button(self, text=FOLDER_SUBMIT_BUTTON_TEXT,
                                  command=self.next_frame_callback, **primary_button_style)

        self.render_frame()

    def render_frame(self):
        self.instruction_label.pack(pady=(100, 50))
        self.folder_button.pack(pady=(0, 50))
        self.folder_display_label.pack(pady=(0, 50))

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.folder_display.set(self.folder_path)
            self.next_button.pack()
        else:
            self.folder_display.set("No folder selected.")
            self.next_button.pack_forget()

    def show(self):
        self.pack()

    def hide(self):
        self.pack_forget()

    def get_folder_path(self):
        return self.folder_path
