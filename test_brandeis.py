from bs4 import BeautifulSoup

import brandeis

def read(fname, mode='r', encoding='utf-8'):
    with open(fname, mode, encoding=encoding) as f:
        return f.read()

def tr_to_soup(html):
    return BeautifulSoup(html, 'html.parser').find('tr')

def test_tr_to_course():
    tr = tr_to_soup(read('test-data/cosi_119a_1.html'))
    crs = brandeis.tr_to_course(tr, request_description=False)
    assert crs.friendly_number == 'COSI 119A_1'
    assert crs.uni_reqs_str == '[sn]'
    assert crs.name == 'Autonomous Robotics Lab'
    assert crs.class_number == 16905
    assert crs.subject == 'COSI'
    assert crs.number == 119
    assert crs.group == 'A'
    assert crs.section == '1'
    assert crs.schedule == [
        brandeis.CourseTime(
            block='S3',
            times='W 2:00 PM–4:50 PM',
            location='Carl J. Shapiro ScienceCtrLL16',
            info=None),
        brandeis.CourseTime(
            block='X3',
            times='W 6:30 PM–9:20 PM',
            location='Carl J. Shapiro ScienceCtrLL16',
            info='Mandatory:')]
    assert crs.enrolled == 4
    assert crs.limit == 10
    assert crs.waiting == 0
    assert crs.enrollment_status == 'Open Consent Req.'
    assert crs.syllabus == 'https://moodle2.brandeis.edu/syllabus/public/0eedb7b65c693257c8d4d24ae46ba227.pdf'
    assert crs.instructors == [brandeis.Instructor(
        name='Salas, R. Pito',
        id='69957fcf6528db656418863916878ea0e4046b09')]
    assert crs.uni_reqs == ['sn']
    assert crs.semester == None
    assert crs.year == None
