# import pymupdf
# from app.tryingFile.pdf_processing import text_extractor

# doc = pymupdf.open("/mnt/hdd/Projects/StudyOS/backend/uploads/system.pdf")
# book = []

# for page_number, page in enumerate(doc, start=1):
#     blocks = page.get_text("blocks")
#     blocks.sort(key=lambda block : block[1])
#     book.append(blocks) 


# bookPages = text_extractor(book)
# for  pageNumber,block in enumerate(bookPages,start=1):
#     print(f"Page number : {pageNumber},Blocks: {len(block)}")
#     for textNum,text in enumerate(block):
#         break


# response = await acompletion(
#     model="openai"
# )