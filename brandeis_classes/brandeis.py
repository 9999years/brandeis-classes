import functools
import itertools
import json
import re
from collections import namedtuple
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple, cast

import bs4
import requests

from . import constants


class Unreachable(RuntimeError):
    """An exception raised when theoretically-unreachable code is hit.

    Comparable to Rust's ``unreachable!()`` panic-macro.
    """


@dataclass
class CourseTime:
    block: str
    times: str
    location: str
    info: str

    def dict(self):
        # useful for encoding as JSON
        return self.__dict__.copy()


@dataclass
class Instructor:
    name: str
    # actually a hash, i think; but a unique identifier of some sort
    id: str

    def __str__(self):
        return self.name

    def dict(self):
        # useful for encoding as JSON
        return self.__dict__.copy()


@dataclass
class Course:
    # e.g. Modal, Temporal, and Spatial Logic for Language
    name: str
    # e.g. 16903; registration number for sage
    class_number: int

    # subject, number, and group form parts of the course's "display name"
    # an example is COSI 118A_1, where the trailing "1" is a section number
    # e.g. COSI
    subject: str
    # e.g. 118
    number: int
    # e.g. a, b, c, ...
    group: str
    # 1, 2, 3...
    # SOMETIMES (ED 285 1DL) something weird like '1DL'
    section: str

    # weirdly formatted; maybe consistent? parsing this is a job for later
    schedule: List[CourseTime]

    # enrollment
    enrolled: int
    limit: int
    waiting: int
    # open, closed, consent req., etc. that kinda thing
    enrollment_status: str

    # syllabus link
    syllabus: str
    # instructor(s); a list
    instructors: List[Instructor]
    # fulfills which requirements?
    uni_reqs: List[str]
    # long description; might include frequencies and prerequisites
    description: Optional[str]
    # notes below course title, might include notes on prereqs, etc.
    notes: str

    semester: Optional[str]
    year: Optional[int]

    @property
    def title(self) -> str:
        """An alias for ``self.name``
        """
        return self.name

    @property
    def instructor_links(self) -> Iterable[str]:
        """URLs linking to each instructor.
        """
        return (
            "https://www.brandeis.edu/facguide/person.html?emplid={instructor.id}"
            for instructor in self.instructors
        )

    @property
    def friendly_number(self) -> str:
        """User-friendly course number.
        """
        return f"{self.subject} {self.number}{self.group}" + (
            f"_{self.section}" if self.section else ""
        )

    @property
    def uni_reqs_str(self) -> str:
        """Requirements-description string.
        """
        return ("[" + ", ".join(self.uni_reqs) + "]") if self.uni_reqs else ""

    @property
    def instructor_str(self) -> str:
        """Instructor string.
        """
        return "; ".join(map(str, self.instructors)) if self.instructors else ""

    def dict(self):
        ret = self.__dict__.copy()
        if ret["schedule"]:
            ret["schedule"] = [ct.dict() for ct in ret["schedule"]]
        if ret["instructors"]:
            ret["instructors"] = [i.dict() for i in ret["instructors"]]
        return ret

    @staticmethod
    def from_dict(d):
        ret = Course(**d)
        if ret.schedule:
            ret.schedule = [CourseTime(**s) for s in ret.schedule]
        if ret.instructors:
            ret.instructors = [Instructor(**i) for i in ret.instructors]
        return ret

    def __str__(self):
        return f"{self.friendly_number} {self.name} ({self.instructor_str})" + (
            f" {self.uni_reqs_str}" if self.uni_reqs else ""
        )


def parse_times(time_location: bs4.element.Tag) -> List[CourseTime]:
    block: Optional[str] = None
    times: Optional[str] = None
    location: Optional[str] = None
    info: Optional[str] = None
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
            if el.name == "hr":
                schedule.append(
                    CourseTime(
                        block=cast(str, block),
                        times=cast(str, times),
                        location=cast(str, location),
                        info=cast(str, info),
                    )
                )
                i = -1

            elif el.name == "strong":
                info = el.text.strip()

        elif isinstance(el, str):
            # join/split collapses whitespace
            el = " ".join(el.split())
            if not el:
                # skip empty tokens
                continue
            i += 1

            if el.startswith("Block"):
                # trim "Block\xa0" from beginning
                # \xa0 = nbsp
                block = el[6:]
            elif i == 0 or (block is not None and i == 1):
                # first row or row after 'block'; times
                times = el
            else:
                location = el

    schedule.append(
        CourseTime(
            block=cast(str, block),
            times=cast(str, times),
            location=cast(str, location),
            info=cast(str, info),
        )
    )
    return schedule


def multiline_text(els: Iterable) -> str:
    # stringify; make <br>s \ns
    ret = []
    for tok in els:
        if isinstance(tok, str):
            ret.append(tok.strip())
        elif isinstance(tok, bs4.element.Tag):
            if tok.name == "br":
                ret.append("\n")
            else:
                ret.append(str(tok))
    return "".join(ret).strip()


