from tkinter import Frame, Label, Button
from .constants import DISCLAIMER_TITLE, DISCLAIMER_TEXT, DISCLAIMER_BUTTON_TEXT
from .styles import large_text_style, small_text_style, primary_button_style


class DisclaimerFrame(Frame):
    def __init__(self, master=None, next_frame_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.next_frame_callback = next_frame_callback

        self.title = Label(self, text=DISCLAIMER_TITLE, **large_text_style)
        self.disclaimer_label = Label(
            self, text=DISCLAIMER_TEXT, justify='left', **small_text_style)
        self.accept_button = Button(self, text=DISCLAIMER_BUTTON_TEXT,
                                    command=self.next_frame_callback, **primary_button_style)

        self.render_frame()

    def render_frame(self):
        self.title.pack(pady=(10, 50))
        self.disclaimer_label.pack(pady=(0, 50))
        self.accept_button.pack(pady=(0, 0))

    def show(self):
        self.pack(pady=50)

    def hide(self):
        self.pack_forget()
