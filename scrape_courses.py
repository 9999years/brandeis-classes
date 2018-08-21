import argparse
import time
import random
import json
from typing import Iterable

import requests
from termcolor import colored

import brandeis

def courses(pages: Iterable[int], year: int, semester: str,
        base_url: str = 'http://registrar-prod.unet.brandeis.edu/registrar/schedule/search'):
    params = {
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
            'page': 1
        }

    for pg in pages:
        print(colored('--- Page ' + str(pg) + ' ---', attrs=['bold']))
        params['page'] = pg
        req = requests.get(base_url, params=params)
        if not req.ok:
            raise requests.exceptions.HTTPError
        print('--- Main req. fin. ---')
        courses = brandeis.page_to_courses(req.text)
        for course in courses:
            course.year = year
            course.semester = semester
        yield courses
        time.sleep(random.randint(1, 15))

def main():
    parser = argparse.ArgumentParser(description='batch downloads course info')

    parser.add_argument('-s', '--start-page', type=int,
            help='''Start page''')
    parser.add_argument('-p', '--page', type=int,
            help='''High page count, inclusive''')
    parser.add_argument('-o', '--out', type=argparse.FileType('a'),
            help='''JSON output file''')
    parser.add_argument('-e', '--semester', choices=brandeis.constants.SEMESTERS)
    parser.add_argument('-y', '--year', type=int)

    args = parser.parse_args()

    if args.page is None or args.year is None or args.semester is None or args.year is None:
        parser.error('Mandatory argument not given')

    for crss in courses(range(args.start_page, args.page + 1), args.year, args.semester):
        for crs in crss:
            print(
                    colored('\t' + crs.friendly_number, 'green', attrs=['bold']),
                    crs.name,
                    colored('(' + crs.instructor + ')', 'cyan') if crs.instructor else '',
                    colored(crs.uni_reqs_str, attrs=['dark']),
                    )
            json.dump(crs.dict(), args.out, indent=2)

if __name__ == '__main__':
    main()
