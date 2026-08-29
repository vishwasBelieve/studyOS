import pymupdf

with pymupdf.open("/mnt/hdd/Projects/StudyOS/backend/uploads/book3.pdf") as file:
    book = []
    for page in file:
        block = page.get_text("blocks")
        book.append(block)
singlePage = book[123]

def lineBlockOrParagraphBlock(result):
    for i in range(len(result)-1):
        currentBlock = result[i]
        nextBlock = result[i+1]
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

lineBlockOrParagraphBlock(singlePage)

