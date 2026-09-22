import pymupdf
from collections import Counter
import re
from difflib import SequenceMatcher
import difflib

doc = pymupdf.open("/mnt/hdd/Projects/StudyOS/backend/uploads/system.pdf")
book = []

for page_number, page in enumerate(doc, start=1):
    blocks = page.get_text("blocks")

    blocks.sort(key=lambda block : block[1])
    book.append(blocks) 

"""so the book is list of element each element is
 page that is list of tuples and tuple represent block"""

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


top_blocks = [page[0] for page in book[50:150] if page]
bottom_blocks = [page[-1] for page in book[50:150] if page]


top_count = Counter(top_blocks)
bottom_count = Counter(bottom_blocks)

def blockWidth(blocks):
    for tup in blocks: #this is for width
        print(tup[3]-tup[1])
    print(isParaBlocked(book))
blockWidth(top_blocks)

def blockLength(blocks):
    beyond100 = 0
    for tup in blocks: #for find the len of the top block text
        if (len(tup[4]) >100 ):
            beyond100 += 1
    print(beyond100)




top_texts = [top_block[4] for top_block in top_blocks]
bottom_texts = [bottom_block[4] for bottom_block in bottom_blocks]
from collections import Counter

def normalize_line(line: str) -> str:
    """
    Normalize a line for repetition detection:
    - strip whitespace
    - remove trailing page-number-like tokens (pure digits)
    """
    s = line.strip()
    parts = s.split()
    
    # If the last token is just digits, assume it's a page number and drop it
    if parts and parts[-1].isdigit():
        parts = parts[:-1]
    
    # Also handle cases like "79\nHash tables" -> "79 Hash tables"
    # After split, "79" will be a separate token; if first token is digits, drop it too
    if parts and parts[0].isdigit():
        parts = parts[1:]
    
    return " ".join(parts)

def find_repeating_lines(texts,min_count):
    """
    Find lines that repeat across the list after normalization.
    
    Returns a list of (normalized_line, count, original_indices).
    """
    normalized = [normalize_line(t) for t in texts]
    counter = Counter(normalized)
    return counter.most_common() #list of tuples (text,frequency)

repeating = find_repeating_lines(bottom_texts, min_count=0)

# def header_detector(book):

