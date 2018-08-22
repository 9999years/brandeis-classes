import argparse
import subprocess

from termcolor import colored

import brandeis

def main():
    for year in range(2008, 2018 + 1):
        print(colored('=========' + str(year) + '=========', 'red'))
        for semester in brandeis.constants.SEMESTERS:
            print(colored('---------' + semester + '---------', 'red'))
            subprocess.run(['python', 'scrape_courses.py', '-e', semester, '-y', str(year)])

if __name__ == '__main__':
    main()
