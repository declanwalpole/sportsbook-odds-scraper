from utils import extract_event_id_from_url, scrape_DK_event, preview_df_contents, write_to_csv


def scrape_event(url):
    print(f"Scraping {url}...")
    eventId = extract_event_id_from_url(url)
    (eventId, eventName, df) = scrape_DK_event(eventId)
    preview_df_contents(df)
    write_to_csv(eventId, eventName, df)
