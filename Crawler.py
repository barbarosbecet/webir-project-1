""" WiSe 15, WebIR, Project Crawler, Becet, Simmet"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


def get_links(url):
    links = []
    with urlopen(url) as response:
        bs = BeautifulSoup(response, "html.parser")
        for lnk in bs.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
            if "href" in lnk.attrs:
                links.append(lnk.attrs["href"])
    return links


def crawl(start_url, naked_url, level=1):
    visited_links = []
    all_links = [[], []]
    all_links[0].append(start_url)
    all_links[1] = get_links(start_url)
    for lvl in range(1, level):
        all_links.append([])
        for lnk in all_links[lvl]:
            if lnk not in visited_links:
                visited_links.append([lnk])
                all_links[lvl+1].extend(get_links(naked_url+lnk))
    return all_links


def get_formatted_string(content):
    result = "level; link_URL\n"
    for lvl in range(len(content)):
        for lnk in content[lvl]:
            result += "{} ; {}\n".format(lvl, lnk)
    return result


def write_to_csv(content, file_name):
    with open(file_name, "w") as file:
        file.write(get_formatted_string(content))


def main():
    start_url = "https://de.wikipedia.org/wiki/Wikipedia:Hauptseite"
    naked_url = "https://de.wikipedia.org"
    all_links = crawl(start_url, naked_url)
    print(all_links[0])
    print(all_links[1])
    # print(all_links[2])
    write_to_csv(all_links, "links.csv")


if __name__ == "__main__":
    main()
