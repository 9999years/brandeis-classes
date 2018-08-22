from typing import List
from glob import glob
import os.path

import brandeis

COURSE_LISTS = []

def all_courses() -> List[List[brandeis.Course]]:
    global COURSE_LISTS
    if COURSE_LISTS:
        return COURSE_LISTS
    else:
        COURSE_LISTS = read_all()
        return COURSE_LISTS

def read(fname: str) -> List[brandeis.Course]:
    """for initializing COURSE_LISTS"""
    with open(fname, 'r') as f:
        return brandeis.load_courses(f)

def read_all(outdir: str = 'out') -> List[brandeis.Course]:
    """for initializing COURSE_LISTS"""

    pat = os.path.join(outdir, '*-*.json')
    ret = []
    # theyre numbered so this works
    for fname in sorted(glob(pat)):
        base, *_ = os.path.basename(fname).split(os.path.extsep)
        year, semester = base.split('-')
        if semester == '2':
            # summer
            continue
        ret.append(read(fname))

    return ret

def courses_per_semester() -> List[int]:
    return list(map(len, all_courses()))

def main():
    print(courses_per_semester())

if __name__ == '__main__':
    main()
