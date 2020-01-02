import unittest

from cris import process_student, is_valid
from models import CommonInfo, Receipt, StudentMonth


class MyTestCase(unittest.TestCase):
    info = CommonInfo('Killstobal Boedo Buño', '21548796F', '2019/20', 'SONICREQUES')

    def test_is_valid(self):
        sm = StudentMonth('X', 'X', 'N')
        assert not is_valid(sm), 'Failed to validate XXN'
        sm = StudentMonth(12, 12, 'S')
        assert not is_valid(sm), 'Failed to validate an already processed month'
        sm = StudentMonth(15, 11, 'N')
        assert is_valid(sm), 'Failed to validate a correct month'

    def test_process_student(self):
        row = ['María Calviño Seixo',
               '15', '17', 'S',
               '30', '17', 'N',
               '45', '17', 'N',
               'X', 'X', 'N',
               'X', 'X', 'N',
               '30', '12', 'S',
               '45', '12', 'N',
               'X', 'X', 'N',
               'X', 'X', 'N',
               '60', 'X', 'N',
               '15', 'X', 'S',
               'X', 'X', 'N',
               ]
        result = process_student(self.info, row)
        assert type(result) == list and all(type(x) is Receipt for x in result)
        ref_row = []
        for i in range(1, 10):
            sm = StudentMonth(row[i:i + 3])
            if is_valid():
                ref_row.append(sm)

        assert len(result) == len(ref_row)


if __name__ == '__main__':
    unittest.main()
