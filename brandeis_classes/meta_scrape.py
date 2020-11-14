"""Scrapes course data for the given years.
"""

import argparse
import subprocess

from termcolor import colored

from . import constants, scrape_courses


def main():
    parser = argparse.ArgumentParser(
        description="Scrapes course data for the given years"
    )
    parser.add_argument("start_year", type=int)
    parser.add_argument("end_year", type=int)
    args = parser.parse_args()

    for year in range(args.start_year, args.end_year + 1):
        print(colored(f"========={year}=========", "green"))
        for semester in constants.SEMESTERS:
            print(colored(f"---------{semester}---------", "green"))
            scrape_courses.scrape_courses(year, semester)


if __name__ == "__main__":
    main()
