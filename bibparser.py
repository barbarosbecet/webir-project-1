"""
WiSe 15, WebIR, Project-1, Becet, Simmet
BibParser Module
"""

from init_logging import init_logging
import logging
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *
import glob

if __name__ == "__main__":
    init_logging()
logger = logging.getLogger(__name__)


def _customizations(record):
    """
    Bibtexparser customizations that are applied to every entry found in the .bib files
    """
    record = convert_to_unicode(record)
    record = type(record)
    record = author(record)
    return record


def get_all_entries(locations):
    """
    Retrieve all the .bib files and parse their content to a list of simple dictionaries
    :param locations: locations of all the .bib files
    :return: return a list of dictionaries
    """
    result = []
    parser = BibTexParser()
    parser.customization = _customizations
    for file_location in locations:
        try:
            with open(file_location, encoding="utf-8") as bib_file:
                result.extend(bibtexparser.load(bib_file, parser=parser).entries)
        except:
            logger.error(" - ".join(".bib parsing error: ", file_location))
    return result


def main():
    """
    This is a main procedure only for testing! It shouldn't normally run!
    """
    logger.warning("This is a main procedure only for testing this module! It shouldn't normally run!")
    bib_db = get_all_entries(glob.glob("bibs/*.bib"))
    for dct in bib_db:
        try:
            print(str(dct))
        except UnicodeEncodeError as e:
            logger.error("{}: Entry with id='{}' can't be printed".format(e.reason, dct["ID"]))


if __name__ == "__main__":
    main()
