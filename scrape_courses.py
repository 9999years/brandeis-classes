import argparse
import time
import random
import json
from typing import Iterable

import requests
from termcolor import colored
import bs4

import brandeis

SEARCH_URL = 'http://registrar-prod.unet.brandeis.edu/registrar/schedule/search'

def req_params(page: int, year: int, semester: str) -> dict:
    return {
            'strm': brandeis.strm(year, semester),
            'view': 'all',
            'time': 'time',
            'day': ['mon', 'tues', 'wed', 'thurs', 'fri', 'sat', 'sun'],
            'start_time': '00:00:00',
            'end_time': '23:59:59',
            'order': 'class',
            'search': 'Search',
            'subsequent': 1,
            'status': '',
            'block': '',
            'keywords': '',
            'page': page
        }

def courses(pages: Iterable[int], year: int, semester: str,
        base_url: str = SEARCH_URL):
    for pg in pages:
        print(colored('--- Page ' + str(pg) + ' ---', attrs=['bold']))
        req = requests.get(base_url, params=req_params(pg, year, semester))
        if not req.ok:
            raise requests.exceptions.HTTPError
        print('--- Main req. fin. ---')
        courses = brandeis.page_to_courses(req.text)
        for course in courses:
            course.year = year
            course.semester = semester
        yield courses
        time.sleep(random.randint(1, 15))

def high_page(year: int, semester: str) -> int:
    req = requests.get(SEARCH_URL, params=req_params(1, year, semester))
    if not req.ok:
        raise requests.exceptions.HTTPError
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    return max(map(int, filter(str.isdigit, map(lambda t: t.text,
            soup.find_all('a', {'class': 'pagenumber'})
        ))))

def main():
    parser = argparse.ArgumentParser(description='batch downloads course info')

    parser.add_argument('-s', '--start-page', type=int,
            help='''Start page''')
    parser.add_argument('-o', '--out', type=argparse.FileType('a'),
            help='''JSON output file''')
    parser.add_argument('-e', '--semester', choices=brandeis.constants.SEMESTERS)
    parser.add_argument('-y', '--year', type=int)

    args = parser.parse_args()

    if args.year is None or args.semester is None or args.year is None:
        parser.error('Mandatory argument not given')

    args.out.write('[\n')
    for crss in courses(
            range(args.start_page, high_page(args.year, args.semester)),
            args.year, args.semester):
        for crs in crss:
            print(
                    colored('\t' + crs.friendly_number, 'green', attrs=['bold']),
                    crs.name,
                    colored('(' + crs.instructor + ')', 'cyan') if crs.instructor else '',
                    colored(crs.uni_reqs_str, attrs=['dark']),
                    )
            json.dump(crs.dict(), args.out, indent=2)
            args.out.write(',\n')
    args.out.write('\n]')

if __name__ == '__main__':
    main()
