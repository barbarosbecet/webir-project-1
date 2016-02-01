"""
WiSe 15, WebIR, Project-2, Becet, Simmet
Crawler Module
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
from urllib.error import URLError
from os.path import abspath
from init_logging import init_logging
import logging
import re
import sys
from urllib.parse import urljoin
from geturl import get_url_list
from validateurl import url_is_http
from validateurl import url_is_relative


biblist = []
file_locations = []
download_counter = 0
links_watched = 0

if __name__ == "__main__":
    init_logging()
logger = logging.getLogger(__name__)

DEPTH_LEVEL_CHARACTER = '*'


def exit_error(error, error_code):
    """
    exit_error function prints an error and exit with the specified error code

    Keyword arguments:
    error -- The error to print on the screen
    error_code -- The error_code returned by the program

    """
    print("")
    print(error)
    print("")
    sys.exit(error_code)


def bib_download(urls,instant = False):
    """
    Downloading of the specified Bib URLs either for instant use or not

    Keyword arguments:
    urls -- An array of urls or a single url to download
    instant -- if true it will download only one file for instant use
    """
    global download_counter
    if instant == False:
        locations = []
        for item in range(len(urls)):
            try:
                response = urlopen(urls[item])
            except URLError as e:
                logger.error("URL/HTTP error @ {} : {}".format(urls[item], e))
            else:
                if response.getcode() == 200 and urls[item].endswith(".bib"):
                    logger.info("Downloading file @ {}".format(urls[item]))
                    urlretrieve(urls[item], "./bibs/bib_%i.bib" % download_counter)
                    logger.info("File saved @ {}".format(abspath("./bibs/bib_%i.bib" % download_counter)))
                    locations.append("{}".format(abspath("./bibs/bib_%i.bib" % download_counter)))
                    download_counter = download_counter +1
                elif response.getcode() == 200 and urls[item].endswith(".bib.gz"):
                    logger.info("Downloading file @ {}".format(urls[item]))
                    urlretrieve(urls[item], "./bibs/bib_%i.bib.gz" % download_counter)
                    logger.info("File saved @ {}".format(abspath("./bibs/bib_%i.bib.gz" % download_counter)))
                    locations.append("{}".format(abspath("./bibs/bib_%i.bib.gz" % download_counter)))
                    download_counter = download_counter +1
                else:
                    logger.error("No bib file found at given URL, download aborted! @ {}".format(urls[item]))
        return locations
    else:
        location = []
        url = urls
        try:
            response = urlopen(url)
        except URLError as e:
            logger.error("URL/HTTP error @ {} : {}".format(url, e))
            return None
        else:
            if response.getcode() == 200 and url.endswith(".bib"):
                logger.info("Downloading file @ {}".format(url))
                urlretrieve(url, "./bibs/bib_%i.bib" % download_counter)
                logger.info("File saved @ {}".format(abspath("./bibs/bib_%i.bib" % download_counter)))
                location.append("{}".format(abspath("./bibs/bib_%i.bib" % download_counter)))
                download_counter = download_counter +1
            elif response.getcode() == 200 and url.endswith(".bib.gz"):
                logger.info("Downloading file @ {}".format(url))
                urlretrieve(url, "./bibs/bib_%i.bib.gz" % download_counter)
                logger.info("File saved @ {}".format(abspath("./bibs/bib_%i.bib.gz" % download_counter)))
                location.append("{}".format(abspath("./bibs/bib_%i.bib.gz" % download_counter)))
                download_counter = download_counter +1
            else:
                logger.error("No bib file found at given URL, download aborted! @ {}".format(url))
                return None
        return location[0]


def bib_crawl(url, max_level=2, dInstant=False):
    """
    Receives a URL and a specified crawling depth and a download flag. It will crawl for bib files until the specified
    deepness. If dInstant is true this files will be download right away.

    Keyword arguments:
    url -- A string with the URL to analyze
    max_level -- The maximum depth of crawling for bib files
    dInstant -- if true it will download the files right away

    """
    if not url_is_http(url):
        exit_error("ERROR: URL provided must have HTTP/HTTPS scheme", 1)
    else:
        # First print all the child links of the URL
        get_child_list(url, 1, dInstant)

        # Print level 2 links and recursive among their links until reach maximum level
        recursive_bib_crawl(url, 2, max_level, dInstant)


def recursive_bib_crawl(url, depth, max_level, dInstant):
    """
    Recursive function that crawl at level of depth,
    and if the max_level has not been reached, continues analyzing to the
    next level.

    Keyword arguments:
    url -- A string with the URL to analyze
    depth -- The current crawling depth
    max_level -- The maximum depth of crawling
    """

    url_list2 = []
    url_list = get_url_list(url)

    for l in url_list:
        if url_is_http(l):
            url_list2.append(l)
        # elif url_is_relative(l):
        elif True:
            url_list2.append(urljoin(url, l))

    if depth <= max_level:
        for l in url_list2:
            get_child_list(l, depth, dInstant)

        for l in url_list2:
            recursive_bib_crawl(l, depth+1, max_level, dInstant)


def get_child_list(url, depth, dInstant):
    """
    Function to get all the links contained in a url, together with a
    series of characters indicating the depth level of the link
    being printed

    Keyword arguments:
    url -- The URL to analyze
    depth -- The crawling depth being analyzed, needed for printing stuff
    """
    bibtmp = []
    url_list = get_url_list(url)
    global file_locations
    global links_watched

    if dInstant == False:
        for l in url_list:
            if url_is_http(l):
                if l.endswith(".bib") or l.endswith(".bib.gz"):
                    biblist.append(l)
                    bibtmp.append(l)
            elif True:
                if l.endswith(".bib") or l.endswith(".bib.gz"):
                    biblist.append(urljoin(url, l))
                    bibtmp.append(urljoin(url, l))
            links_watched = links_watched +1
    else:
        for l in url_list:
            if url_is_http(l):
                if l.endswith(".bib") or l.endswith(".bib.gz"):
                    file_locations.append(bib_download(l, True))
                    bibtmp.append(l)
            elif True:
                if l.endswith(".bib") or l.endswith(".bib.gz"):
                    file_locations.append(bib_download(urljoin(url, l), True))
                    bibtmp.append(urljoin(url, l))
            links_watched = links_watched +1
        logger.info("Links watched in total: %i" % links_watched)

    """
    for l in url_list2:
        print_depth_point(depth)
        print(" %s" % (l))
    """

    for l in bibtmp:
        print_depth_point(depth)
        print(" %s" % l)


def print_depth_point(depth):
    """
    Function to print as many 'level characters'. Default character is '*'

    Keyword arguments:
    depth -- The amount of 'depth level characters' to print
    """

    counter = 0
    while counter < depth:
        sys.stdout.write(DEPTH_LEVEL_CHARACTER)
        sys.stdout.flush()
        counter += 1


def get_file_locations(max_level = 2, dInstant = False):
    """
    Starts the process with the specified level deepness and returns a list of the locations of the bib files.By the
    parameter dInstant is defined if the founded bib files should be download right away or after the crawling is done.

    Keyword arguments:
    max_level -- The maximum depth of crawling for bib files
    dInstant -- if true it will download the files right away
    """
    global file_locations

    with open("seeds.txt") as f:
        urls = f.readlines()
    for l in range(len(urls)):
        bib_crawl(urls[l], max_level, dInstant)
    if dInstant == False:
        file_locations = bib_download(biblist)
        logger.info("Links watched in total: %i" % links_watched)

    return file_locations


def main():
    global links_watched

    file_locations = get_file_locations(2, False)
    print(file_locations)


if __name__ == "__main__":
    main()
