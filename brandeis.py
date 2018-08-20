from dataclasses import dataclass
from typing import Iterable, List
from collections import namedtuple
import itertools
import re

import requests
import bs4

Requirement = namedtuple('Requirement', ['abbr', 'long_name'])

UNI_REQS = { 'CA', 'FL', 'HUM', 'NW', 'OC', 'PE-1', 'QR', 'SN', 'SS', 'UWS', 'WI', }

LONG_REQ_NAMES = {
            'CA':   'School of Creative Arts',
            'FL':   'Foreign Language Requirement',
            'HUM':  'School of Humanities',
            'NW':   'Non-Western and Comparative Studies',
            'OC':   'Oral Communication',
            'PE-1': 'Physical Education 1 Course',
            'QR':   'Quantitative Reasoning Requirement',
            'SN':   'School of Science',
            'SS':   'School of Social Science',
            'UWS':  'University Writing Seminar',
            'WI':   'Writing Intensive',
        }

@dataclass
class CourseTime:
    block: str = None
    times: str = None
    location: str = None
    info: str = None

@dataclass
class Course:
    # e.g. Modal, Temporal, and Spatial Logic for Language
    name: str
    # e.g. 16903; registration number for sage
    class_number: int

    # subject, number, and group form parts of the course's "display name"
    # an example is COSI 118A_1, where the trailing "1" is a section number and
    # is discarded
    # e.g. COSI
    subject: str
    # e.g. 118
    number: int
    # e.g. a, b, c, ...
    group: str

    # weirdly formatted; maybe consistent? parsing this is a job for later
    schedule: Iterable[CourseTime]

    # enrollment
    enrolled: int
    limit: int
    waiting: int
    # open, closed, consent req., etc. that kinda thing
    enrollment_status: str

    # instructor name
    instructor: str
    # actually a hash, i think; but a unique identifier of some sort
    instructor_id: str
    # long description; might include frequencies and prerequisites
    description: str
    # fulfills which requirements?
    uni_reqs: Iterable[str]

def parse_times(time_location: bs4.element.Tag) -> List[CourseTime]:
    meeting = CourseTime()
    schedule = []
    i = 0

    for el in time_location.contents:
        if isinstance(el, bs4.element.Tag):
            if el.name == 'hr':
                schedule.append(meeting)
                i = 0
                meeting = CourseTime()

            elif el.name == 'strong':
                meeting.info = el.text.strip()

        elif isinstance(el, str):
            el = el.strip()

            if el.startswith('Block'):
                # trim "Block\xa0" from beginning
                # \xa0 = nbsp
                meeting.block = el[6:]
            elif i == 0 or (meeting.block is not None and i == 1):
                # first row or row after 'block'; times
                meeting.time = el
            else:
                meeting.location = el
        i += 1

    schedule.append(meeting)
    return schedule

def course_description(td: bs4.element.Tag) -> str:
    href = td.find('a')['href']
    # we know what the slashes are gonna look like, so no need for urljoin
    url = ('http://registrar-prod.unet.brandeis.edu/registrar/schedule/'
            # watch the single quotes!
            + re.search(r"'(course?[^']+)'", href).group(1))
    req = requests.get(url)
    if not req.ok:
        # TODO find a better error?
        raise ValueError
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    return soup.find('p').text.strip()

def row_to_course(tr: bs4.element.Tag) -> Course:
    # soup = bs4.BeautifulSoup(tr, 'html.parser')
    # return soup
    # GHHFHJHFGHJDHBKLDHJKGSDFGKJ
    class_number, course_id, title_reqs, time_location, enrollment, instructor, *_ = tr.find_all('td')
    subject, number, section, *_ = course_id.text.split()
    number, group = re.match(r'(\d+)([^0-9]*)', number).groups()

    name = title_reqs.find('strong').text.strip()
    reqs = list(map(
        lambda req: req.text.strip(),
        title_reqs.find_all('span', {'class': 'requirement'})))

    # last string in enrollment is like '4 / 10 / 0'
    # underscores ignore the slashes
    enrolled, _, limit, _, waiting = enrollment.contents[-1].split()

    instructor_id = re.search(
            r'emplid=([0-9a-f]+)',
            instructor.find('a')['href']).group(1)
    instructor = instructor.text.strip()

    return Course(
            name=name,
            class_number=int(class_number.text),

            subject=subject,
            number=int(number),
            group=group,

            schedule=parse_times(time_location),

            enrollment_status=' '.join(enrollment.find('span').text.split()),
            enrolled=enrolled,
            limit=limit,
            waiting=waiting,

            instructor=instructor,
            instructor_id=instructor_id,

            description=course_description(course_id),
            uni_reqs=reqs,
            )

def grouper(iterable, n):
    """
    generator of chunks of n
    """
    it = iter(iterable)
    while True:
        chunk_it = itertools.islice(it, n)
        try:
            first_el = next(chunk_it)
        except StopIteration:
            return
        yield itertools.chain((first_el,), chunk_it)

def main():
    pass

if __name__ == '__main__':
    main()
