import os
import shutil

src_root = "motorBikeLES/postProcessing/y0Plane"
dst_root = "forParaview/y0Plane"

os.makedirs(dst_root, exist_ok=True)

datasets = []

for name in os.listdir(src_root):
    src_dir = os.path.join(src_root, name)

    if not os.path.isdir(src_dir):
        continue

    try:
        t = float(name)
    except ValueError:
        continue

    src_file = os.path.join(src_dir, "y0.vtp")
    if not os.path.exists(src_file):
        continue

    index = int(round(t * 1000))
    dst_name = f"{index:04d}.vtp"
    dst_file = os.path.join(dst_root, dst_name)

    print(f"{src_file} -> {dst_file}")
    shutil.copy2(src_file, dst_file)

    datasets.append((t, dst_name))

# --- pvd ファイル作成 ---
datasets.sort()

pvd_path = os.path.join(dst_root, "y0Plane.pvd")

with open(pvd_path, "w") as f:
    f.write('<?xml version="1.0"?>\n')
    f.write('<VTKFile type="Collection" version="0.1">\n')
    f.write('  <Collection>\n')

    for t, fname in datasets:
        f.write(f'    <DataSet timestep="{t}" file="{fname}"/>\n')

    f.write('  </Collection>\n')
    f.write('</VTKFile>\n')

print("PVD file written to:", pvd_path)