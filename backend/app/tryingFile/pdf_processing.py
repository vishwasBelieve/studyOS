import pymupdf

with pymupdf.open("/mnt/hdd/Projects/StudyOS/backend/uploads/book3.pdf") as file:
    book = []
    for page in file:
        block = page.get_text("blocks")
        book.append(block)
singlePage = book[123]

def lineBlockOrParagraphBlock(page):
    for i in range(len(page)-1):
        currentBlock = page[i]
        nextBlock = page[i+1]
        dif = nextBlock[1] - currentBlock[1]
        line = 0
        paragaph = 0
        match dif:
            case lineCase if dif <= 30:
                line += 1
            case parCase if dif > 30:
                paragaph += 1
    typeOfDoc = "Line blocked" if line > paragaph else "Paragraph blocked"
    print(typeOfDoc)


def paragraphFromLine(page):
    pageStructure = [[]]
    line = []
    for i in range(len(page) - 1):
        currentBlock = page[i]
        nextBlock = page[i+1]
        dif = nextBlock[1] - currentBlock[1]
        if 18 <= dif <= 25:
            print("if block ran")
            line.append(currentBlock[4])
        else:
            line = []
            line.append(currentBlock[4])
            line = []
    return pageStructure

        
print(paragraphFromLine(singlePage))
        