class ScraperException(Exception):
    SERVER_ERROR = "Server-side HTTP error when hitting the sportsbook's API: the sportsbook's service is acting up. Retry later."
    FORBIDDEN_ERROR = "Forbidden HTTP error: the request we made to the sportsbook was denied. Unlikely that retrying (on same IP) will resolve the issue."
    CLIENT_ERROR = "Bad Request/Not Found HTTP error: the request we made to the sportsbook was invalid. Double check the URL. If this is occurring repeatedly for one sportsbook, potentially their site has changed."
    CONNECTION_ERROR = "Connection error encountered when trying to request sportsbook's API. Check your internet connection."
    TIMEOUT_ERROR = "Request sportsbook's API timed out."
    UNEXPECTED_HTTP_ERROR = "Unexpected HTTP error when hitting the sportsbook's API: Status code {status_code}"
    UNEXPECTED_REQUEST_ERROR = "Unexpected error when hitting the sportsbook's API: {ex}"
    ODDS_PARSING_ERROR = "The request to the API was successful, but we were unable to parse odds from the response. If the match is live, perhaps all markets were suspended? If this is occurring repeatedly for one sportsbook, potentially their site has changed."
    INVALID_URL_ERROR = "URL input is not a valid website URL"

    def __init__(self, message_template, *args, **kwargs):
        message = message_template.format(*args, **kwargs)
        super().__init__(message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.args[0]}"
