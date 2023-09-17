from tkinter import Frame, Label, Button, StringVar
from tkinter import filedialog

from constants import FOLDER_FRAME_TITLE, FOLDER_BUTTON_TEXT, FOLDER_SUBMIT_BUTTON_TEXT


class FolderFrame(Frame):
    def __init__(self, master=None, next_frame_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.next_frame_callback = next_frame_callback
        self.folder_path = ""

        self.folder_display = StringVar()

        self.instruction_label = Label(
            self,
            text=FOLDER_FRAME_TITLE,
            font=("Helvetica", 12)
        )
        self.instruction_label.pack(pady=(10, 50))

        self.folder_button = Button(
            self,
            text=FOLDER_BUTTON_TEXT,
            command=self.browse_folder
        )
        self.folder_button.pack()

        self.folder_display_label = Label(
            self,
            textvariable=self.folder_display
        )
        self.folder_display_label.pack(pady=(10, 50))

        self.next_button = Button(
            self,
            text=FOLDER_SUBMIT_BUTTON_TEXT,
            command=self.next_frame_callback,
            font=("Helvetica", 16),
            borderwidth=3,
            relief="solid",
            foreground='white',
            background='green'
        )

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.folder_display.set(f"Selected Folder: {self.folder_path}")
            self.next_button.pack(pady=10)
        else:
            self.folder_display.set("No folder selected.")
            self.next_button.pack_forget()

    def show(self):
        self.pack(pady=50)

    def hide(self):
        self.pack_forget()

    def get_folder_path(self):
        return self.folder_path
