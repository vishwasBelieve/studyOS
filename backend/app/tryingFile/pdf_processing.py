import pymupdf
from collections import Counter
import re

# doc = pymupdf.open("/mnt/hdd/Projects/StudyOS/backend/uploads/system.pdf")
# book = []

# for page_number, page in enumerate(doc, start=1):
#     blocks = page.get_text("blocks")
    
#     blocks.sort(key=lambda block : block[1])
#     book.append(blocks) 
"""so the book is list of element each element is
 page that is list of tuples and tuple represent block"""
def y0_difference(page):
    difference_list = []
    for i  in range(1,len(page)):
        prev_block = page[i-1][1]  
        next_block = page[i][1]
        block_height = page[i-1][3] - page[i-1][1] 
        difference = next_block - prev_block
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

# top_blocks = [page[0] for page in book[150:250] if page]
# bottom_blocks = [page[-1] for page in book[50:150] if page]

# top_count = Counter(top_blocks)
# bottom_count = Counter(bottom_blocks)

def blockWidth(blocks,numberOfPages):
    numLargeWidth = 0
    for tup in blocks: #this is for width
        width = tup[3]-tup[1]
        if(width > 35):
            numLargeWidth += 1
    if (numLargeWidth > numberOfPages/4):
        return False #the block are bigger than footer and header should be
    return True #mean the block smaller so they could be header and footer

def blockLength(blocks,numberOfPages): #when it return true it means blocks are  header or footer
    beyond100 = 0
    for tup in blocks:
        #for find the len of the top block text
        if (len(tup[4]) > 100):
            beyond100 += 1
    if (beyond100 > numberOfPages/2):
        return False #doesn't have header
    else :
        return True #has header


# top_texts = [top_block[4] for top_block in top_blocks]
# bottom_texts = [bottom_block[4] for bottom_block in bottom_blocks]


def normalize_line(line: str) -> str:
    """
    Normalize a line for repetition detection:
    - strip whitespace
    - remove trailing page-number-like tokens (pure digits)
    """
    s = line.strip()

    result = re.sub(r'^\d+|\d+$', '', s)
    s = result
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

# repeating = find_repeating_lines(top_texts, min_count=0)
def header_scorrer(top_blocks,top_texts,numberOfPages):
        headerPointLen = 0
        headerPointWidth = 0
        headerPointRepeat = 0
        
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
            if ((first+second+third) > numberOfPages/4):
                headerPointRepeat += 1
            
            else:
                headerPointRepeat -= 1
        else:
            if(len(freqList) <= 2):
                if (freqList[0] > numberOfPages/2):
                    headerPointRepeat += 1
        
        
        if(blockLength(top_blocks,numberOfPages)):
            headerPointLen += 1
        else:
            headerPointLen -= 1
        if(blockWidth(top_blocks,numberOfPages)):
            headerPointWidth += 1
        else:
            headerPointWidth -= 1
        return (headerPointLen,headerPointRepeat,headerPointWidth)


def footer_scorrer(bottom_blocks,bottom_texts,numberOfPages):
        footerPointLen = 0
        footerPointWidth = 0
        footerPointRepeat = 0
        
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
            if ((first+second+third) > numberOfPages/4):
                footerPointRepeat += 1
            
            else:
                footerPointRepeat -= 1
        else:
            if(len(freqList) <= 2):
                if (freqList[0] > numberOfPages/2):
                    footerPointRepeat += 1
        
        
        if(blockLength(bottom_blocks,numberOfPages)):
            footerPointLen += 1
        else:
            footerPointLen -= 1
        if(blockWidth(bottom_blocks,numberOfPages)):
            footerPointWidth += 1
        else:
            footerPointWidth -= 1
        return (footerPointLen,footerPointRepeat,footerPointWidth)

WEIGHTS = (0.2, 1.0, 0.6)


def score_maker(book,batch_size):
    if(not isParaBlocked(book)):
        print("Can't process this book")
        return None
    # if (not isParaBlocked(book)):
    #     return
    numberOfBatches = 0
    headerPointRepeat = 0
    headerPointLen = 0
    headerPointWidth = 0
    footerPointRepeat = 0
    footerPointLen = 0
    footerPointWidth = 0   

    for i in range(0,len(book),batch_size):
        numberOfBatches += 1
        batch = book[i:i+batch_size]
        top_blocks = [page[0] for page in batch if page] #list of tuples of top blocks
        bottom_blocks = [page[-1] for page in batch if page] #list of tupoles of bottom blocks
        top_texts = [top_block[4] for top_block in top_blocks] #list of top text
        bottom_texts = [bottom_block[4] for bottom_block in bottom_blocks]
        newLenH,newRepH,newWidH = header_scorrer(top_blocks,top_texts,batch_size)
        headerPointLen += newLenH
        headerPointRepeat += newRepH
        headerPointWidth += newWidH
        newLenF,newRepF,newWidF = footer_scorrer(bottom_blocks,bottom_texts,batch_size)
        footerPointLen += newLenF
        footerPointRepeat += newRepF
        footerPointWidth += newWidF
    headerScores = (headerPointLen,headerPointRepeat,headerPointWidth)
    footerScores = (footerPointLen,footerPointRepeat,footerPointWidth)
    return (numberOfBatches,headerScores,footerScores)
    
    
# nBatch,headerTup,footerTup = score_maker(book,100)

def detector(headerScore, footerScore, numberOfBatches):

    header_ratio = tuple(
        x / numberOfBatches
        for x in headerScore
    )

    footer_ratio = tuple(
        x / numberOfBatches
        for x in footerScore
    )

    header_score = sum(
        value * weight
        for value, weight in zip(header_ratio, WEIGHTS)
    )

    footer_score = sum(
        value * weight
        for value, weight in zip(footer_ratio, WEIGHTS)
    )



    return header_score > 0, footer_score > 0


def text_extractor(book):
    
    nBatch,headerTup,footerTup = score_maker(book,100)
    header,footer = detector(headerTup,footerTup,nBatch)
    bookTexts = []
    for page in book:
        pageTexts = []
        for i in range(len(page)):
            if header and i == 0:
                continue
            if footer and i == (len(page) - 1):
                continue
            text = page[i][4].replace('\n','').strip()
            if(not len(text)):
                continue
            pageTexts.append(text)
        bookTexts.append(pageTexts)
    return bookTexts


        
        