def course_description(td: bs4.element.Tag) -> str:
    href = td.find("a")["href"]
    # we know what the slashes are gonna look like, so no need for urljoin
    url = (
        "http://registrar-prod.unet.brandeis.edu/registrar/schedule/"
        # watch the single quotes!
        + cast(re.Match, re.search(r"'(course?[^']+)'", href)).group(1)
    )
    req = requests.get(url)
    if not req.ok:
        raise requests.exceptions.HTTPError
    soup = bs4.BeautifulSoup(req.text, "html.parser")

    return multiline_text(soup.find("p").children)


def syllabus(td: bs4.element.Tag) -> str:
    for a in td.find_all("a"):
        if "Syllabus" in a.text:
            return a["href"]

    raise Unreachable


def course_ids(td: bs4.element.Tag) -> Tuple[str, int, str, str]:
    subject, number, section, *_ = td.text.split()
    number, group = cast(re.Match, re.match(r"(\d+)([^0-9]*)", number)).groups()
    return subject, int(number), group, section


def uni_reqs(td: bs4.element.Tag):
    return list(
        map(lambda req: req.text.strip(), td.find_all("span", {"class": "requirement"}))
    )


def course_notes(td: bs4.element.Tag):
    found_close = False
    children = td.children
    if uni_reqs(td):
        for tok in children:
            if isinstance(tok, str) and tok.strip() == "]":
                found_close = True
                break
    else:
        for tok in children:
            if isinstance(tok, bs4.element.Tag) and tok.name == "strong":
                found_close = True
                break

    if not found_close:
        return None

    ret = multiline_text(children)

    if not ret.strip():
        return None

    return ret


def enrollment_info(td: bs4.element.Tag):
    # last string in enrollment is like '4 / 10 / 0'
    # underscores ignore the slashes
    enrolled, _, limit, _, waiting = td.contents[-1].split()
    return int(enrolled), int(limit), int(waiting)


def enrollment_status(td: bs4.element.Tag):
    return " ".join(td.find("span").text.split())


def instructor_info(td: bs4.element.Tag) -> List[Instructor]:
    """returns name, id tuple"""

    def instructor_id(a):
        return re.search(r"emplid=([0-9a-f]+)", a["href"]).group(1)

    instructors = td.find_all("a")
    if not instructors:
        return []
    else:
        return [
            Instructor(name=" ".join(a.text.split()), id=instructor_id(a))
            for a in instructors
        ]


def tr_is_course(tr: bs4.element.Tag) -> List[bs4.element.Tag]:
    """
    if yes: returns list of tds
    if no: returns None
    """
    tds: List[bs4.element.Tag] = list(filter(tag_filter("td"), tr.children))
    if len(tds) < 6 or (
        "Class #" in tds[0].text
        and "Course #" in tds[1].text
        and "Course Title" in tds[2].text
    ):
        return []
    return tds


def tr_to_course(tr: bs4.element.Tag, request_description=True) -> Optional[Course]:
    """
    might return None
    """
    tds = tr_is_course(tr)
    if not tds:
        return None

    # GHHFHJHFGHJDHBKLDHJKGSDFGKJ
    (
        class_number,
        course_id,
        title_reqs,
        time_location,
        enrollment,
        instructor,
        *rest,
    ) = tds

    if rest:
        _books, *_ = rest

    subject, number, group, section = course_ids(course_id)

    name = title_reqs.find("strong").text.strip()
    reqs = uni_reqs(title_reqs)

    enrolled, limit, waiting = enrollment_info(enrollment)

    instructors = instructor_info(instructor)

    return Course(
        name=name,
        class_number=int(class_number.text),
        subject=subject,
        number=number,
        group=group,
        section=section,
        schedule=parse_times(time_location),
        enrollment_status=enrollment_status(enrollment),
        enrolled=enrolled,
        limit=limit,
        waiting=waiting,
        syllabus=syllabus(course_id),
        instructors=instructors,
        description=course_description(course_id) if request_description else None,
        notes=course_notes(title_reqs),
        uni_reqs=reqs,
        semester=None,  # TODO this shouldn't be None
        year=None,  # TODO this shouldn't be None
    )


def is_tag(tag, name=None):
    return isinstance(tag, bs4.element.Tag) and (tag.name == name if name else True)


def tag_filter(name):
    return functools.partial(is_tag, name=name)


def page_to_courses(html, request_description=True):
    soup = bs4.BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="classes-list")
    if not table:
        # couldnt find a good table, try anyways
        table = soup
    trs = filter(tag_filter("tr"), table.children)
    # return list(trs)
    tr_fn = tr_to_course
    if not request_description:
        tr_fn = functools.partial(tr_to_course, request_description=False)
    return list(filter(None, map(tr_fn, trs)))


def schedule_url(year, semester, subject, kind="all"):
    """
    kind: All, UGRD, or GRAD
    semester: Fall, Spring, or Summer
    subject: an int; a key from constants.SUBJECTS
    """
    return (
        "http://registrar-prod.unet.brandeis.edu/registrar/schedule/classes"
        f"/{year}/{semester}/{subject}/{kind}"
    )


def strm(year, semester):
    return int(
        1000 + (10 * (year % 100)) + constants.SEMESTERS.index(semester) + 1  # ????
    )


def load_courses(file_obj):
    course_dicts = json.load(file_obj)
    return [Course.from_dict(c) for c in course_dicts]
