import pymupdf

with pymupdf.open("/mnt/hdd/Projects/StudyOS/backend/uploads/book4.pdf") as file:
    book = []
    for page in file:
        block = page.get_text("blocks")
        book.append(block)
singlePage = book[125]
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
    pageStructure = []

    for i in range(len(page)):
        currentBlock = page[i]

        # First line always starts a paragraph
        if i == 0:
            pageStructure.append([currentBlock[4]])
            continue

        previousBlock = page[i - 1]

        dif = currentBlock[1] - previousBlock[1]

        if 18 <= dif <= 25:
            # Same paragraph
            pageStructure[-1].append(currentBlock[4])
        else:
            # New paragraph
            pageStructure.append([currentBlock[4]])

    return pageStructure