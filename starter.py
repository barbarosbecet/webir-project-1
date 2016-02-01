"""
WiSe 15, WebIR, Project-2, Becet, Simmet
Starter Module
"""

from init_logging import init_logging
import logging
import bibparser
import database
import crawler_2
import glob

logger = logging.getLogger(__name__)


def test_run_with_crawler_2():
    bib_files = crawler_2.get_file_locations(max_level=2)
    bib_items = bibparser.get_all_entries(bib_files)
    my_db = database.BibDB(db_user_name="root",
                           db_password="WebIR2015",
                           db_address="localhost",
                           db_name="bib_db",
                           verbose=False)
    my_db.create_tables()
    my_db.fill_entries(bib_items)


def test_run_without_crawling():
    bib_items = bibparser.get_all_entries(glob.glob("bibs/*.bib"))
    my_db = database.BibDB(db_user_name="root",
                           db_password="WebIR2015",
                           db_address="localhost",
                           db_name="bib_db",
                           verbose=False)
    my_db.create_tables()
    my_db.fill_entries(bib_items)


def main():
    test_run_without_crawling()
    # test_run_with_crawler_2()

if __name__ == "__main__":
    init_logging()
    main()
