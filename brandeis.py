from dataclasses import dataclass
from typing import Iterable, List
from collections import namedtuple
import itertools
import re
import functools

import requests
import bs4


# Requirements change over the years, so don't expect these to be perfectly
# stable, all valid for a given semester, or all-inclusive. Courses from 2004
# are sometimes marked 'qr2', for example. (shrug!)

UNI_REQS = {'CA', 'FL', 'HUM', 'NW', 'OC', 'PE-1', 'QR', 'SN', 'SS', 'UWS', 'WI'}

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

SEMESTERS = ['Fall', 'Spring', 'Summer']

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
    schedule: Iterable[CourseTime] = None

    # enrollment
    enrolled: int = None
    limit: int = None
    waiting: int = None
    # open, closed, consent req., etc. that kinda thing
    enrollment_status: str = None

    # syllabus link
    syllabus: str = None
    # instructor name
    instructor: str = None
    # actually a hash, i think; but a unique identifier of some sort
    instructor_id: str = None
    # fulfills which requirements?
    uni_reqs: Iterable[str] = None
    # long description; might include frequencies and prerequisites
    description: str = None

    semester: str = None
    year: int = None

    @property
    def instructor_link(self):
        return ('https://www.brandeis.edu/facguide/person.html?emplid='
                + self.instructor_id)

    @property
    def friendly_number(self):
        return f'{self.subject} {self.number}{self.group}'

    def __str__(self):
        return (f'{self.friendly_number} {self.name} ({self.instructor})'
                + ((' [' + ', '.join(self.uni_reqs) + ']')
                    if self.uni_reqs else ''))

# TODO fix this???
def parse_times(time_location: bs4.element.Tag) -> List[CourseTime]:
    meeting = CourseTime()
    schedule = []

    # time_location might look kinda like:
    #     <strong>Lecture:</strong>
    #     <br>Block D 
    #     <br>M,W,Th 11:00 AM–11:50 AM 
    #     <br>Golding Judaica Center110
    #     <hr>
    #     <strong>Recitation:</strong>
    #     <br>M 6:30 PM–9:20 PM 
    #     <br>Gerstenzang 123
    # NOTE: the "block" appears optional; so is the <strong>, especially if
    # theres only 1 listing

    # i is a counter for the string tokens in time_location; it only increments
    # on strings
    i = -1
    for el in time_location.children:
        if isinstance(el, bs4.element.Tag):
            if el.name == 'hr':
                schedule.append(meeting)
                i = -1
                meeting = CourseTime()

            elif el.name == 'strong':
                meeting.info = el.text.strip()

        elif isinstance(el, str):
            # join/split collapses whitespace
            el = ' '.join(el.split())
            if not el:
                # skip empty tokens
                continue
            i += 1

            if el.startswith('Block'):
                # trim "Block\xa0" from beginning
                # \xa0 = nbsp
                meeting.block = el[6:]
            elif i == 0 or (meeting.block is not None and i == 1):
                # first row or row after 'block'; times
                meeting.time = el.split()
            else:
                meeting.location = el

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

    # stringify; make <br>s \ns
    ret = []
    for tok in soup.find('p').children:
        if isinstance(tok, str):
            ret.append(tok)
        elif isinstance(tok, bs4.element.Tag):
            if tok.name == 'br':
                ret.append('\n')
            else:
                ret.append(str(tok))
    return ''.join(ret)

def syllabus(td: bs4.element.Tag) -> str:
    for a in td.find_all('a'):
        if 'Syllabus' in a.text:
            return a['href']

def tr_to_course(tr: bs4.element.Tag) -> Course:
    """
    might return None
    """
    tds = list(filter(tag_filter('td'), tr.children))
    if (len(tds) < 6 or (
                'Class #' in tds[0].text
            and 'Course #' in tds[1].text
            and 'Course Title' in tds[2].text)):
        return None

    # GHHFHJHFGHJDHBKLDHJKGSDFGKJ
    (class_number, course_id, title_reqs, time_location, enrollment,
            instructor, *_) = tds
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

            enrolled=int(enrolled),
            limit   =int(limit),
            waiting =int(waiting),

            syllabus=syllabus(course_id),
            instructor=instructor,
            instructor_id=instructor_id,

            description=course_description(course_id),
            uni_reqs=reqs,
            )

def is_tag(tag, name=None):
    return (isinstance(tag, bs4.element.Tag)
            and (tag.name == name if name else True))

def tag_filter(name):
    return functools.partial(is_tag, name=name)

def page_to_courses(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    trs = filter(
            tag_filter('tr'),
            soup.find('table', id='classes-list').children)
    # return list(trs)
    return list(filter(None, map(tr_to_course, trs)))

def main():
    pass

if __name__ == '__main__':
    main()
