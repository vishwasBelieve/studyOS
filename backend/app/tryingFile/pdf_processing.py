import pymupdf
from collections import Counter
from difflib import SequenceMatcher


doc = pymupdf.open("/mnt/hdd/Projects/StudyOS/backend/uploads/data.pdf")
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

def blockWidth(blocks,batch_size):
    numLargeWidth = 0
    for tup in blocks: #this is for width
        width = tup[3]-tup[1]
        if(width > 35):
            numLargeWidth += 1
    if (numLargeWidth > batch_size/2):
        return True
    return False
print(blockWidth(top_blocks,3))

def blockLength(topblocks,batchSize):
    beyond100 = 0
    for tup in topblocks: #for find the len of the top block text
        if (len(tup[4]) >100):
            beyond100 += 1
    if (beyond100 > batchSize/4):
        return False #doesn't have header
    else :
        return True #has header



top_texts = [top_block[4] for top_block in top_blocks]
bottom_texts = [bottom_block[4] for bottom_block in bottom_blocks]


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
    return counter.values() #list of tuples (text,frequency)

repeating = find_repeating_lines(bottom_texts, min_count=0)

def header_processor(top_blocks,top_texts,batch_size):
    # headerPointLen = 0
    # headerPointWidth = 0
    # numberOfBatches = 0

    # for i in range(0,len(book),batch_size):
    #     numberOfBatches += 1
    #     batch = book[i:i+batch_size]
    #     top_blocks = [page[0] for page in batch[:] if page]
    #     bottom_blocks = [page[-1] for page in batch[:] if page]
    #     top_texts = [top_block[4] for top_block in top_blocks]
    #     bottom_texts = [bottom_block[4] for bottom_block in bottom_blocks]
        repeats = find_repeating_lines(top_texts,0)
        freqList = [freq for freq in repeats]
        freqList.sort(reverse=True)
        if(len(freqList) > 3):
            first,second,third,*rest = freqList
            if first + second + third > 15:
                headerPointReapt += 1;
            else:
                headerPointReapt -= 1;
        if(blockLength(top_blocks,batch_size)):
            headerPointLen += 1
        else:
            headerPointLen -= 1
        if(blockWidth(top_blocks,batch_size)):
            headerPointWidth += 1
        else:
            headerPointWidth -= 1
        
            
    # print("Header point for length", headerPointLen)
    # print("Header point for repeats", headerPointReapt)
    # print("Header point for width", headerPointWidth)
    # print("number of batches", numberOfBatches)

def bottom_processor(bottom_blocks,bottom_texts,batch_size):
        # headerPointLen = 0
    # headerPointWidth = 0
    # numberOfBatches = 0

    # for i in range(0,len(book),batch_size):
    #     numberOfBatches += 1
    #     batch = book[i:i+batch_size]
    #     top_blocks = [page[0] for page in batch[:] if page]
    #     bottom_blocks = [page[-1] for page in batch[:] if page]
    #     top_texts = [top_block[4] for top_block in top_blocks]
    #     bottom_texts = [bottom_block[4] for bottom_block in bottom_blocks]
        repeats = find_repeating_lines(bottom_texts,0)
        freqList = [freq for freq in repeats]
        freqList.sort(reverse=True)
        if(len(freqList) > 3):
            first,second,third,*rest = freqList
            if first + second + third > 15:
                footerPointReapt += 1;
            else:
                footerPointReapt -= 1;
        if(blockLength(bottom_blocks,batch_size)):
            footerPointLen += 1
        else:
            footerPointLen -= 1
        if(blockWidth(bottom_blocks,batch_size)):
            footerPointWidth += 1
        else:
            footerPointWidth -= 1
        
            
    # print("Header point for length", headerPointLen)
    # print("Header point for repeats", headerPointReapt)
    # print("Header point for width", headerPointWidth)
    # print("number of batches", numberOfBatches)


def header_detector(book,batch_size):
    # if (not isParaBlocked(book)):
    #     return
    
    headerPointReapt = 0
    headerPointLen = 0
    headerPointWidth = 0
    numberOfBatches = 0

    for i in range(0,len(book),batch_size):
        numberOfBatches += 1
        batch = book[i:i+batch_size]
        top_blocks = [page[0] for page in batch[:] if page]
        bottom_blocks = [page[-1] for page in batch[:] if page]
        top_texts = [top_block[4] for top_block in top_blocks]
        bottom_texts = [bottom_block[4] for bottom_block in bottom_blocks]
        repeats = find_repeating_lines(top_texts,0)
        freqList = [freq for freq in repeats]
        freqList.sort(reverse=True)
        if(len(freqList) > 3):
            first,second,third,*rest = freqList
            if first + second + third > 15:
                headerPointReapt += 1;
            else:
                headerPointReapt -= 1;
        if(blockLength(top_blocks,batch_size)):
            headerPointLen += 1
        else:
            headerPointLen -= 1
        if(blockWidth(top_blocks,batch_size)):
            headerPointWidth += 1
        else:
            headerPointWidth -= 1
        
            
    print("Header point for length", headerPointLen)
    print("Header point for repeats", headerPointReapt)
    print("Header point for width", headerPointWidth)
    print("number of batches", numberOfBatches)

    
header_detector(book,50)

        

