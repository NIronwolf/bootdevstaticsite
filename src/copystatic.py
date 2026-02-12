import os
import shutil


def init_public():
    public = "public"
    static = "static"
    dirs = [(static, public)]
    if os.path.exists(public):
        shutil.rmtree(public)
    os.mkdir(public)
    if os.path.exists(static):
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
