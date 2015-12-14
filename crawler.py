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
    with urlopen(url) as response:
        bs = BeautifulSoup(response, "html.parser")
        for lnk in bs.find("body").findAll("a"):
            if "href" in lnk.attrs:
                links.append(lnk.attrs["href"])
    return links


def crawl(urls, level=1):

    links = []
    all_links = [[], []]
    for url in range(len(urls)):
        with urlopen(urls[url]) as response:
            bs = BeautifulSoup(response, "html.parser")
            for lnk in bs.find("body").findAll("a", href=re.compile(".*bib$")):
                if "href" in lnk.attrs:
                    links.append(lnk.attrs["href"])
        all_links[0].extend(get_links(urls[url]))

        # belongs to the hop
        for lvl in range(1, level):
            for ins in range(len(all_links[lvl-1])):
                all_links_tmp = []
                all_links_tmp.extend(get_links(all_links[lvl-1][ins]))
            all_links[lvl-1].extend(all_links_tmp)

    # hop !! problem is that sometimes only half links are stored or just trash
    for lvl in range(1, level):
        for ln in range(1, len(all_links[lvl])):
            with urlopen(all_links[lvl][ln]) as response:
                bs = BeautifulSoup(response, "html.parser")
                for lnk in bs.find("body").findAll("a", href=re.compile(".*bib$")):
                    if "href" in lnk.attrs:
                        links.append(lnk.attrs["href"])

    return links



def main():


    logging.basicConfig(format="%(levelname)s - '%(message)s'", level=logging.INFO)
    urls = []
    urls.append("http://www.ims.uni-stuttgart.de/institut/mitarbeiter/seeker/")
    urls.append("http://www.isg.uni-konstanz.de/publications/")
    # urls.append("http://www.informatik.uni-konstanz.de/cvia/publications/")
    # add more urls here

    # naked_url needed for some pages, have to be known
    # all_links = crawl(start_url, naked_url)
    all_bib_links = crawl(urls)
    file_locations = bib_download(all_bib_links);
    print(file_locations)


if __name__ == "__main__":
    main()
