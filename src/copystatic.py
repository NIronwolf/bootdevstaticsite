import os
import shutil


def init_public(src: str = "static", dst: str = "public"):
    dirs = [(src, dst)]
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    if os.path.exists(src):
        while dirs:
            current_src, current_dst = dirs.pop()
            for entry in os.listdir(current_src):
                src_path = os.path.join(current_src, entry)
                dst_path = os.path.join(current_dst, entry)
                if os.path.isdir(src_path):
                    dirs.append((src_path, dst_path))
                    if not os.path.isdir(dst_path):
                        os.mkdir(dst_path)
                elif os.path.isfile(src_path):
                    shutil.copy2(src_path, dst_path)
