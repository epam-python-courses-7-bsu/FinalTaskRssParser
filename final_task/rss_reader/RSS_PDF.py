from fpdf import FPDF


class PDF(FPDF):
    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
