import pymupdf

with pymupdf.open("../trial/frank.pdf") as pdf:
    page_count = len(pdf)
    with open("../trial/frank.text","w+",encoding="utf-8") as file:
        for page_number,page in enumerate(pdf):
            file.write(f"\n\n==== PAGE {page_number} ====\n\n")
            file.write(page.get_text())
        
