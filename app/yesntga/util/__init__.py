import random
import os
import time
from logging import Logger
from flask import Response
from typing import Union
from werkzeug.datastructures import FileStorage
import io
import magic
import platform

# totally didn steal this from pep471
def get_tree_size(path):
    """Return total size of files in given path and subdirs."""
    total = 0
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            total += get_tree_size(entry.path)
        else:
            total += entry.stat(follow_symlinks=False).st_size
    return total

# Ref: https://stackoverflow.com/a/1094933
def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def rand_str(fn: str):
    """Makes an unique name using the input string as a seed"""
    l = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-'
    rng = random.Random(fn)
    return ''.join([l[rng.randint(0, len(l) - 1)] for _ in range(1, 12)])

def no_cache(r: Response, d: dict = None, **kwargs):
    r.headers = {**dict(r.headers), **d, **kwargs,
                 **{'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache'}}
    return r

def rb(f: Union[io.StringIO, io.BytesIO, FileStorage], b: int):
    pos = f.tell()
    i = f.read(b)
    f.seek(pos)
    return i

def mplat_mime(f: Union[io.StringIO, io.BytesIO, FileStorage]):
    """Multiplatform MIME identification, good for testing on Windows"""
    if platform.system() == "Windows":
        m = magic.Magic(magic_file="C:/magic.mgc", mime=True)
    else:
        m = magic.Magic(mime=True)
    return m.from_buffer(rb(f,4096))

def mplat_file_mime(f):
    """Lime mplat_mime() but for files"""
    if platform.system() == "Windows":
        m = magic.Magic(magic_file="C:/magic.mgc", mime=True)
    else:
        m = magic.Magic(mime=True)
    return m.from_file(f)

class TimeCap:
    def __init__(self, label: str, log_object: Logger):
        self.label = label
        self.lg = log_object
    def __enter__(self):
        self.init_time = time.time()
    def __exit__(self, type, value, traceback):
        self.lg.debug(f"Task {self.label} finished in {time.time()-self.init_time}")