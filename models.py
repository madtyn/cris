
import datetime as dt
from enum import Enum

from indexes import FIRST_MONTH_COL, COLS_PER_MONTH


class Months(Enum):
    OCTOBER = ('Octubre', 10)
    NOVEMBER = ('Noviembre', 11)
    DECEMBER = ('Diciembre', 12)
    JANUARY = ('Enero', 1)
    FEBRUARY = ('Febrero', 2)
    MARCH = ('Marzo', 3)
    APRIL = ('Abril', 4)
    MAY = ('Mayo', 5)
    JUNE = ('Junio', 6)
    JULY = ('Julio', 7)
    AUGUST = ('Agosto', 8)
    SEPTEMBER = ('Septiembre', 9)

    def __new__(cls, *args, **kwargs):
        idx = FIRST_MONTH_COL + (len(cls.__members__) * COLS_PER_MONTH)
        obj = object.__new__(cls)
        obj._value_ = idx
        obj.processed_idx = idx
        obj.number_idx = idx + 1
        obj.quota_idx = idx + 2
        obj.trans = args[0]
        obj.ordinal = args[1]
        return obj

    @classmethod
    def get_month(cls, ordinal):
        for m in cls:
            if ordinal == m.ordinal:
                return f'{m!s}'

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __str__(self):
        return self.trans


class Receipt(object):
    tag = """----------------
Nombre del escolar: {student}
Número de recibo: {number}
Precio mensualidad: {quota}
    
{teacher}, con NIF {nif}, ha recibido de los responsables del alumno/a anteriormente\n
citado las cantidades que se desglosan en este recibo en concepto de pago de la actividad "{activity}",\n
realizada durante el curso {school_year}\n
    
A Coruña, {day} de {month} del {year}
----------------
"""

    def __init__(self, teacher, nif, student, rec_number, quota):
        self.teacher = teacher
        self.nif = nif
        self.student = student
        self.number = rec_number
        self.quota = quota

    def template(self):
        d = {
            'teacher': self.teacher,
            'nif': self.nif,
            'student': self.student,
            'number': self.number,
            'quota': self.quota,
            'day': dt.datetime.today().day,
            'month': Months.get_month(dt.datetime.today().month),
            'year': dt.datetime.today().year
        }

        return self.tag.format(d)


if __name__ == '__main__':
    print()
    print()
    print()
