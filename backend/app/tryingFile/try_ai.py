from google import genai
from app.core.config import settings
from app.tryingFile.pdf_processing import book_pages
import json

client = genai.Client(api_key=settings.GEMINI_API_KEY)




singleString = ""
for pages in book_pages[150:250]:
    singleString += f"\nPAGE {pages['page_number']}:\n{pages['text']}\n"

def clean_text(singleString):
    prompt = f"""
        Clean the following extracted PDF text.

    For each page:
    - Remove headers, footers, and page numbers when they are clearly part of the page layout rather than the actual content.
    - Fix obvious PDF extraction problems such as words incorrectly split across lines.
    - Join lines that belong to the same paragraph.
    - Preserve the original wording and meaning.
    - Do NOT summarize.
    - Do NOT rewrite or add content.
    - Do NOT remove meaningful content.
    - Preserve headings, chapter titles, quotations, and other meaningful structure.
    - Use the PAGE X markers only to determine which text belongs to which page.
    - Do not include the PAGE X markers inside the returned text.
    - Fix words that were accidentally joined together during PDF extraction.
    -Return ONLY valid JSON.
    - Normalize all PDF extraction whitespace.
    - Remove unnecessary line breaks within sentences and paragraphs.
    - Merge lines that belong to the same paragraph.
    - Remove extra blank lines.
    - Fix words that were accidentally split apart or joined together by PDF extraction.
    - Preserve a single blank line between separate paragraphs.
    - Do not remove meaningful paragraph breaks.
    - Do not preserve formatting from the raw PDF unless it represents meaningful document structure.
    -Each page must have exactly two fields:
    - page_number
    - text

    -Return the result as a JSON array.

    -Each page must have exactly two fields:
    - page_number
    - text

    Example:
    [
    {{
        "page_number": 1,
        "text": "cleaned text..."
    }},
    {{
        "page_number": 2,
        "text": "cleaned text..."
    }}
    ]

    TEXT:
    {singleString}
    """

    response = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    output = response.output_text
    print(repr(output[:500]))

    clean_pages = json.loads(output)

    return clean_pages

print(clean_text(singleString))

