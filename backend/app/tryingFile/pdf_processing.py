import pymupdf
from collections import Counter
import re
from difflib import SequenceMatcher
import difflib

#book is list of list (pages) and that pages contain tuple which represent each blocks
doc = pymupdf.open("/mnt/hdd/Projects/StudyOS/backend/uploads/frank.pdf")
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


top_blocks = [page[0] for page in book[50:150] if page]
bottom_blocks = [page[-1] for page in book[50:60] if page]


top_count = Counter(top_blocks)
bottom_count = Counter(bottom_blocks)

# for tup in top_blocks: #this is for width
#     print(tup[3]-tup[1])
# print(isParaBlocked(book))
# beyond100 = 0
# for tup in top_blocks: #for find the len of the top block text
#     if (len(tup[4]) >100 ):
#         beyond100 += 1
# print(isParaBlocked(book))

s1 = "Chapter 1: Introduction to methods"
s2 = "Chapter 2: Introduction to results"

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

def find_repeating_lines(texts):
    """
    Find lines that repeat across the list after normalization.
    
    Returns a list of (normalized_line, count, original_indices).
    """
    normalized = [normalize_line(t) for t in texts]
    counter = Counter(normalized)
    
    # Map normalized line -> list of original indices
    indices_map = {}
    for i, n in enumerate(normalized):
        indices_map.setdefault(n, []).append(i)

    result = [
        (line, count, indices_map[line])
        for line, count in counter.items()
        if count >= 0 and line  # skip empty lines if you want
    ]
    # Sort by frequency
    result.sort(key=lambda x: -x[1])
    return result



repeating = find_repeating_lines(bottom_texts, min_count=2)
print(repeating)
for line, count, indices in repeating:
    print(f"{count:2d}  {line!r}  -> indices {indices[:5]}...")  # show first few indices