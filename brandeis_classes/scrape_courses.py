import argparse
import json
import os
import random
import sys
import time
from typing import Iterable

import bs4
import requests
from termcolor import colored

from . import brandeis, constants

SEARCH_URL = "http://registrar-prod.unet.brandeis.edu/registrar/schedule/search"


def req_params(page: int, year: int, semester: str) -> dict:
    return {
        "strm": brandeis.strm(year, semester),
        "view": "all",
        "time": "time",
        "day": ["mon", "tues", "wed", "thurs", "fri", "sat", "sun"],
        "start_time": "00:00:00",
        "end_time": "23:59:59",
        "order": "class",
        "search": "Search",
        "subsequent": 1,
        "status": "",
        "block": "",
        "keywords": "",
        "page": page,
    }


def courses(start_pg, end_pg, year: int, semester: str, base_url: str = SEARCH_URL):
    for pg in range(start_pg, end_pg + 1):
        print(colored(f"\r--- Page {pg} / {end_pg} ---", attrs=["bold"]), end="")
        sys.stdout.flush()
        req = requests.get(base_url, params=req_params(pg, year, semester))
        if not req.ok:
            raise requests.exceptions.HTTPError
        print(" (Main req. fin.)")
        courses = brandeis.page_to_courses(req.text)
        for course in courses:
            course.year = year
            course.semester = semester
        yield courses
        if pg != end_pg:
            print("Sleeping...", end="")
            sys.stdout.flush()
            time.sleep(random.randint(1, 15))


def high_page(year: int, semester: str) -> int:
    req = requests.get(SEARCH_URL, params=req_params(1, year, semester))
    if not req.ok:
        raise requests.exceptions.HTTPError
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    return max(
        map(
            int,
            filter(
                str.isdigit,
                map(lambda t: t.text, soup.find_all("a", {"class": "pagenumber"})),
            ),
        )
    )


def scrape_courses(year: int, semester: str, start_page: int = 1) -> None:
    if semester not in constants.SEMESTERS:
        raise ValueError

    os.makedirs("out", exist_ok=True)

    with open(f"out/{year}-{semester}.json", "a") as out:
        out.write("[\n")
        end_page = high_page(year, semester)
        for crss in courses(start_page, end_page, year, semester):
            for i, crs in enumerate(crss):
                if i % 5 == 0 and i > 0:
                    print()
                print(crs.friendly_number, "\t", end="")
                json.dump(crs.dict(), out, indent=2)
                out.write(",\n")
            print()
        # truncate the trailing comma to prevent invalid json syntax
        out.seek(out.tell() - 2)  # DANGEROUS!!!!
        out.write("\n]\n")


def main():
    parser = argparse.ArgumentParser(
        description="Scrapes course data for a given year/semester"
    )

    parser.add_argument(
        "-s", "--start-page", type=int, default=1, help="""Start page"""
    )
    parser.add_argument("year", type=int)
    parser.add_argument("semester", choices=brandeis.constants.SEMESTERS)

    args = parser.parse_args()

    if args.year is None or args.semester is None or args.year is None:
        parser.error("Mandatory argument not given")

    scrape_courses(args.year, args.semester, args.start_page)


if __name__ == "__main__":
    main()
