TEACHER_NAME_ROW_IDX = 0
NIF_TEACHER_ROW_IDX = 1
SCHOOL_YEAR_ROW_IDX = 2
ACTIVITY_NAME_ROW_IDX = 3
FIRST_GROUP_ROW_IDX = 4

STUDENTS_PER_GROUP = 15
ROWS_PER_GROUP = STUDENTS_PER_GROUP + 1  # (Header row

COLS_PER_MONTH = 3
MONTHS = 12
FIRST_MONTH_COL = FIRST_PROCESSED_COL = 1
FIRST_RECEIPT_COL = 3
FIRST_QUOTA_COL = 4


def is_group_header_row(idx):
    """
    Checks if the row with index idx is a group header row

    :param idx: the int for the index
    :return: True if the index corresponds to a group header row, False otherwise
    """
    return idx % ROWS_PER_GROUP == FIRST_GROUP_ROW_IDX


if __name__ == '__main__':
    pass
FIRST_COL_IDX = 0