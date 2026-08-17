import sys
import os
import re
from pathlib import Path

VAULT_DIR = Path(".")  # Searches all subdirectories in current workspace
CONTEXT_OUTPUT_FILE = Path("00_Inbox/.search_context.md")

def get_all_vault_notes():
    """Recursively collects all markdown notes from 01_Literature and 02_Concepts."""
    notes = {}
    search_dirs = [Path("01_Literature"), Path("02_Concepts")]
    for d in search_dirs:
        if d.exists():
            for filepath in d.rglob("*.md"):
                with open(filepath, "r", encoding="utf-8") as f:
                    notes[filepath.stem] = (filepath, f.read())
    return notes

def clean_wikilink(raw_link):
    """Handles aliases and section headers: [[Concept|Alias]] -> Concept, [[Concept#Section]] -> Concept"""
    link = raw_link.split("|")[0]
    link = link.split("#")[0]
    return link.strip()

def search_graph(query):
    notes = get_all_vault_notes()
    if not notes:
        print("No notes found in 01_Literature/ or 02_Concepts/.")
        return

    query_terms = query.lower().split()
    matched_nodes = set()

    # 1. Base keyword match
    for title, (path, content) in notes.items():
        combined = f"{title.lower()} {content.lower()}"
        if any(term in combined for term in query_terms):
            matched_nodes.add(title)

    if not matched_nodes:
        print(f"No notes matched the query: '{query}'")
        return

    # 2. Graph Traversal (1-Hop via clean wikilinks)
    traversed_nodes = set(matched_nodes)
    link_pattern = re.compile(r'\[\[(.*?)\]\]')

    for node in matched_nodes:
        _, content = notes[node]
        raw_links = link_pattern.findall(content)
        for raw in raw_links:
            target = clean_wikilink(raw)
            if target in notes:
                traversed_nodes.add(target)

    # 3. Write structured context file
    with open(CONTEXT_OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# GRAPH SEARCH CONTEXT FOR QUERY: '{query}'\n")
        f.write(f"Matched {len(matched_nodes)} primary notes | Traversed {len(traversed_nodes)} total connected notes.\n\n")
        
        for node in traversed_nodes:
            path, content = notes[node]
            f.write(f"## File: {path}\n")
            f.write(f"{content}\n\n{'='*40}\n\n")

    print(f"Search complete! Retrieved {len(traversed_nodes)} connected notes. Context written to: {CONTEXT_OUTPUT_FILE}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python tools/graph_search.py "YOUR RESEARCH QUESTION"')
        sys.exit(1)
    search_graph(" ".join(sys.argv[1:]))