from tkinter import Tk
from event_scraper import EventScraper
from scraper_exception import ScraperException
from ui.disclaimer_frame import DisclaimerFrame
from ui.folder_frame import FolderFrame
from ui.input_output_frame import InputOutputFrame


class App:
    TITLE = "Odds Scraping Tool"
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 700

    def __init__(self, root):
        self.root = root
        self.set_title()
        self.center_window()

        # Initialize the scraper
        self.scraper = None

        # Initialize frames
        self.disclaimer_frame = DisclaimerFrame(root, self.show_folder_frame)
        self.folder_frame = FolderFrame(root, self.show_input_output)
        self.input_output_frame = InputOutputFrame(root, self.scrape_event)

        self.render_frames()

    def set_title(self):
        self.root.title(self.TITLE)

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        center_x = int((screen_width / 2) - (self.WINDOW_WIDTH / 2))
        center_y = int((screen_height / 2) - (self.WINDOW_HEIGHT / 2))

        self.root.geometry(
            f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{center_x}+{center_y}")

    def render_frames(self):
        self.disclaimer_frame.show()

    def show_folder_frame(self):
        self.disclaimer_frame.hide()
        self.folder_frame.show()

    def show_input_output(self):
        self.folder_frame.hide()
        folder_path = self.folder_frame.get_folder_path()
        self.input_output_frame.set_folder_name(folder_path)
        self.input_output_frame.show()

    def scrape_event(self, url, filename, folder_name):

        try:
            if not filename.endswith('.csv'):
                filename += '.csv'

            csv_outfile = f"{folder_name}/{filename}"

            self.scraper = EventScraper()

            self.scraper.scrape(url, csv_outfile)

            formatted_message = '\n'.join(
                [f"{k}: {v}" for k, v in self.scraper.get_summary().items()])

            return {'status': "Success!", 'message': formatted_message}

        except ScraperException as exception:
            return {'status': "Error!", 'message': exception}


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
