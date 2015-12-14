"""
WiSe 15, WebIR, Project-1, Becet, Simmet
Crawler Module
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
from urllib.error import URLError
from os.path import abspath
import logging
import re


def bib_download(urls):
    locations = []
    for item in range(len(urls)):
        try:
            response = urlopen(urls[item])
        except URLError as e:
            logging.error("URL/HTTP error @ {} : {}".format(urls[item], e))
            return None
        else:
            if response.status == 200 and urls[item].endswith(".bib"):
                logging.info("Downloading file @ {}".format(urls[item]))
                urlretrieve(urls[item], "./bibs/bib_%i.bib" %item)
                logging.info("File saved @ {}".format(abspath("bib_%i.bib" %item)))
                locations.append("{}".format(abspath("bib_%i.bib" %item)))
            else:
                logging.error("No bib file found at given URL, download aborted! @ {}".format(urls[item]))
    return locations


def get_links(url):
    links = []
    try:
        response = urlopen(url)
    except ValueError as e:
        logging.error("URL/HTTP error @ {} : {}".format(url, e))
        return None
    except URLError as e:
            logging.error("URL/HTTP error @ {} : {}".format(url, e))
            return None
    else:
        if response.status == 200:
            bs = BeautifulSoup(response, "html.parser")
            for lnk in bs.findAll("a"):
                if "href" in lnk.attrs:
                    links.append(lnk.attrs["href"])

    return links


def crawl(urls, level=1):

    links = []
    all_links = [[], []]
    for url in range(len(urls)):
        with urlopen(urls[url]) as response:
            bs = BeautifulSoup(response, "html.parser")
            for lnk in bs.findAll("a", href=re.compile(".*bib$")):
                if "href" in lnk.attrs:
                    links.append(lnk.attrs["href"])
        all_links[0] = get_links(urls[url])

        # belongs to the hop
        for lvl in range(1, level):
            for ins in range(len(all_links[lvl-1])):
                all_links_tmp = []
                all_links_tmp = get_links(all_links[lvl-1][ins])
            all_links[lvl-1] = all_links_tmp

    # hop !! problem is that sometimes only half links are stored or even just trash or nothing for that exception in opening
    for lvl in range(1, level):
        for ln in range(1, len(all_links[lvl])):
            with urlopen(all_links[lvl][ln]) as response:
                bs = BeautifulSoup(response, "html.parser")
                for lnk in bs.findAll("a", href=re.compile(".*bib$")):
                    if "href" in lnk.attrs:
                        links.append(lnk.attrs["href"])

    return links


def getFileLocations():
    with open("seeds.txt") as f:
        urls = f.readlines()

    all_bib_links = crawl(urls,2)
    file_locations = bib_download(all_bib_links);

    return file_locations

def main():


    logging.basicConfig(format="%(levelname)s - '%(message)s'", level=logging.INFO)
    with open("seeds.txt") as f:
        urls = f.readlines()

    # naked_url needed for some pages, have to be known
    # all_links = crawl(start_url, naked_url)
    all_bib_links = crawl(urls,2)
    file_locations = bib_download(all_bib_links);
    # print(file_locations)


if __name__ == "__main__":
    main()
