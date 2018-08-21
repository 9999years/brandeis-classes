from bs4 import BeautifulSoup

import brandeis

def read(fname, mode='r', encoding='utf-8'):
    with open(fname, mode, encoding=encoding) as f:
        return f.read()

def tr_to_soup(html):
    return BeautifulSoup(html, 'html.parser').find('tr')

def test_tr_to_course():
    tr = tr_to_soup(read('test-data/cosi_199a_1.html'))
    crs = brandeis.tr_to_course(tr)
    print(repr(crs.description))
    print(repr(crs.notes))
    assert crs == brandeis.Course(
            name='Autonomous Robotics Lab',
            class_number=16905,
            subject='COSI',
            number=119,
            group='A',
            section='1',
            schedule=[
                brandeis.CourseTime(
                    block='S3',
                    times='W 2:00 PM–4:50 PM',
                    location='Carl J. Shapiro ScienceCtrLL16',
                    info=None),
                brandeis.CourseTime(
                    block='X3',
                    times='W 6:30 PM–9:20 PM',
                    location='Carl J. Shapiro ScienceCtrLL16',
                    info='Mandatory:')],
            enrolled=4,
            limit=10,
            waiting=0,
            enrollment_status='Open Consent Req.',
            syllabus='https://moodle2.brandeis.edu/syllabus/public/0eedb7b65c693257c8d4d24ae46ba227.pdf',
            instructor='Salas, R. Pito',
            instructor_id='69957fcf6528db656418863916878ea0e4046b09',
            uni_reqs=['sn'],
            description='Prerequisites: COSI 12b, COSI 21a, and junior standing.\n\nLearn fundamentals of autonomous robots software. Learn and understand Robot Operating System (ROS), and foundational algorithms such as SLAM. Solve gradually more advanced problems, then demonstrate them on the actual robot. Use the mBot and  TurtleBot3 Robots. The course emphasizes real world implementations. Usually offered every semester.\nPito Salas',
            notes='See Course Catalog for prerequisites.\nStudents interested in enrolling should contact Pito Salas (pitosalas@brandeis.edu) for permission.',
            semester=None,
            year=None)
