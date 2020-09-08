"""
Scrape data to get coursework info from DataCamp, Pluralsight and other sources.
"""

import csv
import argparse
import requests
import logging

import tldextract
from bs4 import BeautifulSoup

def argument_parser(epilog: str = None) -> argparse.ArgumentParser:
    """
    Create an argument parser for accepting course urls(single or from files)
    from DataCamp and generate corresponding dataset.

    Limited to using a file for each language, as external learning sources
    don't expose language of instruction on website.
    """

    parser = argparse.ArgumentParser(epilog=epilog or f"""
    Example:
        python generate.py --file URLFILE.txt --o DATASET.csv
    """)

    parser.add_argument("--file", "-f", type=str,
                        help="Enter filename which contains line separated URLS")
    parser.add_argument("--lang", "-l", type=str, default="Python",
                        help="Enter language of coursework of the input URLs")
    parser.add_argument("--out", "-o", type=str, default="data/dataset.csv",
                        help="Enter a name for the generated dataset")

    args = parser.parse_args()
    return args

def extract_datacamp(url: str = None, lang: str = None, medium: str = None,
                     _type: str = None) -> dict:
    if not url:
        logger.error("URL not passed")
        return

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        title = soup.find("meta", property="og:title")['content']
        description = soup.find("meta", attrs={"name": "description"})['content']
        time = soup.find("li", class_="header-hero__stat--hours").text
    
        coursetracks = soup.find_all("li", class_="course__track")

        paths = []
        for item in coursetracks:
            paths.append(item.text.strip())

        path_string = ",".join(item for item in paths)
    except AttributeError:
        # inconsistencies in DataCamp HTML DOM
        logger.info(url)
        logger.debug("Look into HTML DOM for given URL")
        return {}

    info = {
        "title": title.strip(),
        "description": description.strip(),
        "provider": "DataCamp",
        "url": url,
        "time": time.strip(),
        "language": lang,
        "paths": path_string,
        "medium": medium,
        "type": _type
    }

    return info

def run(args: argparse.Namespace) -> None:
    """
    Use BeautifulSoup to extract info from passed URL and generate a
    .csv dataset file.
    """

    infile = args.file
    outfile = args.out
    lang = args.lang

    with open(infile, 'r') as f:
        lines = f.readlines()
    
    logger.info("Parsing URL HTML using BeautifulSoup")
    results = []

    for line in lines:
        URL = line.strip()
        root = tldextract.extract(URL)

        if root.domain == "datacamp":
            info = extract_datacamp(URL, lang=lang, medium="video", _type="course")
            results.append(info)

    with open(outfile, 'w') as csvfile:
        fields = ['title', 'description', 'provider', 'url', 'time', 'language',
                  'paths', 'medium', 'type']
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        writer.writeheader()
        for item in results:
            writer.writerow(item)


if __name__ == "__main__":
    logger = logging.getLogger('logger')
    args = argument_parser()
    run(args)