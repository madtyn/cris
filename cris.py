"""

CRIS: Creador de Recibos Instantáneos Sistematizados

SCRIPT FILE TO BE EXECUTED FROM THE TEST SCRIPT

Requirements:
pip3 install pyexcel-ods3
"""
import datetime
import os.path
import sys
import random
from collections import OrderedDict
from tkinter import filedialog as fd, Tk, messagebox
import os

from pyexcel_ods3 import get_data, save_data

from indexes import *
from messages import *
from models import Months, CommonInfo, Receipt

SEP = ''
test = False


def extract_main_header(excel_data, cell_idx, msg):
    """
    Extracts one field from the main header in the ods
    :param excel_data: the data variable
    :param cell_idx: the cell index
    :param msg: the msg for the user
    :return: the extracted data from cell
    """
    result = excel_data[cell_idx][FIRST_COL_IDX]
    print(msg, result)
    return result


def extract_common_info(excel_data):
    """
    Extracts the fields from the main header
    :param excel_data: the data variable
    :return: the header info in an object
    """
    teacher = extract_main_header(excel_data, TEACHER_NAME_ROW_IDX, TEACHER_DETECTED_MSG)
    nif = extract_main_header(excel_data, NIF_TEACHER_ROW_IDX, NIF_DETECTED_MSG)
    school_year = extract_main_header(excel_data, SCHOOL_YEAR_ROW_IDX, SCHOOL_YEAR_DETECTED_MSG)
    activity = extract_main_header(excel_data, ACTIVITY_NAME_ROW_IDX, ACTIVITY_DETECTED_MSG)

    return CommonInfo(teacher, nif, school_year, activity)


def process_group(row):
    """
    Process a group title line
    :param row: the excel row as a list
    """
    group = row[FIRST_COL_IDX]
    print(PROCESSING_GROUP_MSG, group)


def is_valid(sm):
    """
    Determines if a StudentMonth tuple is valid for processing
    :param sm: the StudentMonth object
    :return: True if it can be processed, False otherwise
    """
    if 'S' in sm.processed.strip().upper():
        return False
    if type(sm.quota) is not int:
        return False
    if type(sm.number) is not int:
        return False

    return True


def process_student(info, row, output_file):
    """
    Process a student row, creating a Receipt and writing it to file
    :param info: the common info for all student receipts
    :param row: the excel row as a list
    :param output_file: the file to write to
    :return: all the receipts as a list variable
    """
    result_list = []
    student = row[FIRST_COL_IDX]
    print(PROCESSING_STUDENT_MSG, student)

    for m in Months:
        try:
            sm = m.get_student_month(row)
            if is_valid(sm):
                r = Receipt(info, student, sm).template()
                output_file.write(r)
                row[m.processed_idx] = 'S'
                result_list.append(r)
        except IndexError:
            continue

    return result_list


def ask_input(test):
    """
    Asks for input file
    :param test: True if test mode, False otherwise
    :return: the filename for the input file
    """
    if test:
        print(ASK_INPUT, end=SEP)
        input_filename = input().rstrip('\n')
    else:
        input_filetypes = (("Openoffice calc files", "*.ods"),)
        input_filename = fd.askopenfilename(initialdir=os.getcwd(), filetypes=input_filetypes)
    return input_filename


def ask_output(test):
    """
    Asks for output file
    :param test: True if test mode, False otherwise
    :return: the file-like object for the output file
    """
    if test:
        print(ASK_OUTPUT, end=SEP)
        output_filename = input().rstrip('\n')
        output_file = open(output_filename, 'w', encoding='utf-8')
    else:
        output_filetypes = (("Archivo de recibos CRIS", "*.txt"),)
        output_file = fd.asksaveasfile(initialdir=os.getcwd(), filetypes=output_filetypes)
    return output_file


if __name__ == '__main__':
    print(RUNNING_MSG)

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        SEP = '\n'
        test = True
    else:
        root = Tk()
        root.withdraw()

    input_file = ask_input(test)
    print(CHECK_FILE_PATH)
    print(input_file)

    if os.path.exists(input_file):
        output_file = ask_output(test)
        print(CHECK_FILE_PATH)
        print(output_file.name)

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

            for _ in range(STUDENTS_PER_GROUP):
                if len(data[current_row]):
                    process_student(common_info, data[current_row], output_file)
                elif test:
                    # For the test to read a \n line
                    print(PROCESSING_STUDENT_MSG, '-')
                current_row += 1

        output_file.close()
        output_data = OrderedDict()
        output_data.update({'CONTABILIDAD': data})

        d = datetime.datetime.today()
        new_excel_path = os.path.dirname(input_file)
        new_excel_filename = f'{d.strftime("%Y_%m_%d_%Hh_%Mm")}_{os.path.basename(input_file)}'
        new_excel_name = '/'.join([new_excel_path, new_excel_filename])
        save_data(new_excel_name, output_data)

        if not test:
            msg = 'Fin de proceso. Tip del día:\n' + random.choice(END_MESSAGES)
            messagebox.showinfo('De nada, colega', msg)
        print(SUCCESS_MSG)
    else:
        os._exit(1)
