import pymupdf
import re

with pymupdf.open("/mnt/hdd/Projects/StudyOS/backend/uploads/book2.pdf") as file:
    book = []
    for page in file:
        block = page.get_text("blocks")
        book.append(block)
singlePage = book[159]


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
            pageStructure.append([currentBlock[4].strip('\n')])
            continue

        previousBlock = page[i - 1]

        dif = currentBlock[1] - previousBlock[1]

        if dif <= 25:
            # Same paragraph
            pageStructure[-1].append(currentBlock[4].strip("\n"))
        else:
            # New paragraph
            pageStructure.append([currentBlock[4].strip('\n')])

    return pageStructure

def paragraphBlockedToText(page):
    pageStructure = []
    for block in page:
        pageStructure.append([re.sub("\n","",block[4])])
    return pageStructure

print(len(paragraphBlockedToText(singlePage)),paragraphBlockedToText(singlePage))
    