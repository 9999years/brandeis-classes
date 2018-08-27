SUBJECT_NUMBERS = {
    100  : 'African and Afro-American Studies',
    200  : 'American Studies',
    300  : 'Anthropology',
    400  : 'Arabic Language, Literature and Culture',
    425  : 'Architectural Studies',
    450  : 'Art History',
    475  : 'Asian-American Pacific Islander',
    500  : 'Biochemistry',
    510  : 'Biochemistry and Biophysics',
    600  : 'Biological Physics',
    700  : 'Biology',
    850  : 'Biotechnology',
    900  : 'Business',
    1000 : 'Chemistry',
    1100 : 'Chinese',
    1200 : 'Classical Studies',
    1250 : 'Comparative Humanities',
    1300 : 'Comparative Literature and Culture',
    1400 : 'Computer Science',
    9999 : 'Courses Offered for the First Time',
    1425 : 'Creative Writing',
    1475 : 'Creativity, the Arts, and Social Transformation',
    1500 : 'East Asian Studies',
    1600 : 'Economics',
    1700 : 'Education',
    1800 : 'English',
    1850 : 'English as a Second Language',
    1900 : 'Environmental Studies',
    2000 : 'European Cultural Studies',
    2050 : 'Experiential Learning',
    2100 : 'Film, Television and Interactive Media',
    2300 : 'Fine Arts',
    8000 : 'First Year Seminars (FYS)',
    2400 : 'French and Francophone Studies',
    2450 : 'Genetic Counseling',
    2500 : 'German Studies',
    2525 : 'German, Russian, and Asian Languages and Literature',
    2535 : 'Global Studies',
    2550 : 'Greek',
    2750 : 'Health, Wellness and Life Skills',
    2700 : 'Health: Science, Society, and Policy',
    2800 : 'Hebrew',
    2900 : 'Heller School for Social Policy and Management',
    6600 : 'Hispanic Studies',
    3000 : 'History',
    3100 : 'History of Ideas',
    3200 : 'Hornstein Jewish Professional Leadership Program',
    3250 : 'Humanities',
    3300 : 'Independent Interdisciplinary Major',
    3400 : 'International and Global Studies',
    3600 : 'International Business School',
    3700 : 'Internship',
    3900 : 'Islamic and Middle Eastern Studies',
    4000 : 'Italian Studies',
    4100 : 'Japanese',
    4200 : 'Journalism',
    4225 : 'Justice Brandeis Semester',
    4235 : 'Korean',
    4600 : 'Language and Linguistics',
    4250 : 'Latin',
    4300 : 'Latin American and Latino Studies',
    4400 : 'Legal Studies',
    4700 : 'Mathematics',
    4800 : 'Medieval and Renaissance Studies',
    4900 : 'Molecular and Cell Biology',
    5000 : 'Music',
    5100 : 'Near Eastern and Judaic Studies',
    5200 : 'Neuroscience',
    5300 : 'Peace, Conflict, and Coexistence Studies',
    5400 : 'Philosophy',
    5500 : 'Physical Education',
    5600 : 'Physics',
    5700 : 'Politics',
    5750 : 'Portuguese',
    5800 : 'Postbaccalaureate Premedical Studies',
    5900 : 'Psychology',
    5950 : 'Quantitative Biology',
    6000 : 'Religious Studies',
    6100 : 'Romance Studies',
    6300 : 'Russian Studies',
    6325 : 'Sculpture and Digital Media',
    6350 : 'Sexuality and Queer Studies',
    6400 : 'Social Justice and Social Policy',
    6500 : 'Sociology',
    6550 : 'South Asian Studies',
    6625 : 'Spanish Language and Literature',
    6675 : 'Studio Art',
    6700 : 'Theater Arts',
    7050 : 'University Writing (COMP and UWS)',
    6900 : "Women's, Gender, and Sexuality Studies",
    7000 : 'Yiddish',
}

