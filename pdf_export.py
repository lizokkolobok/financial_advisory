from fpdf import FPDF
import os

def create_pdf(profile_text, advice, filename="financial_advice_report.pdf"):
    pdf = FPDF()
    pdf.add_page()

    # Updated font path
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "DejaVuSans.ttf"))
    if not os.path.exists(font_path):
        raise FileNotFoundError("DejaVuSans.ttf font file is required in the project root directory.")

    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.multi_cell(0, 10, "Financial Profile:\n" + profile_text)
    pdf.ln(5)
    pdf.multi_cell(0, 10, "Personalized Advice:\n" + advice)

    pdf.output(filename)

