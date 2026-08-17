---
name: ingest-literature
description: Extracts key arguments from a new PDF in 00_Inbox and creates an interconnected Zettelkasten note in 01_Literature.
---

# Ingestion Workflow

When the user provides a PDF file name in `00_Inbox/`:

1. Run the terminal command:
   `python tools/pdf_parser.py 00_Inbox/<filename>`
2. Read the generated output file at `00_Inbox/.inbox_extracted.md`.
3. Create a new Markdown note in `01_Literature/<Paper_Author_Year>.md` with the following structure:
   - **YAML Frontmatter**: `tags`, `authors`, `year`, `citations`.
   - **Core Thesis**: 2–3 sentences summarizing the central argument.
   - **Key Findings & Methodology**: Bullet points of empirical or theoretical contributions.
   - **Connections & Wikilinks**: Connect ideas using `[[Wikilinks]]`. Prioritize the "EXISTING VAULT CONCEPTS" listed in the extraction file before creating new concepts.
4. If a major new concept is introduced that does not exist in `02_Concepts/`, create a brief atomic note for it in `02_Concepts/<Concept_Name>.md`.