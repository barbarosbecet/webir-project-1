"""
WiSe 15, WebIR, Project-2, Becet, Simmet
BibParser Module
"""

from init_logging import init_logging
import logging
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode, type, author
from my_customization import editor
import glob

logger = logging.getLogger(__name__)


def _customizations(record):
    """
    Bibtexparser customizations that are applied to every entry found in the .bib files
    """
    record = convert_to_unicode(record)
    record = type(record)    # make the entry types lower-case
    record = author(record)  # split the authors into a list
    record = editor(record)  # split the editors into a list
    return record


def get_all_entries(locations):
    """
    Retrieve all the .bib files and parse their content to a list of simple dictionaries
    :param locations: locations of all the .bib files
    :return: return a list of dictionaries
    """
    result = []
    my_parser = BibTexParser()
    my_parser.customization = _customizations
    for file_location in locations:
        try:
            with open(file_location, encoding="utf-8") as bib_file:
                result.extend(bibtexparser.load(bib_file, parser=my_parser).entries)
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
    init_logging()
    main()
