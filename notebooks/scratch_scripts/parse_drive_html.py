import re

html_path = r"C:\Users\Fabio\.gemini\antigravity\brain\29c8c496-9c02-45a8-aece-af8d01cc9493\.system_generated\steps\505\content.md"
with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

labels = re.findall(r'aria-label="([^"]+)"', text)
unique_labels = sorted(list(set(labels)))
print("Total unique aria-labels found:", len(unique_labels))
for l in unique_labels:
    if any(k in l.lower() for k in ["folder", "file", "csv", "ipynb", "png", "data", "tugas", "check", "result", "note"]):
        print("  ->", l)

# Also check for jsdata or JSON array items
items = re.findall(r'\["([^"]+)",\["([^"]+)"\],"[^"]+","([^"]+)"', text)
print("\nPossible items:", len(items))
for it in items[:20]:
    print("  ->", it)
