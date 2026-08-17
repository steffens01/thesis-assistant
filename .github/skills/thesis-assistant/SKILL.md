---
name: thesis-assistant
description: Performs graph-aware retrieval across 01_Literature and 02_Concepts to answer research and thesis questions with citations.
---

# Research Assistant Workflow

When the user asks a thesis or literature question:

1. Run the terminal command:
   `python tools/graph_search.py "<USER QUERY>"`
2. Read the resulting context file at `00_Inbox/.search_context.md`.
3. Synthesize an academic answer answering the query:
   - Base your claims strictly on the retrieved primary and connected notes.
   - Cite the exact note filenames in parentheses, e.g., `(Smith_2023.md)`.
   - Highlight where different papers agree, disagree, or use contrasting methodologies.