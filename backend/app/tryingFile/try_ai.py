from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------
# Data structures
# ---------------------------------------------------------

@dataclass
class TextLine:
    page_number: int
    text: str

    x0: float
    y0: float
    x1: float
    y1: float

    font_size: float = 0.0
    font_name: str = ""
    is_bold: bool = False

    @property
    def height(self) -> float:
        return self.y1 - self.y0

    @property
    def width(self) -> float:
        return self.x1 - self.x0


@dataclass
class Paragraph:
    text: str
    page_start: int
    page_end: int

    lines: list[TextLine] = field(default_factory=list)


# ---------------------------------------------------------
# Basic text helpers
# ---------------------------------------------------------

def normalize_text(text: str) -> str:
    """
    Clean obvious extraction artifacts without destroying
    meaningful text.
    """

    text = text.replace("\u00ad", "")  # soft hyphen
    text = text.replace("\xa0", " ")

    # Collapse repeated whitespace
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def ends_sentence(text: str) -> bool:
    """
    Rough sentence-ending signal.

    This is NOT used as a hard rule.
    """

    text = text.rstrip()

    return bool(
        re.search(
            r'[.!?]["\')\]]?$',
            text
        )
    )


def starts_with_lowercase(text: str) -> bool:
    text = text.lstrip()

    if not text:
        return False

    return text[0].islower()


def ends_with_hyphen(text: str) -> bool:
    return text.rstrip().endswith("-")


def join_lines(previous: str, current: str) -> str:
    """
    Join two PDF lines intelligently.

    Handles:
        "transfor-"
        "mation"

    as:

        "transformation"
    """

    previous = previous.rstrip()
    current = current.lstrip()

    if previous.endswith("-"):
        return previous[:-1] + current

    return previous + " " + current


# ---------------------------------------------------------
# Header / footer detection
# ---------------------------------------------------------

def detect_repeated_headers_footers(
    pages: list[list[TextLine]],
    minimum_occurrences: int = 3,
) -> set[str]:
    """
    Detect text that appears repeatedly near the top/bottom
    of multiple pages.

    Example:

        AI Engineering
        17

    appearing on many pages.

    We remove these before paragraph reconstruction.
    """

    occurrences: dict[str, int] = {}

    for page_lines in pages:

        if not page_lines:
            continue

        page_height = max(line.y1 for line in page_lines)

        top_lines = [
            line
            for line in page_lines
            if line.y0 < page_height * 0.12
        ]

        bottom_lines = [
            line
            for line in page_lines
            if line.y1 > page_height * 0.88
        ]

        seen_on_page = set()

        for line in top_lines + bottom_lines:

            text = normalize_text(line.text)

            if not text:
                continue

            seen_on_page.add(text)

        for text in seen_on_page:
            occurrences[text] = occurrences.get(text, 0) + 1

    return {
        text
        for text, count in occurrences.items()
        if count >= minimum_occurrences
    }


# ---------------------------------------------------------
# Line relationship scoring
# ---------------------------------------------------------

def alignment_score(a: TextLine, b: TextLine) -> float:
    """
    How strongly are the two lines horizontally aligned?
    """

    difference = abs(a.x0 - b.x0)

    if difference <= 2:
        return 1.0

    if difference <= 5:
        return 0.8

    if difference <= 10:
        return 0.5

    return 0.0


def font_score(a: TextLine, b: TextLine) -> float:

    if not a.font_size or not b.font_size:
        return 0.5

    difference = abs(a.font_size - b.font_size)

    if difference <= 0.5:
        return 1.0

    if difference <= 1:
        return 0.7

    if difference <= 2:
        return 0.3

    return 0.0


def vertical_gap_score(a: TextLine, b: TextLine) -> float:

    gap = b.y0 - a.y1

    # Normal line spacing
    if gap <= max(a.height, b.height) * 0.6:
        return 1.0

    # Slightly larger spacing
    if gap <= max(a.height, b.height) * 1.2:
        return 0.7

    # Probably paragraph break
    if gap <= max(a.height, b.height) * 2:
        return 0.3

    return 0.0


def indentation_score(a: TextLine, b: TextLine) -> float:

    difference = abs(a.x0 - b.x0)

    if difference <= 3:
        return 1.0

    if difference <= 10:
        return 0.6

    return 0.2


def punctuation_score(a: TextLine, b: TextLine) -> float:
    """
    Important distinction:

        "The model works by"

    strongly suggests continuation.

        "The model works."

    suggests a boundary.

    """

    text = a.text.rstrip()

    if not text:
        return 0.0

    if text.endswith((",", ";", ":", "(", "[", "{")):
        return 1.0

    if text.endswith(("-", "—")):
        return 1.0

    if ends_sentence(text):
        return 0.2

    return 0.7


def continuation_score(a: TextLine, b: TextLine) -> float:
    """
    Linguistic signal that b continues a.
    """

    score = 0.0

    if starts_with_lowercase(b.text):
        score += 0.35

    if a.text.rstrip().endswith(
        (",", ";", ":", "(", "[", "{", "-", "—")
    ):
        score += 0.35

    if not ends_sentence(a.text):
        score += 0.20

    return min(score, 1.0)


