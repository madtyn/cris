"""

CRIS: Creador de Recibos Instantáneos Sistematizados

SCRIPT FILE TO BE EXECUTED FROM THE TEST SCRIPT

Requirements:
pip3 install pyexcel-ods3
"""
import os.path
import sys
from pyexcel_ods3 import get_data

from indexes import *
from messages import *
from models import Months

print(RUNNING_MSG)

test = False
SEP = ''
if len(sys.argv) > 1 and sys.argv[1] == 'test':
    SEP = '\n'
    test = True

print(ASK_INPUT, end=SEP)
input_file = input().rstrip('\n')
print(CHECK_INPUT_PATH)
print(input_file)

print(ASK_OUTPUT, end=SEP)
output_file = input().rstrip('\n')
print(CHECK_INPUT_PATH)
print(output_file)

if os.path.exists(input_file):
    print(DETECTED_FILE_MSG)
    print(READING_FILE_MSG)
    data = get_data(input_file)['CONTABILIDAD']
    print(READ_DATA_MSG)

    teacher = data[TEACHER_NAME_ROW_IDX][FIRST_COL_IDX]
    print(TEACHER_DETECTED_MSG, teacher)

    nif = data[NIF_TEACHER_ROW_IDX][FIRST_COL_IDX]
    print(NIF_DETECTED_MSG, nif)

    school_year = data[SCHOOL_YEAR_ROW_IDX][FIRST_COL_IDX]
    print(SCHOOL_YEAR_DETECTED_MSG, school_year)

    activity = data[ACTIVITY_NAME_ROW_IDX][FIRST_COL_IDX]
    print(ACTIVITY_DETECTED_MSG, activity)

    current_row = ACTIVITY_NAME_ROW_IDX + 1

    while True:
        if not len(data[current_row]):
            break
        group = data[current_row][FIRST_COL_IDX]
        print(PROCESSING_GROUP_MSG, group)
        current_row += 1

        for _ in range(STUDENTS_PER_GROUP):
            if len(data[current_row]):
                student = data[current_row][FIRST_COL_IDX]
                print(PROCESSING_STUDENT_MSG, student)
                for m in Months:
                    print(f'{m!s}')
                    try:
                        print(data[current_row][m.processed_idx])
                        print(data[current_row][m.number_idx])
                        print(data[current_row][m.quota_idx])
                    except IndexError:
                        continue
            elif test:
                print(PROCESSING_STUDENT_MSG, '-')  # For achieving in the test to read a \n line
            current_row += 1

    print(SUCCESS_MSG)
else:
    os._exit(1)