SUBJECTS = {
    'AAAS'     : 'African and Afro-American Studies'                , # 100
    'HIST'     : 'American Studies'                                 , # 200
    'ANTH'     : 'Anthropology'                                     , # 300
    'ARBC'     : 'Arabic Language, Literature and Culture'          , # 400
    'AAPI'     : 'Asian-American Pacific Islander'                  , # 475
    'BCHM'     : 'Biochemistry and Biophysics'                      , # 510
    'BIOL'     : 'Biology'                                          , # 700
    'BUS'      : 'Business'                                         , # 900
    'CHEM'     : 'Chemistry'                                        , # 1000
    'CHIN'     : 'Chinese Studies'                                  , # 1100
    'CLAS'     : 'Classical Studies'                                , # 1200
    'COMP'     : 'Composition'                                      ,
    'COSI'     : 'Computer Science'                                 , # 1400
    'CHIN'     : 'Chinese'                                          , # 1500
    'ECON'     : 'Economics'                                        , # 1600
    'ED'       : 'Education'                                        , # 1700
    'ESL'      : 'English as a Second Language'                     , # 1850
    'ENVS'     : 'Environmental Studies'                            , # 1900
    'PHIL'     : 'Philosophy'                                       , # 2000
    'EL'       : 'Experiential Learning'                            , # 2050
    'ENG'      : 'English'                                          , # 2100
    'FA'       : 'Fine Arts'                                        , # 2300
    'FYS'      : 'First Year Seminars'                              , # 8000
    'FREN'     : 'French and Francophone Studies'                   , # 2400
    'GER'      : 'German Studies'                                   , # 2500
    'HS'       : 'Global Studies'                                   , # 2535
    'GRK'      : 'Greek'                                            , # 2550
    'HBRW'     : 'Hebrew'                                           , # 2800
    'HS'       : 'Heller School for Social Policy and Management'   , # 2900
    'HISP'     : 'Hispanic Studies'                                 , # 6600
    'HIST'     : 'History'                                          , # 3000
    'HRNS'     : 'Hornstein Jewish Professional Leadership Program' , # 3200
    'HUM'      : 'Humanities'                                       , # 3250
    'POL'      : 'International and Global Studies'                 , # 3400
    'FIN'      : 'International Business School'                    , # 3600
    'INT'      : 'Internship'                                       , # 3700
    'IMES'     : 'Islamic and Middle Eastern Studies'               , # 3900
    'ITAL'     : 'Italian Studies'                                  , # 4000
    'JAPN'     : 'Japanese'                                         , # 4100
    'JOUR'     : 'Journalism'                                       , # 4200
    'KOR'      : 'Korean'                                           , # 4235
    'LING'     : 'Language and Linguistics'                         , # 4600
    'LAT'      : 'Latin'                                            , # 4250
    'HISP'     : 'Latin American and Latino Studies'                , # 4300
    'LGLS'     : 'Legal Studies'                                    , # 4400
    'MATH'     : 'Mathematics'                                      , # 4700
    'MUS'      : 'Medieval and Renaissance Studies'                 , # 4800
    'MUS'      : 'Music'                                            , # 5000
    'NEJS'     : 'Near Eastern and Judaic Studies'                  , # 5100
    'POL'      : 'Peace, Conflict, and Coexistence Studies'         , # 5300
    'PHIL'     : 'Philosophy'                                       , # 5400
    'PE'       : 'Physical Education'                               , # 5500
    'PHYS'     : 'Physics'                                          , # 5600
    'POL'      : 'Politics'                                         , # 5700
    'PSYC'     : 'Psychology'                                       , # 5900
    'RUS'      : 'Russian Studies'                                  , # 6300
    'HIST/SOC' : 'Sexuality and Queer Studies'                      , # 6350
    'SOC'      : 'Sociology'                                        , # 6500
    'SAS'      : 'South Asian Studies'                              , # 6550
    'THA'      : 'Theater Arts'                                     , # 6700
    'UWS'      : 'University Writing (COMP and UWS)'                , # 7050
    'WMGS'     : "Women's, Gender, and Sexuality Studies"           , # 6900
    'YDSH'     : 'Yiddish'                                          , # 7000
    'AMST' : '',
    'BCBP' : '',
    'BCSC' : '',
    'BIBC' : '',
    'BIOP' : '',
    'BIOT' : '',
    'BIPH' : '',
    'BISC' : '',
    'CA' : '',
    'CAST' : '',
    'CBIO' : '',
    'CHSC' : '',
    'COEX' : '',
    'COMH' : '',
    'COML' : '',
    'CONT' : '',
    'CP' : '',
    'EAS' : '',
    'EBIO' : '',
    'ECS' : '',
    'FECS' : '',
    'FILM' : '',
    'GECS' : '',
    'GS' : '',
    'GSAS' : '',
    'HECS' : '',
    'HINDI' : '',
    'HOID' : '',
    'HSSP' : '',
    'IECS' : '',
    'IGS' : '',
    'JCS' : '',
    'LALS' : '',
    'LAS' : '',
    'NBIO' : '',
    'NPHY' : '',
    'NPSY' : '',
    'PAX' : '',
    'PHSC' : '',
    'PMED' : '',
    'PORT' : '',
    'QBIO' : '',
    'RECS' : '',
    'REL' : '',
    'SAL' : '',
    'SECS' : '',
    'SJSP' : '',
    'SPAN' : '',
    'SQS' : '',
    'SYS' : '',
    'USEM' : '',
    'WMNS' : '',
}

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

SEMESTERS = ['Spring', 'Summer', 'Fall']
