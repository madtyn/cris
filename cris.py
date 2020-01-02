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
from models import Months, CommonInfo, Receipt

SEP = ''
test = False


def extract_main_header(excel_data, cell_idx, msg):
    result = excel_data[cell_idx][FIRST_COL_IDX]
    print(msg, result)
    return result


def extract_common_info(excel_data):
    teacher = extract_main_header(excel_data, TEACHER_NAME_ROW_IDX, TEACHER_DETECTED_MSG)
    nif = extract_main_header(excel_data, NIF_TEACHER_ROW_IDX, NIF_DETECTED_MSG)
    school_year = extract_main_header(excel_data, SCHOOL_YEAR_ROW_IDX, SCHOOL_YEAR_DETECTED_MSG)
    activity = extract_main_header(excel_data, ACTIVITY_NAME_ROW_IDX, ACTIVITY_DETECTED_MSG)

    return CommonInfo(teacher, nif, school_year, activity)


def process_group(row):
    group = row[FIRST_COL_IDX]
    print(PROCESSING_GROUP_MSG, group)


def is_valid(sm):
    if 'S' in sm.processed.strip().upper():
        return False
    if type(sm.quota) is not int:
        return False
    if type(sm.number) is not int:
        return False

    return True


def process_student(info, row):
    student = row[FIRST_COL_IDX]
    print(PROCESSING_STUDENT_MSG, student)

    result = []
    for m in Months:
        try:
            sm = m.get_student_month(row)
            if not is_valid(sm):
                continue
            r = Receipt(common_info, student, sm)
            result.append(r)
        except IndexError:
            continue

    return result


if __name__ == '__main__':
    print(RUNNING_MSG)

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

        common_info = extract_common_info(data)

        current_row = ACTIVITY_NAME_ROW_IDX + 1

        while True:
            if not len(data[current_row]):
                break

            process_group(data[current_row])

            current_row += 1

            list_receipts = []
            for _ in range(STUDENTS_PER_GROUP):
                if len(data[current_row]):
                    list_receipts.extend(process_student(common_info, data[current_row]))
                elif test:
                    print(PROCESSING_STUDENT_MSG, '-')  # For achieving in the test to read a \n line
                current_row += 1

            for r in list_receipts:
                print(r.template())

        print(SUCCESS_MSG)
    else:
        os._exit(1)