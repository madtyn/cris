from fpdf import FPDF


# Instantiation of inherited class
PER_PAGE = 4
IMAGE_WIDTH = 28
IMAGE_HEIGHT = 21

LONG_LINE_WIDTH = 190
SHORT_LINE_WIDTH = 150

FONT_SIZE = 12
REGULAR_LINE_HEIGHT = 8
SEPARATOR_HEIGHT = 6


class PdfOutput(object):
    def __init__(self, name, logo='logo.png'):
        self.name = name
        self.num_receipts = 0
        self.pdf = FPDF()
        self.pdf.alias_nb_pages()
        self.pdf.set_font('Times', '', FONT_SIZE)
        self.logo = logo
        self._new_page()

    def _new_page(self):
        self.pdf.set_margins(0, 0)
        self.pdf.add_page()

    def write_receipt(self, receipt):
        if self.num_receipts > 0 and self.num_receipts % PER_PAGE == 0:
            self._new_page()
        self.pdf.image(self.logo, self.pdf.w - (IMAGE_WIDTH + 5), self.pdf.get_y() + 1, IMAGE_WIDTH, IMAGE_HEIGHT)

        for line in receipt.header():
            self.write_pdf_header(line)

        self.write_pdf_sep_line()

        for line in receipt.body():
            self.write_pdf_line(line)
        self.write_pdf_sep_line()

        for line in receipt.sign():
            self.write_pdf_line(line)

        self.pdf.dashed_line(self.pdf.get_x(), self.pdf.get_y(), self.pdf.w, self.pdf.get_y())
        self.num_receipts += 1

    def write_pdf_header(self, line):
        self.pdf.cell(SHORT_LINE_WIDTH, REGULAR_LINE_HEIGHT, line, 0, 1)

    def write_pdf_line(self, line):
        self.pdf.cell(LONG_LINE_WIDTH, REGULAR_LINE_HEIGHT, line, 0, 1)

    def write_pdf_sep_line(self):
        self.pdf.cell(SHORT_LINE_WIDTH, SEPARATOR_HEIGHT, '', 0, 1)

    def save(self):
        self.pdf.output(self.name, 'F')
