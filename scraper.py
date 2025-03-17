from options import Options
from scraper_exceptions import ScraperException
from theposterdb_scraper import ThePosterDBScraper
from mediux_scraper import MediuxScraper
from notifications import debug_me
from urllib.parse import urlparse

class Scraper:

    """
    A class to scrape one of the supported providers

    Attributes:
        url (str): The URL to scrape

    Methods:
        set_options():          A way to pass in the scrape options (either from the CLI, in a line of the bulk file, or in the GUI)
        scrape():               Decides which scraper to use
        scrape_theposterdb():   Scrapes The Poster DB (theposterdb.com)
        scrape_mediux():        Scrapes MediUX (mediux.pro)
        scrape_html():          Scrapes a local HTML file using the Poster DB scraper
    """

    def __init__(self, url):
        self.url = url
        self.options = Options()
        self.movie_artwork = []
        self.tv_artwork = []
        self.collection_artwork = []
        self.source = None
        self.title = None

        # Set source based on the contents of the URL
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        if host == "theposterdb.com":
            self.source = "theposterdb"
        elif host == "mediux.pro" and "sets" in url:
            self.source = "mediux"
        elif ".html" in url:
            self.source = "html"


    # Set options - otherwise will use defaults of False
    def set_options(self, options):
        self.options = options


    def scrape(self):

        """
        Runs the correct scraper based on the source of the URL (as set in the __init__ function)

        Returns:
            None
        """
        try:
            debug_me(f"Scraping from {self.source}")
            if self.source == "theposterdb":
                self.scrape_theposterdb()
            elif self.source == "mediux":
                self.scrape_mediux()
            elif self.source == "html":
                return self.scrape_html()
            else:
                raise ScraperException(f"Invalid source provided ({self.source if self.source else 'empty source'})")
        except Exception as e:
            raise

    def scrape_theposterdb(self):
        try:
            theposterdb_scraper = ThePosterDBScraper(self.url)
            theposterdb_scraper.set_options(self.options)
            theposterdb_scraper.scrape()

            self.title = theposterdb_scraper.title
            self.movie_artwork = theposterdb_scraper.movie_artwork
            self.tv_artwork = theposterdb_scraper.tv_artwork
            self.collection_artwork = theposterdb_scraper.collection_artwork

        except ScraperException as scraper_exception:
            raise
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")


    def scrape_mediux(self):

        """
        Scrape mediux.pro - this could be anything from a backdrop, posters or episode cards

        Returns:
            list: movie_artwork
            list: tv_artwork
            list: collection_artwork
        """

        try:

            mediux_scraper = MediuxScraper(self.url)
            mediux_scraper.set_options(self.options)
            mediux_scraper.scrape()

            self.title = mediux_scraper.title
            self.movie_artwork = mediux_scraper.movie_artwork
            self.tv_artwork = mediux_scraper.tv_artwork
            self.collection_artwork = mediux_scraper.collection_artwork

        except ScraperException:
            raise
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")


    def scrape_html(self):

        """
        Scrapes a local HTML file.  Not sure what this option is actually used for!

        I'm guessing it was a saved page used so that TPDb wasn't hammered during
        development, but we'll keep it for posterity

        Returns:
            None
        """

        self.scrape_theposterdb()

