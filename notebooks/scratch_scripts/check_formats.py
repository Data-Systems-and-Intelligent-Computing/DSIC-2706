import os

ROOT = r"D:\FILE AND TASK\TA\data\xeno_canto"
ext_count = {}
non_mp3 = []

for root, dirs, files in os.walk(ROOT):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        ext_count[ext] = ext_count.get(ext, 0) + 1
        if ext not in ('.mp3', '.png', '.gitkeep', '.xlsx', '.py'):
            non_mp3.append(os.path.join(root, f))

print("=== Semua ekstensi file ===")
for k, v in sorted(ext_count.items()):
    label = k if k else "(no ext)"
    print(f"  {label}: {v} file")

print(f"\n=== File NON-MP3 audio ({len(non_mp3)} file) ===")
for f in non_mp3:
    print(f"  {f}")
