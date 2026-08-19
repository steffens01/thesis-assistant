import re
from pathlib import Path

INDEX_FILE = Path("INDEX.md")
SEARCH_DIRS = [Path("01_Literature"), Path("02_Concepts")]

def extract_summary(content):
    """Extracts a short 1-line summary or core thesis from the note."""
    # Look for a Core Thesis section or the first paragraph after YAML frontmatter
    body = re.sub(r'^---[\s\S]*?---\n', '', content).strip()
    lines = [line.strip() for line in body.split('\n') if line.strip() and not line.startswith('#')]
    if lines:
        summary = lines[0]
        return (summary[:120] + '...') if len(summary) > 120 else summary
    return "No summary available."

def build_index():
    entries = {"01_Literature": [], "02_Concepts": []}

    for directory in SEARCH_DIRS:
        if directory.exists():
            for file in sorted(directory.glob("*.md")):
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read()
                summary = extract_summary(content)
                entries[directory.name].append(f"- [[{file.stem}]]: {summary}")

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write("# Knowledge Base Index (Map of Content)\n\n")
        f.write("> Auto-generated index for quick navigation and AI agent orientation.\n\n")
        
        f.write("## 📚 Literature Notes\n")
        f.write("\n".join(entries["01_Literature"]) if entries["01_Literature"] else "- None yet.")
        
        f.write("\n\n## 💡 Core Concepts\n")
        f.write("\n".join(entries["02_Concepts"]) if entries["02_Concepts"] else "- None yet.")
        f.write("\n")

    print(f"INDEX.md successfully updated with {len(entries['01_Literature']) + len(entries['02_Concepts'])} entries.")

if __name__ == "__main__":
    build_index()