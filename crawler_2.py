"""
WiSe 15, WebIR, Project-1, Becet, Simmet
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

if __name__ == "__main__":
    init_logging()
logger = logging.getLogger(__name__)

DEPTH_LEVEL_CHARACTER = '*'


def exit_error(error, error_code):
    """
    exit_error function prints an error and exit with code specified

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
    Downloading of the specified Bib URLs
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


def print_links_to_level(url, max_depth=2, dInstant=False):
    """
    arsespyder main function. Receives a URL and the crawling depth
    and prints on screen the links of the url, the links of the links
    of the url, etc. up to the max_depth

    Keyword arguments:
    url -- A string with the URL to analyze
    max_depth -- The maximum depth of link analysis

    """
    if not url_is_http(url):
        exit_error("ERROR: URL provided must have HTTP/HTTPS scheme", 1)
    else:
        # First print all the child links (links on the URL)
        print_child_list(url, 1, dInstant)

        # Print level 2 links and recursive among their links until reach
        # maximum depth
        recursive_analyze_links(url, 2, max_depth, dInstant)


def recursive_analyze_links(url, depth, max_depth, dInstant):
    url_list2 = []
    """
    Recursive function that prints the links of the url and at level depth,
    and if the max_depth has not been reached, continues analyzing to the
    next level

    Keyword arguments:
    url -- A string with the URL to analyze
    depth -- The crawling depth being analyzed
    max_depth -- The maximum depth of link analysis

    """

    url_list = get_url_list(url)

    for l in url_list:
        if url_is_http(l):
            url_list2.append(l)
        # elif url_is_relative(l):
        elif True:
            url_list2.append(urljoin(url, l))

    if depth <= max_depth:
        for l in url_list2:
            print_child_list(l, depth, dInstant)

        for l in url_list2:
            recursive_analyze_links(l, depth+1, max_depth, dInstant)


def print_child_list(url, depth, dInstant):
    """
    Function to print all the links contained in a url, together with a
    series of characters indicating the depth level of the link
    being printed

    Keyword arguments:
    url -- A string with the URL to analyze
    depth -- The crawling depth being analyzed, needed for printing stuff

    """
    bibtmp = []
    url_list = get_url_list(url)
    global file_locations

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
    Starts the process with the specified level deepness and returns a list of the locations of the bib files.
    """
    global file_locations

    with open("seeds.txt") as f:
        urls = f.readlines()

    print_links_to_level(urls[0], max_level, dInstant)
    if dInstant == False:
        file_locations = bib_download(biblist)

    return file_locations


def main():
    """
    with open("seeds.txt") as f:
        urls = f.readlines()

    print_links_to_level(urls[0], 2);

    file_locations = bib_download(biblist);
    print(file_locations)
    """

    file_locations = get_file_locations(2, False)
    print(file_locations)

if __name__ == "__main__":
    main()
