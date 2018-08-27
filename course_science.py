from typing import List, Mapping
from glob import glob
import os.path
from collections import Counter
import itertools

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
            # semester = '01'
            pass
        elif semester == '2':
            # skip summer
            continue
        elif semester == '3':
            # september
            # semester = '09'
            pass
        else:
            raise ValueError('Invalid semester number ' + semester)
        ret[f'{year}-{semester}'] = read(fname)

    return ret

def display_semester(sem) -> str:
    yr, sem = sem.split('-')
    sem = {
            '1': 'Spring',
            '3': 'Fall',
        }[sem]
    return f'{yr} {sem}'

def total_courses_per_subject():
    ret = {}
    for courses in all_courses().values():
        for course in courses:
            if course.subject not in ret:
                ret[course.subject] = 0
            ret[course.subject] += 1
    return ret


def courses_per_subject():
    ret = {}
    for sem, courses in all_courses().items():
        ret[sem] = Counter(map(lambda c: c.subject, courses))

    return ret

def courses_per_semester(subj=None) -> List[int]:
    ret = {}
    for sem, courses in all_courses().items():
        if subj is not None:
            courses = list(filter(lambda c: c.subject == subj, courses))
        ret[sem] = len(courses)
    return ret

def students_per_semester(subj=None) -> List[int]:
    ret = {}
    for sem, courses in all_courses().items():
        if subj is not None:
            courses = list(filter(lambda c: c.subject == subj, courses))
        ret[sem] = sum(map(lambda c: c.enrolled, courses))
    return ret

def students_per_class():
    total_courses = []
    for sem, courses in all_courses().items():
        total_courses.extend(courses)
    ret = {}
    for subj in brandeis.constants.SUBJECTS:
        subj_courses = list(
                filter(lambda e: e > 0,
                map(lambda c: c.enrolled,
                filter(lambda c: c.subject == subj, total_courses))))
        if subj_courses:
            ret[subj] = sum(subj_courses) / len(subj_courses)
    return ret

def sorted_dict(d):
    return [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]

def printdict(d):
    i = 0
    print('[')
    for sem, dat in d.items():
        i += 1
        sem = format(repr(display_semester(sem)), '13')
        print('[', sem, ',', dat, '],')
    print(']')

def main():
    # corr = courses_per_semester()
    # for sem, dat in courses_per_semester('COSI').items():
        # corr[sem] = dat / corr[sem]
    print(*map(lambda x: f'{x[0]} | {x[1]}],', students_per_class().items()), sep='\n')
    # print(*sorted_dict(students_per_class()['2018-3']), sep='\n')
    # print(sorted(set(map(lambda c: c.subject, itertools.chain(*all_courses().values())))))
    # subjects = total_courses_per_subject()
    # subjects = [(k, subjects[k]) for k in sorted(subjects, key=subjects.get, reverse=True)]
    # print(*[s[0] for s in subjects if s[1] > 500], sep='\n')
    # for sem, courses in courses_per_subject().items():
        # print(sem, ':', courses.most_common(5))

if __name__ == '__main__':
    main()
