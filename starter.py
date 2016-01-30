"""
WiSe 15, WebIR, Project-1, Becet, Simmet
Starter Module
"""

from init_logging import init_logging
import logging
import bibparser
import database
import crawler

if __name__ == "__main__":
    init_logging()
logger = logging.getLogger(__name__)


def example_run():
    """
    An example (should be) working run...
    """
    bib_files = crawler.getFileLocations(max_level=2)
    bib_items = bibparser.get_all_entries(bib_files)
    my_db = database.BibDB(db_user_name="root",
                           db_password="WebIR2015",
                           db_address="localhost",
                           db_name="bib_db",
                           verbose=False)
    my_db.create_tables()
    my_db.fill_entries(bib_items)


def main():
    example_run()

if __name__ == "__main__":
    main()
