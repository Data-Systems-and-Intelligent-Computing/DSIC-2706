import struct
import os

BYTES_PER_SEC = 512
SEC_PER_CLUS = 16
CLUS_SIZE = BYTES_PER_SEC * SEC_PER_CLUS # 8192
DATA_OFFSET = 16777216 # Sector 32768 * 512

def cluster_to_offset(cluster):
    return DATA_OFFSET + (cluster - 2) * CLUS_SIZE

with open(r"\\.\E:", "rb") as f:
    # Read FAT table to follow cluster chains if needed
    fat_offset = 2822 * 512
    # Let's inspect root directory cluster (Cluster 2)
    f.seek(cluster_to_offset(2))
    root_data = f.read(CLUS_SIZE * 4) # read first 4 clusters of root dir

print("=== Scanning Root Directory for Entries ===")
for i in range(0, len(root_data), 32):
    entry = root_data[i:i+32]
    first_byte = entry[0]
    if first_byte == 0x00:
        continue # End of dir
    is_deleted = (first_byte == 0xE5)
    attr = entry[11]
    name = entry[:11]
    first_clus_hi = struct.unpack("<H", entry[20:22])[0]
    first_clus_lo = struct.unpack("<H", entry[26:28])[0]
    first_clus = (first_clus_hi << 16) | first_clus_lo
    size = struct.unpack("<I", entry[28:32])[0]
    
    if attr == 0x0F: # LFN
        continue
    
    status = "DELETED" if is_deleted else "ACTIVE"
    try:
        short_name = name.decode('latin1', errors='replace')
    except:
        short_name = str(name)
    
    if first_clus > 0 or size > 0 or is_deleted:
        print(f"[{status}] Name: {short_name!r} | Attr: 0x{attr:02X} | Clus: {first_clus} | Size: {size}")
