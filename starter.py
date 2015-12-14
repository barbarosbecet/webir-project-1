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
    bib_items = bibparser.get_all_bibs("bibs/")
    my_db = database.BibDB()
    my_db.create_tables()
    my_db.fill_entries(bib_items)


def main():
    example_run()

if __name__ == "__main__":
    main()
