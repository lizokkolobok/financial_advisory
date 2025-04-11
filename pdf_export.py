from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "LLM Financial Advisor Report", ln=True, align="C")
        self.ln(10)

    def section_title(self, title):
        self.set_font("Arial", "B", 14)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def section_body(self, text):
        self.set_font("Arial", "", 12)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 8, text)
        self.ln()

def create_pdf(profile_text, advice_text, filename="financial_advice_report.pdf"):
    pdf = PDFReport()
    pdf.add_page()

    pdf.section_title("User Profile")
    pdf.section_body(profile_text)

    pdf.section_title("Investment Advice")
    pdf.section_body(advice_text)

    pdf.output(filename)
    return filename
