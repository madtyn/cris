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

import indexes
import messages
from models import Months, CommonInfo, Receipt
from pdfmaker import PdfOutput

LOGO_FILENAME = 'logo.png'

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
    result = excel_data[cell_idx][indexes.FIRST_COL_IDX]
    print(msg, result)
    return result


def extract_common_info(excel_data):
    """
    Extracts the fields from the main header
    :param excel_data: the data variable
    :return: the header info in an object
    """
    teacher = extract_main_header(excel_data,
                                  indexes.TEACHER_NAME_ROW_IDX,
                                  messages.TEACHER_DETECTED_MSG)
    nif = extract_main_header(excel_data,
                              indexes.NIF_TEACHER_ROW_IDX,
                              messages.NIF_DETECTED_MSG)
    school_year = extract_main_header(excel_data,
                                      indexes.SCHOOL_YEAR_ROW_IDX,
                                      messages.SCHOOL_YEAR_DETECTED_MSG)
    activity = extract_main_header(excel_data,
                                   indexes.ACTIVITY_NAME_ROW_IDX,
                                   messages.ACTIVITY_DETECTED_MSG)

    return CommonInfo(teacher, nif, school_year, activity)


def process_group(row):
    """
    Process a group title line
    :param row: the excel row as a list
    """
    group = row[indexes.FIRST_COL_IDX]
    print(messages.PROCESSING_GROUP_MSG, group)


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
    student = row[indexes.FIRST_COL_IDX]
    print(messages.PROCESSING_STUDENT_MSG, student)

    for m in Months:
        try:
            sm = m.get_student_month(row)
            if is_valid(sm):
                r = Receipt(info, student, sm)
                output_file.write_receipt(r)
                row[m.processed_idx] = 'S'
                result_list.append(r)
        except IndexError:
            continue

    return result_list


def ask_input(test_flag):
    """
    Asks for input file
    :param test_flag: True if test mode, False otherwise
    :return: the filename for the input file
    """
    if test_flag:
        print(messages.ASK_INPUT, end=SEP)
        input_filename = input().rstrip('\n')
    else:
        input_filetypes = (("Openoffice calc files", "*.ods"),)
        input_filename = fd.askopenfilename(initialdir=os.getcwd(), filetypes=input_filetypes)
    return input_filename


def ask_output(test_flag):
    """
    Asks for output file
    :param test_flag: True if test mode, False otherwise
    :return: the file-like object for the output file
    """
    if test_flag:
        print(messages.ASK_OUTPUT, end=SEP)
        output_filename = input().rstrip('\n')
    else:
        output_filetypes = (("Pdfs de recibos CRIS", "*.pdf"),)
        output_filename = fd.asksaveasfilename(initialdir=os.getcwd(),
                                               filetypes=output_filetypes)
    logo_filename = os.path.join(os.path.dirname(output_filename), LOGO_FILENAME)
    if os.path.exists(logo_filename):
        output_file = PdfOutput(output_filename, logo=logo_filename)
        return output_file
    messagebox.showerror('Error',
                         f'No se encontró el fichero {LOGO_FILENAME} \n'
                         f'en la ruta {os.path.dirname(logo_filename)}')
    return os._exit(1)


if __name__ == '__main__':
    print(messages.RUNNING_MSG)

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        SEP = '\n'
        test = True
    else:
        root = Tk()
        root.withdraw()

    input_file = ask_input(test)
    print(messages.CHECK_FILE_PATH)
    print(input_file)

    if os.path.exists(input_file):
        pdf_output_file = ask_output(test)
        print(messages.CHECK_FILE_PATH)
        print(pdf_output_file.name)

        print(messages.DETECTED_FILE_MSG)
        print(messages.READING_FILE_MSG)
        data = get_data(input_file)['CONTABILIDAD']
        print(messages.READ_DATA_MSG)

        common_info = extract_common_info(data)

        current_row = indexes.ACTIVITY_NAME_ROW_IDX + 1

        while True:
            if not len(data[current_row]):
                break

            process_group(data[current_row])

            current_row += 1

            for _ in range(indexes.STUDENTS_PER_GROUP):
                if len(data[current_row]):
                    process_student(common_info, data[current_row], pdf_output_file)
                elif test:
                    # For the test to read a \n line
                    print(messages.PROCESSING_STUDENT_MSG, '-')
                current_row += 1

        pdf_output_file.save()
        output_data = OrderedDict()
        output_data.update({'CONTABILIDAD': data})

        d = datetime.datetime.today()
        new_excel_path = os.path.dirname(input_file)
        new_excel_filename = f'{d.strftime("%Y_%m_%d_%Hh_%Mm")}_{os.path.basename(input_file)}'
        new_excel_name = '/'.join([new_excel_path, new_excel_filename])
        save_data(new_excel_name, output_data)

        if not test:
            msg = 'Fin de proceso. Tip del día:\n' + random.choice(messages.END_MESSAGES)
            messagebox.showinfo('De nada, colega', msg)
        print(messages.SUCCESS_MSG)
    else:
        messagebox.showerror('Error', 'No se encontró el fichero')
        os._exit(1)
