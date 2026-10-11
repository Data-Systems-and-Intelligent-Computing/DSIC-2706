import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

nb_path = r"D:\FILE AND TASK\TA\notebooks\EDA_Tugas_Akhir.ipynb"

try:
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    print(f"Total sel dalam notebook: {len(nb.get('cells', []))}")
    for i, cell in enumerate(nb.get("cells", [])):
        cell_type = cell.get("cell_type")
        source = "".join(cell.get("source", []))[:100].replace("\n", " ")
        outputs = cell.get("outputs", [])
        output_summary = []
        for o in outputs:
            otype = o.get("output_type")
            if otype == "stream":
                output_summary.append("text: " + "".join(o.get("text", []))[:60].replace("\n", " "))
            elif otype in ["display_data", "execute_result"]:
                data_keys = list(o.get("data", {}).keys())
                output_summary.append(f"{otype} ({', '.join(data_keys)})")
            elif otype == "error":
                ename = o.get("ename")
                evalue = o.get("evalue")
                output_summary.append(f"ERROR: {ename} - {evalue}")
        print(f"\n--- Sel {i+1} [{cell_type}] ---")
        print(f"Code preview : {source}")
        print(f"Output ({len(outputs)} item): {output_summary}")

except Exception as e:
    print(f"Error inspecting notebook: {e}")
