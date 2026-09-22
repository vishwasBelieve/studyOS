import pymupdf

from try_ai import TextLine, parse_document


def extract_document(file_path: str):

    pages: list[list[TextLine]] = []

    with pymupdf.open(file_path) as pdf:

        for page_number, page in enumerate(
            pdf,
            start=1
        ):

            page_lines: list[TextLine] = []

            # dict preserves layout information
            data = page.get_text("dict")

            for block in data["blocks"]:

                # Ignore image blocks
                if block.get("type") != 0:
                    continue

                for line in block.get("lines", []):

                    spans = line.get("spans", [])

                    if not spans:
                        continue

                    text = "".join(
                        span.get("text", "")
                        for span in spans
                    ).strip()

                    if not text:
                        continue

                    bbox = line["bbox"]

                    # Use first span as representative typography
                    first_span = spans[0]

                    page_lines.append(
                        TextLine(
                            page_number=page_number,
                            text=text,

                            x0=bbox[0],
                            y0=bbox[1],
                            x1=bbox[2],
                            y1=bbox[3],

                            font_size=first_span.get(
                                "size",
                                0.0
                            ),

                            font_name=first_span.get(
                                "font",
                                ""
                            ),

                            is_bold=(
                                "bold"
                                in first_span.get(
                                    "font",
                                    ""
                                ).lower()
                            ),
                        )
                    )

            pages.append(page_lines)

    return parse_document(pages)

paragraphs = extract_document(
    "/mnt/hdd/Projects/StudyOS/backend/uploads/ai.pdf"
)

for paragraph in paragraphs[:20]:

    print("=" * 80)

    print(
        f"Pages: "
        f"{paragraph.page_start}"
        f"-"
        f"{paragraph.page_end}"
    )

    print(paragraph.text)

    