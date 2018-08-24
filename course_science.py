from typing import List, Mapping
from glob import glob
import os.path
from collections import Counter

import brandeis

COURSES = {}

def all_courses() -> Mapping[str, List[brandeis.Course]]:
    global COURSES
    if COURSES:
        return COURSES
    else:
        COURSES = read_all()
        return COURSES

def read(fname: str) -> List[brandeis.Course]:
    """for initializing COURSES"""
    with open(fname, 'r') as f:
        return brandeis.load_courses(f)

def read_all(outdir: str = 'out') -> List[brandeis.Course]:
    """for initializing COURSES"""

    pat = os.path.join(outdir, '*-*.json')
    ret = {}
    # theyre numbered so this works
    for fname in sorted(glob(pat)):
        base, *_ = os.path.basename(fname).split(os.path.extsep)
        year, semester = base.split('-')
        if semester == '1':
            # january
            semester = '01'
        elif semester == '2':
            # skip summer
            continue
        elif semester == '3':
            # september
            semester = '09'
        else:
            raise ValueError('Invalid semester number ' + semester)
        ret[f'{year}-{semester}'] = read(fname)

    return ret

def courses_per_subject():
    ret = {}
    for sem, courses in all_courses().items():
        ret[sem] = Counter(map(lambda c: c.subject, courses))

    return ret

def courses_per_semester() -> List[int]:
    return list(map(len, all_courses()))

def main():
    for sem, courses in courses_per_subject().items():
        print(sem, ':', courses.most_common(5))

if __name__ == '__main__':
    main()
