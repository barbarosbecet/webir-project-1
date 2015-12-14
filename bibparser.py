"""
WiSe 15, WebIR, Project-1, Becet, Simmet
BibParser Module
"""

from init_logging import init_logging
import logging
import bibtexparser
from bibtexparser.customization import *
import glob

if __name__ == "__main__":
    init_logging()
logger = logging.getLogger(__name__)


def _customizations(record):
    """
    Bibtexparser customizations that are applied to every entry found in the .bib files
    """
    record = homogeneize_latex_encoding(record)
    return record


def get_all_bibs(locations):
    """
    Retrieve all the .bib files and parse their content to a list of simple dictionaries
    :param location: directory with .bib files
    :return: return a list of dictionaries
    """
    result = []
    for file_location in locations:
        with open(file_location, encoding="utf-8") as bib_file:
            result.extend(bibtexparser.load(bib_file).entries)
    return result


def main():
    """
    This is a main procedure only for testing! It shouldn't normally run!
    """
    logger.warning("This is a main procedure only for testing this module! It shouldn't normally run!")
    bib_db = get_all_bibs("test_bib/")
    for dct in bib_db:
        print(dct)


if __name__ == "__main__":
    main()
