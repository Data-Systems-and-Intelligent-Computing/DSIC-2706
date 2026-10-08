import json

def inspect_notebook(path):
    print("=" * 60)
    print("NOTEBOOK:", path)
    print("=" * 60)
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)
    for idx, cell in enumerate(nb["cells"]):
        ctype = cell.get("cell_type")
        source = "".join(cell.get("source", []))
        print(f"\n[Cell {idx} - {ctype}]")
        print("CODE/MARKDOWN:")
        print(source.strip())
        outputs = cell.get("outputs", [])
        if outputs:
            print("--- OUTPUT ---")
            for out in outputs:
                if out.get("output_type") == "stream":
                    print("".join(out.get("text", [])).strip())
                elif out.get("output_type") in ("execute_result", "display_data"):
                    text_p = out.get("data", {}).get("text/plain", "")
                    if text_p:
                        print("".join(text_p).strip())

inspect_notebook("notebooks/E0_Pipeline_Sanity_Check.ipynb")
inspect_notebook("notebooks/E1_Clean_Retrieval.ipynb")
