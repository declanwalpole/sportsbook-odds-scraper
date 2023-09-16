from tkinter import Tk, Label, Button, Entry, filedialog, StringVar, CENTER, OptionMenu, Frame
from event_scraper import EventScraper
from datetime import datetime
import threading


class App:
    def __init__(self, root):
        self.root = root
        root.title("Odds Scraping Tool")
        root.geometry('600x400')
        root.eval('tk::PlaceWindow . center')

        # Initialize the scraper
        self.scraper = None
        self.input_frame = Frame(root)

        self.initial_frame = Frame(root)
        self.initial_frame.pack(pady=50)

        # Instructional header
        self.instruction_label = Label(
            self.initial_frame, text="Before we begin, select the folder in which to write csv's", font=("Helvetica", 12))
        self.instruction_label.pack(pady=10)

        self.folder_button = Button(
            self.initial_frame, text="Choose Output Directory", command=self.browse_folder)
        self.folder_button.pack()

        self.folder_path = ""
        self.folder_display = StringVar()
        self.folder_display_label = Label(
            self.initial_frame, textvariable=self.folder_display)
        self.folder_display_label.pack()

        self.next_button = Button(
            self.initial_frame, text="Next", command=self.show_remaining_inputs)
        self.next_button.pack()

        # Remaining inputs
        self.title_label = Label(
            self.input_frame, text="Write Betting Event Odds To Csv From Url", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.sportsbook_label = Label(
            self.input_frame, text="Select Sportsbook")
        self.sportsbook_label.pack()
        self.selected_sportsbook = StringVar(root)
        self.selected_sportsbook.set("Select")
        self.sportsbook_menu = OptionMenu(self.input_frame, self.selected_sportsbook, *[
                                          "draftkings", "betmgm", "betrivers", "bovada", "caesars", "ladbrokes", "pointsbet", "sportsbet", "superbook", "tab"])
        self.sportsbook_menu.pack()

        self.url_label = Label(self.input_frame, text="Enter URL")
        self.url_label.pack()
        self.url_entry = Entry(self.input_frame, width=70)
        self.url_entry.pack()

        self.filename_label = Label(self.input_frame, text="Enter Filename")
        self.filename_label.pack()
        self.filename_entry = Entry(self.input_frame, width=30)
        self.filename_entry.pack()

        self.scrape_button = Button(
            self.input_frame, text="Scrape", command=self.scrape_event)
        self.scrape_button.pack()

        self.reset_button = Button(
            self.input_frame, text="Clear Inputs", command=self.reset_fields)
        self.reset_button.pack()

        self.message_display = StringVar()
        self.message_display_label = Label(
            self.input_frame, textvariable=self.message_display, wraplength=400)
        self.message_display_label.pack()

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:  # Only show the "Next" button if a directory is selected
            self.folder_display.set(f"Selected Folder: {self.folder_path}")
            self.next_button.pack()

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

        try:
            self.root.after(0, update_message, "Scraping...")
            url = self.url_entry.get().strip()
            filename = self.filename_entry.get().strip() or "odds"

            if not filename.endswith('.csv'):
                filename += '.csv'

            csv_outfile = f"{self.folder_path}/{filename}"

            self.scraper = EventScraper()

            scraping_result = self.scraper.scrape(url, csv_outfile)

            formatted_message = '\n'.join(
                [f"{k}: {v}" for k, v in scraping_result.get_summary().items()])

            self.root.after(0, update_message,
                            "Success!\n" + formatted_message)

        except Exception as e:
            self.root.after(0, update_message, f"Error: {e}")

    def reset_fields(self):
        """
        Resets the input fields, keeping the folder path.
        """
        self.selected_sportsbook.set("Select")
        self.url_entry.delete(0, 'end')
        self.filename_entry.delete(0, 'end')
        self.message_display.set("")


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
