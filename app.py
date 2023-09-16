from tkinter import Tk, Label, Button, Entry, filedialog, StringVar, CENTER, OptionMenu, Frame
from event_scraper import EventScraper
from datetime import datetime
import threading


class App:
    def __init__(self, root):
        self.root = root
        root.title("Odds Scraping Tool")
        root.geometry('700x700')
        # root.eval('tk::PlaceWindow . center')

        # Initialize frames
        self.disclaimer_frame = Frame(root)
        self.initial_frame = Frame(root)
        self.input_frame = Frame(root)

        # Disclaimer frame
        self.disclaimer_title = Label(
            self.disclaimer_frame,
            text="Important Information",
            font=("Helvetica", 24)
        )
        self.disclaimer_title.pack(pady=10)

        self.disclaimer_label = Label(
            self.disclaimer_frame,
            justify='left',
            text=("""
                  Disclaimer:

                  This app fetches odds information from sportsbooks.
                  The author accepts no responsibility: intellectual property of the odds remains with the sportsbooks.
                  The sportsbooks supported have not authorized the use of this tool.
                  Sportsbooks may change their site/API at any time causing this app to break.
                  Requests to sportsbook servers are made from your IP.
                  Sportsbook may block your IP from making requests at their discretion.
                  App may not work correctly if your IP location (or VPN) does not match that of the sportsbook's jurisdiction.

                  North American Sportsbooks Supported:

                  DraftKings
                  BetMGM
                  Caesars
                  BetRivers/SugarHouse
                  Pointsbet
                  Superbook
                  Bovada

                  Australian Sportsbooks Supported:

                  Sportsbet
                  TAB
                  Ladbrokes"""
                  ),
            wraplength=650
        )
        self.disclaimer_label.pack(pady=10)

        self.accept_button = Button(
            self.disclaimer_frame, text="I Accept", command=self.show_initial_frame)
        self.accept_button.pack(pady=10)

        self.disclaimer_frame.pack(pady=50)

        # Instructional header
        self.instruction_label = Label(
            self.initial_frame, text="Before we begin, select the folder in which to write csv's", font=("Helvetica", 12))
        self.instruction_label.pack(pady=(10, 50))

        self.folder_button = Button(
            self.initial_frame, text="Choose Output Directory", command=self.browse_folder)
        self.folder_button.pack()

        self.folder_path = ""
        self.folder_display = StringVar()
        self.folder_display_label = Label(
            self.initial_frame, textvariable=self.folder_display)
        self.folder_display_label.pack(pady=(10, 50))

        self.next_button = Button(
            self.initial_frame,
            text="Next",
            command=self.show_remaining_inputs,
            font=("Helvetica", 16),
            borderwidth=3,
            relief="solid",
            foreground='white',  # Text color
            background='green'  # Background color
        )

        # Initialize the scraper
        self.scraper = None

        # Remaining inputs
        self.title_label = Label(
            self.input_frame, text="Scrape Odds To Csv From Event Url", font=("Helvetica", 24))
        self.title_label.pack(pady=(10, 50))

        self.url_label = Label(self.input_frame, text="Enter URL")
        self.url_label.pack()

        self.url_entry = Entry(self.input_frame, width=70)
        self.url_entry.pack(pady=10)

        self.filename_label = Label(self.input_frame, text="Enter Filename")
        self.filename_label.pack()
        self.filename_entry = Entry(self.input_frame, width=30)
        self.filename_entry.pack(pady=10)

        self.scrape_button = Button(
            self.input_frame,
            text="Scrape",
            command=self.scrape_event,
            font=("Helvetica", 16),
            borderwidth=3,
            relief="solid",
            foreground='white',  # Text color
            background='green'  # Background color
        )
        self.scrape_button.pack(pady=(50, 10))

        self.reset_button = Button(
            self.input_frame,
            text="Clear Inputs",
            command=self.reset_fields,
            font=("Helvetica", 16),
            borderwidth=3,
            relief="solid",
            foreground='white',  # Text color
            background='red'  # Background color
        )
        self.reset_button.pack(pady=10)

        self.status_display = StringVar()
        self.status_display_label = Label(
            self.input_frame,
            textvariable=self.status_display,
            wraplength=550,
            font=("Helvetica", 16)  # Text color
        )
        self.status_display_label.pack()

        self.message_display = StringVar()
        self.message_display_label = Label(
            self.input_frame, textvariable=self.message_display, wraplength=550)
        self.message_display_label.pack()

    def show_initial_frame(self):
        self.disclaimer_frame.pack_forget()
        self.initial_frame.pack(pady=50)

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:  # Only show the "Next" button if a directory is selected
            self.folder_display.set(f"Selected Folder: {self.folder_path}")
            self.next_button.pack(pady=10)
        else:
            self.folder_display.set("No folder selected.")
            self.next_button.pack_forget()  # Hide the "Next" button if no folder is selected

    def show_remaining_inputs(self):
        self.initial_frame.pack_forget()
        self.input_frame.pack(pady=10)

    def scrape_event(self):
        self.message_display.set("")  # Reset the message
        thread = threading.Thread(target=self._scrape_event)
        thread.start()

    def _scrape_event(self):
        def update_message(msg):
            self.message_display.set(msg)

        def update_status(msg):
            self.status_display.set(msg)

        try:
            self.root.after(0, update_status, "Scraping...")
            self.root.after(0, update_message, "")
            url = self.url_entry.get().strip()
            filename = self.filename_entry.get().strip() or "odds"

            if not filename.endswith('.csv'):
                filename += '.csv'

            csv_outfile = f"{self.folder_path}/{filename}"

            self.scraper = EventScraper()

            scraping_result = self.scraper.scrape(url, csv_outfile)

            formatted_message = '\n'.join(
                [f"{k}: {v}" for k, v in scraping_result.get_summary().items()])

            self.root.after(0, update_status, "Success!")

            self.root.after(0, update_message, formatted_message)

        except Exception as e:
            self.root.after(0, update_status, f"Error")
            self.root.after(0, update_message, f"{e}")

    def reset_fields(self):
        """
        Resets the input fields, keeping the folder path.
        """
        self.url_entry.delete(0, 'end')
        self.filename_entry.delete(0, 'end')
        self.status_display.set("")
        self.message_display.set("")


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
