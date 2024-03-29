"""
Scrape data to get coursework info from DataCamp, Pluralsight and other sources.
"""

import csv
import argparse
import requests
import logging

from tqdm import tqdm
import tldextract
from bs4 import BeautifulSoup

logger = logging.getLogger('logger')

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

    parser.add_argument("--file", "-f", type=str, default="urls.txt",
                        help="Enter filename which contains line separated URLS")
    parser.add_argument("--lang", "-l", type=str, default="Python",
                        help="Enter language of coursework of the input URLs")
    parser.add_argument("--out", "-o", type=str, default="data/dataset.csv",
                        help="Enter a name for the generated dataset")
    parser.add_argument("--medium", "--m", choices=[True, False],
                        help="Build a corpus of articles from Medium")

    return parser

def extract_datacamp(url: str = None, lang: str = None, medium: str = None,
                     _type: str = None) -> dict:
    if not url:
        logger.error("URL not passed")
        return

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        title = soup.find("meta", property="og:title")['content']
<<<<<<< HEAD
        short_description = soup.find("meta", attrs={"name": "description"})['content']
        long_description = soup.find("p", class_="course__description").text
=======
        description = soup.find("p", class_="course__description").text
>>>>>>> 5dc7f185674913408ad9c1118f1598371c1e648c
        time = soup.find("li", class_="header-hero__stat--hours").text
    
        coursetracks = soup.find_all("li", class_="course__track")
        prereq = soup.find_all("li", class_="course__prerequisite")

        path_string = ",".join(item.text.strip() for item in coursetracks)
        prereq_string = ",".join(item.text.strip() for item in prereq)
    except AttributeError:
        # inconsistencies in DataCamp HTML DOM
        logger.info(url)
        logger.debug("Look into HTML DOM for given URL")
        return {}

    info = {
        "title": title.strip(),
<<<<<<< HEAD
        "short_description": short_description.strip(),
        "long_description": long_description.strip().replace("\n", ""),
=======
        "description": description.strip().replace("\n", ""),
>>>>>>> 5dc7f185674913408ad9c1118f1598371c1e648c
        "provider": "DataCamp",
        "url": url,
        "time": time.strip(),
        "language": lang,
        "paths": path_string,
        "prerequisites": prereq_string,
        "medium": medium,
        "type": _type
    }

    return info

def write(output: str = None, res: list = None) -> None:
    with open(output, 'w') as csvfile:
        fields = ['title', 'short_description', 'long_description', 'provider', 'url',
                  'time', 'language', 'paths', 'prerequisites', 'medium', 'type']
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        writer.writeheader()
        for item in res:
            writer.writerow(item)

def run(args: argparse.Namespace) -> list:
    """
    Use BeautifulSoup to extract info from passed URL and generate a
    .csv dataset file.
    """

    infile = args.file
    lang = args.lang

    with open(infile, 'r') as f:
        lines = f.readlines()
    
    logger.info("Parsing URL HTML using BeautifulSoup")
    results = []

    for line in tqdm(lines):
        URL = line.strip()
        root = tldextract.extract(URL)

        if root.domain == "datacamp":
            info = extract_datacamp(URL, lang=lang, medium="video", _type="course")
            results.append(info)
    
    return results


if __name__ == "__main__":
    parser = argument_parser()
    args = parser.parse_args()
    res = run(args)
    write(args.out, res)