# ---------------------------------------------------------
# Main decision function
# ---------------------------------------------------------

def should_merge(
    previous: TextLine,
    current: TextLine,
) -> tuple[bool, float]:
    """
    Decide whether two lines belong to the same paragraph.

    Returns:

        (merge?, confidence)
    """

    # -----------------------------------------------------
    # Never merge across pages here.
    # Cross-page merging is handled separately.
    # -----------------------------------------------------

    if previous.page_number != current.page_number:
        return False, 0.0

    alignment = alignment_score(previous, current)
    vertical = vertical_gap_score(previous, current)
    font = font_score(previous, current)
    indentation = indentation_score(previous, current)
    punctuation = punctuation_score(previous, current)
    continuation = continuation_score(previous, current)

    score = (
        alignment * 0.25
        + vertical * 0.20
        + font * 0.10
        + indentation * 0.10
        + punctuation * 0.15
        + continuation * 0.20
    )

    # Strong evidence of a new paragraph
    if vertical == 0.0:
        return False, score

    # Strong indentation change
    if indentation < 0.3 and continuation < 0.5:
        return False, score

    # Confident merge
    if score >= 0.65:
        return True, score

    return False, score


# ---------------------------------------------------------
# Same-page paragraph reconstruction
# ---------------------------------------------------------

def build_page_paragraphs(
    lines: list[TextLine],
) -> list[Paragraph]:

    if not lines:
        return []

    lines = sorted(
        lines,
        key=lambda line: line.y0
    )

    paragraphs: list[Paragraph] = []

    current_lines: list[TextLine] = [lines[0]]

    for current in lines[1:]:

        previous = current_lines[-1]

        merge, confidence = should_merge(
            previous,
            current
        )

        if merge:

            current_lines.append(current)

        else:

            paragraphs.append(
                Paragraph(
                    text="",
                    page_start=current_lines[0].page_number,
                    page_end=current_lines[-1].page_number,
                    lines=current_lines,
                )
            )

            current_lines = [current]

    # Flush final paragraph
    if current_lines:

        paragraphs.append(
            Paragraph(
                text="",
                page_start=current_lines[0].page_number,
                page_end=current_lines[-1].page_number,
                lines=current_lines,
            )
        )

    # Convert lines → text
    for paragraph in paragraphs:

        text = ""

        for line in paragraph.lines:

            if not text:
                text = line.text

            else:
                text = join_lines(
                    text,
                    line.text
                )

        paragraph.text = normalize_text(text)

    return paragraphs


# ---------------------------------------------------------
# Cross-page paragraph merging
# ---------------------------------------------------------

def can_continue_across_page(
    previous: Paragraph,
    current: Paragraph,
) -> bool:

    if previous.page_end + 1 != current.page_start:
        return False

    previous_text = previous.text.rstrip()
    current_text = current.text.lstrip()

    if not previous_text or not current_text:
        return False

    # If previous page ends with obvious continuation
    if (
        previous_text.endswith(
            (",", ";", ":", "(", "[", "{", "-", "—")
        )
    ):
        return True

    # If it doesn't end a sentence
    if not ends_sentence(previous_text):
        return True

    # Lowercase beginning is strong evidence
    if starts_with_lowercase(current_text):
        return True

    return False


def merge_cross_page_paragraphs(
    paragraphs: list[Paragraph],
) -> list[Paragraph]:

    if not paragraphs:
        return []

    result: list[Paragraph] = []

    current = paragraphs[0]

    for next_paragraph in paragraphs[1:]:

        if can_continue_across_page(
            current,
            next_paragraph
        ):

            current.text = join_lines(
                current.text,
                next_paragraph.text
            )

            current.page_end = next_paragraph.page_end
            current.lines.extend(
                next_paragraph.lines
            )

        else:

            result.append(current)
            current = next_paragraph

    result.append(current)

    return result


# ---------------------------------------------------------
# Full document parser
# ---------------------------------------------------------

def parse_document(
    pages: list[list[TextLine]],
) -> list[Paragraph]:

    # -----------------------------------------------------
    # Detect repeated headers / footers
    # -----------------------------------------------------

    repeated = detect_repeated_headers_footers(pages)

    cleaned_pages: list[list[TextLine]] = []

    for page_lines in pages:

        cleaned = []

        for line in page_lines:

            text = normalize_text(line.text)

            if not text:
                continue

            if text in repeated:
                continue

            line.text = text

            cleaned.append(line)

        cleaned_pages.append(cleaned)

    # -----------------------------------------------------
    # Build paragraphs page-by-page
    # -----------------------------------------------------

    paragraphs: list[Paragraph] = []

    for page_lines in cleaned_pages:

        page_paragraphs = build_page_paragraphs(
            page_lines
        )

        paragraphs.extend(page_paragraphs)

    # -----------------------------------------------------
    # Merge paragraphs split across pages
    # -----------------------------------------------------

    paragraphs = merge_cross_page_paragraphs(
        paragraphs
    )

    return paragraphs