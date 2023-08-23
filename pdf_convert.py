# from pypdf import PdfReader
#
# reader = PdfReader("menu_toti.pdf")
#
# parts = {}
#
#
# def visitor_body(text, cm, tm, font_dict, font_size):
#
#         parts[text] = font_size
#
#
# page = reader.pages[0]
# page.extract_text(visitor_text=visitor_body)
#
# #
# print(parts)


# for page_num in range(len(reader.pages)):
#     page = reader.pages[page_num]
#     page.extract_text(visitor_text=visitor_body())
import pdfplumber

import pdfplumber

with pdfplumber.open("menu_toti.pdf") as pdf:
    first_page = pdf.pages[0]
    print(first_page.extract_text_lines(strip=True))



