"""
WiSe 15, WebIR, Project-1, Becet, Simmet
BibParser Module
"""

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *
import glob
import logging
import logging.config


logger = logging.getLogger(__name__)


def init_logging():
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s %(funcName)s:%(lineno)d: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'WARNING',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': 'WARNING',
                'formatter': 'standard',
                'propagate': True
            }
        }
    })


def _customizations(record):
    record = homogeneize_latex_encoding(record)
    return record


def get_all_bibs(location):
    result = []
    for file_location in glob.glob("".join(location+"*.bib")):
        with open(file_location, encoding="utf-8") as bib_file:
            my_parser = BibTexParser()
            my_parser.customization = _customizations
            result.extend(bibtexparser.load(bib_file,).entries)
    return result


def main():
    """
        This is a main procedure only for testing! It shouldn't normally run
    """
    init_logging()
    bib_db = get_all_bibs("test_bib/")
    print(bib_db)


if __name__ == "__main__":
    main()
