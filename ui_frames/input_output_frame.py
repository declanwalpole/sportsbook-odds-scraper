from tkinter import Frame, Label, Entry, Button, StringVar
from constants import INPUT_OUTPUT_TITLE, URL_INSTRUCTION, FILENAME_INSTRUCTION, SCRAPE_BUTTON_TEXT, RESET_BUTTON_TEXT


class InputOutputFrame(Frame):
    def __init__(self, master=None, scrape_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.scrape_callback = scrape_callback
        self.folder_name = ""

        self.status_display = StringVar()
        self.message_display = StringVar()

        self.title_label = Label(
            self,
            text=INPUT_OUTPUT_TITLE,
            font=("Helvetica", 24))
        self.title_label.pack(pady=(10, 50))

        self.url_label = Label(self, text=URL_INSTRUCTION)
        self.url_label.pack()

        self.url_entry = Entry(self, width=70)
        self.url_entry.pack(pady=10)

        self.filename_label = Label(
            self, text=FILENAME_INSTRUCTION)
        self.filename_label.pack()

        self.filename_entry = Entry(self, width=30)
        self.filename_entry.pack(pady=10)

        self.scrape_button = Button(
            self,
            text=SCRAPE_BUTTON_TEXT,
            command=self.scrape_event,
            font=("Helvetica", 16),
            borderwidth=3,
            relief="solid",
            foreground='white',
            background='green'
        )
        self.scrape_button.pack(pady=(50, 10))

        self.reset_button = Button(
            self,
            text=RESET_BUTTON_TEXT,
            command=self.reset_fields,
            font=("Helvetica", 16),
            borderwidth=3,
            relief="solid",
            foreground='white',
            background='red'
        )
        self.reset_button.pack(pady=10)

        self.status_display_label = Label(
            self, textvariable=self.status_display, wraplength=550, font=("Helvetica", 16))
        self.status_display_label.pack()

        self.message_display_label = Label(
            self, textvariable=self.message_display, wraplength=550)
        self.message_display_label.pack()

    def scrape_event(self):
        url = self.url_entry.get().strip()
        filename = self.filename_entry.get().strip() or "odds"
        folder_name = self.folder_name

        self.update_status("Scraping...")
        self.update_message("")

        # delay so that the UI can immediately update status and message without getting blocked
        self.master.after(100, self.run_scrape, url, filename, folder_name)

    def run_scrape(self, url, filename, folder_name):
        try:
            scrape_result = self.scrape_callback(url, filename, folder_name)
            self.update_status(scrape_result.get('status'))
            self.update_message(scrape_result.get('message'))
        except Exception as e:
            self.update_status("Error")
            self.update_message(str(e))

    def reset_fields(self):
        self.url_entry.delete(0, 'end')
        self.filename_entry.delete(0, 'end')
        self.status_display.set("")
        self.message_display.set("")

    def update_status(self, msg):
        self.status_display.set(msg)

    def update_message(self, msg):
        self.message_display.set(msg)

    def show(self):
        self.pack(pady=10)

    def hide(self):
        self.pack_forget()

    def set_folder_name(self, folder_name):
        self.folder_name = folder_name
