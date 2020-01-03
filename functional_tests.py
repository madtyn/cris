import os
import sys

import subprocess as sp

from indexes import ACTIVITY_NAME_ROW_IDX
from messages import *

INPUT_FILE = '/home/madtyn/sandbox/kills/sample_input.ods'
OUTPUT_FILE = '/home/madtyn/sandbox/kills/output.txt'

# The user cristofania executes CRIS
process = sp.Popen('/usr/bin/python3 /home/madtyn/PycharmProjects/cris/cris.py test', stdin=sp.PIPE, stdout=sp.PIPE, shell=True,
                   env={'PYTHONPATH': os.pathsep.join(sys.path),
                        'PYTHONIOENCODING': 'UTF-8'})


def check_next_line(expected_line, error_msg):
    global process
    printed = process.stdout.readline()
    assert f'{expected_line}\n'.encode().rstrip(
        b'\n') in printed.rstrip(b'\n'), error_msg


def check_regular_line(expected_line, group=False):
    global process
    printed = process.stdout.readline()

    is_eof = f'{SUCCESS_MSG}\n'.encode().rstrip(b'\n') in printed.rstrip(b'\n')
    if is_eof:
        return False
    group_end_condition = printed.strip() == b'' or b'Nombre del escolar' in printed.strip()
    if group and group_end_condition:
        return False

    is_expected_line = f'{expected_line}\n'.encode().rstrip(b'\n') in printed.rstrip(b'\n')

    assert is_expected_line, 'La fila es incorrecta'
    return True


def test_input_path_file(asking_msg, asked_file):
    global process
    # CRIS asks for the path and name of the input file
    check_next_line(asking_msg, f'No se pidió el fichero {asked_file}')
    # The user inputs the input file name
    process.stdin.write(asked_file.encode() + b'\n')
    process.stdin.flush()
    check_next_line(CHECK_FILE_PATH, 'No hubo respuesta a la introducción de ruta')
    check_next_line(asked_file, 'La ruta y nombre de fichero no coinciden con lo esperado')


check_next_line(RUNNING_MSG, 'Algo falló en la ejecución de CRIS')

test_input_path_file(ASK_INPUT, INPUT_FILE)
test_input_path_file(ASK_OUTPUT, OUTPUT_FILE)

# CRIS checks the input file is there
assert os.path.exists(INPUT_FILE)
assert os.path.isfile(INPUT_FILE)

input_size = os.path.getsize(INPUT_FILE)
assert input_size > 0, 'Input file is empty'

# CRIS shows a message about having detected the file
check_next_line(DETECTED_FILE_MSG, 'No existe el fichero o es vacío')

# CRIS shows a reading file message
check_next_line(READING_FILE_MSG, 'No se llegó a leer el fichero *.ods con normalidad')

# CRIS shows a reading success message
check_next_line(READ_DATA_MSG, 'Algo falló en la lectura de la hoja de cálculo')

check_next_line(TEACHER_DETECTED_MSG, 'No se detecta un valor para el profesor')
check_next_line(NIF_DETECTED_MSG, 'No se detecta un valor para el profesor')
check_next_line(SCHOOL_YEAR_DETECTED_MSG, 'No se detecta un valor para el año escolar')
check_next_line(ACTIVITY_DETECTED_MSG, 'No se detecta un valor para la actividad')

current_row = ACTIVITY_NAME_ROW_IDX + 1
while True:
    if not check_regular_line(PROCESSING_GROUP_MSG, group=True):
        break
    current_row += 1
    for _ in range(15):
        check_regular_line(PROCESSING_STUDENT_MSG)
        current_row += 1

# The user notices there is a PDF as output
assert os.path.exists(OUTPUT_FILE), 'The output was not generated'
assert os.path.isfile(OUTPUT_FILE), 'Something is wrong with the output file'

output_size = os.path.getsize(OUTPUT_FILE)
assert output_size > 0, 'Output file is empty'
