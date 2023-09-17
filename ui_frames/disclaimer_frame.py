from tkinter import Frame, Label, Button
from constants import DISCLAIMER_TITLE, DISCLAIMER_TEXT, DISCLAIMER_BUTTON_TEXT


class DisclaimerFrame(Frame):

    def __init__(self, master=None, next_frame_callback=None, **kwargs):

        super().__init__(master, **kwargs)

        self.master = master
        self.next_frame_callback = next_frame_callback

        self.title = Label(
            self,
            text=DISCLAIMER_TITLE,
            font=("Helvetica", 24)
        )
        self.title.pack(pady=10)

        self.disclaimer_label = Label(
            self,
            justify='left',
            text=(DISCLAIMER_TEXT),
            wraplength=650
        )
        self.disclaimer_label.pack(pady=10)

        self.accept_button = Button(
            self,
            text=DISCLAIMER_BUTTON_TEXT,
            command=self.next_frame_callback)
        self.accept_button.pack(pady=10)

    def show(self):
        self.pack(pady=50)

    def hide(self):
        self.pack_forget()
