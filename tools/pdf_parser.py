import sys
import os
import pymupdf4llm
from pathlib import Path

INBOX_DIR = Path("00_Inbox")
CONCEPTS_DIR = Path("02_Concepts")
TEMP_OUTPUT_FILE = Path("00_Inbox/.inbox_extracted.md")

def get_existing_concepts():
    """Returns a list of all existing concept notes to prevent duplicate tags."""
    if not CONCEPTS_DIR.exists():
        return []
    return [f.stem for f in CONCEPTS_DIR.glob("*.md")]

def parse_pdf(file_path_str):
    file_path = Path(file_path_str)
    if not file_path.exists():
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    print(f"Parsing PDF: {file_path.name}...")
    try:
        # Extract markdown text from PDF
        md_text = pymupdf4llm.to_markdown(str(file_path))
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        sys.exit(1)

    existing_concepts = get_existing_concepts()
    concepts_str = ", ".join(f"[[{c}]]" for c in existing_concepts) if existing_concepts else "None yet"

    # Write structured output to a temporary file for Copilot to read directly
    with open(TEMP_OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# RAW SOURCE EXTRACTION: {file_path.name}\n\n")
        f.write("## EXISTING VAULT CONCEPTS (PREFER THESE FOR WIKILINKS):\n")
        f.write(f"{concepts_str}\n\n")
        f.write("## EXTRACTED DOCUMENT CONTENT:\n\n")
        f.write(md_text)

    print(f"Extraction successful! Extracted content written to: {TEMP_OUTPUT_FILE}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/pdf_parser.py 00_Inbox/<filename.pdf>")
        sys.exit(1)
    parse_pdf(sys.argv[1])