import pymupdf 

with open("../trial/frank.txt",'w+') as file:
    with pymupdf.open("../../uploads/frank.pdf") as pdf:
        for page_number,page in enumerate(pdf,start=1):
            file.write(f"===Page Number{page_number}===\n")
            file.write(page.get_text())