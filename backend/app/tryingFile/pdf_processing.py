import pymupdf
from collections import Counter
import re
from difflib import SequenceMatcher

#book is list of list (pages) and that pages contain tuple which represent each blocks
doc = pymupdf.open("/mnt/hdd/Projects/StudyOS/backend/uploads/system.pdf")
book = []
for page_number, page in enumerate(doc, start=1):
    blocks = page.get_text("blocks")

    blocks.sort(key=lambda block : block[1])
    book.append(blocks)
def y0_difference(page):
    difference_list = []
    for i  in range(1,len(page)):
        prev_block = page[i-1][1]  
        next_block = page[i][1]
        block_height = page[i-1][3] - page[i-1][1] 
        difference = next_block - prev_block
        # print(f"block height = {block_height}")
        difference_list.append(difference)
    count_large = sum(x > 29 for x in difference_list)
    count_small = sum(x < 29 for x in difference_list)
    return (count_large,count_small)

def isParaBlocked(book):
    total_small = 0
    total_large = 0
    for page in book:
        large,small = y0_difference(page)
        total_large += large
        total_small += small
    if total_large > total_small:
        return True
    else:
        return False


top_blocks = [page[0] for page in book[50:60] if page]
bottom_blocks = [page[-1] for page in book[50:60] if page]


top_count = Counter(top_blocks)
bottom_count = Counter(bottom_blocks)

print(top_blocks)
print(bottom_blocks)
