Library for retrieving structured data from [Brandeis course
listings][course-listing]

Prereqs:
* `bs4`
* `requests`

Example:

    >>> req = requests.get('http://registrar-prod.unet.brandeis.edu/course/schedule/registrar/classes/2004/Fall/1400/all')
    >>> courses = brandeis.page_to_courses(req) # List[brandeis.Course]
    >>> brandeis.tr_to_course(my_bs4_element)
    Course(
            name='Computational Chemistry',
            class_number=5466,
            subject='CHEM',
            number=111,
            group='A',
            schedule=[
                CourseTime(
                    block='D',
                    times='M,W,Th 11:10 AM–12:00 PM',
                    location="Volen Nat'l Ctr for Complex106",
                    info=None)],
            enrolled=3,
            limit=999,
            waiting=0,
            enrollment_status='Open',
            syllabus=None,
            instructor='Jordan, Peter',
            instructor_id='623a39c741a1e4b4b530535787879e4158bd16bb',
            uni_reqs=['sn'],
            description='Prerequisite: Satisfactory grades in CHEM 41a and b, '
                'or equivalent. Does not meet the major requirements in '
                'chemistry.\n\nSelected topics in computational chemistry, '
                'including one or two of the following: small molecule modeling; '
                'biomolecular modeling; quantum mechanical modeling. Usually '
                'offered every second year.\nMr. Jordan')

`brandeis.Course` also provides a few properties:

* `friendly_number`, like `CHEM 111A` for the above
* `instructor_link`, like
  `https://www.brandeis.edu/facguide/person.html?emplid=623a39c741a1e4b4b530535787879e4158bd16bb`
  for the above (from the `instructor_id`)

A `brandeis.Course`’s `str()` looks like `CHEM 111A Computational Chemistry
(Jordan, Peter) [sn]`

[course-listing]: http://registrar-prod.unet.brandeis.edu/course/schedule/registrar/classes/2004/Fall/1400/all
