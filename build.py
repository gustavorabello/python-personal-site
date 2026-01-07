# -*- coding: utf-8 -*-
"""
build.py — site builder (Python 2.7 compatible)

Optimized, structured and highly visual output.
Compatible with Hyde + Python 2.7.15
"""

from __future__ import print_function

import os
import fnmatch
import re
import shutil
import subprocess
import time
from datetime import datetime, timedelta

# ============================================================
# ANSI colors (Python 2.7 friendly)
# ============================================================

class C:
    END  = '\033[0m'
    BOLD = '\033[1m'

    BLUE   = '\033[94m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    RED    = '\033[91m'
    MAG    = '\033[95m'
    DIM    = '\033[2m'


def title(msg):
    print(C.MAG + C.BOLD + "\n✨ " + msg + C.END)

def info(msg):
    print(C.BLUE + "ℹ  " + msg + C.END)

def ok(msg):
    print(C.GREEN + "✔  " + msg + C.END)

def warn(msg):
    print(C.YELLOW + "⚠  " + msg + C.END)

def err(msg):
    print(C.RED + "✖  " + msg + C.END)

def step(msg):
    print(C.BLUE + "➡  " + msg + C.END)

def hr():
    print(C.DIM + "-" * 70 + C.END)


# ============================================================
# Config
# ============================================================

TABS_HTML_DIR = "content/media/html/tabs"
MUSICS_DIR    = "content/musics"
PUBLIC_DIR    = "./gustavorabello.github.io"

DUP_SUFFIXES = [' 2.html', ' 3.html', ' 4.html', ' 5.html']


# ============================================================
# Helpers
# ============================================================

def run(cmd, cwd=None):
    step("Running command")
    print(C.DIM + "   $ " + " ".join(cmd) + C.END)
    if cwd:
        print(C.DIM + "   cwd: " + cwd + C.END)
    ret = subprocess.call(cmd, cwd=cwd)
    if ret != 0:
        raise RuntimeError("Command failed: " + " ".join(cmd))


def split_camel(name):
    """
    sambaEPagode -> Samba E Pagode
    oMeuLugar    -> O Meu Lugar
    """
    parts = re.sub(r'(?<=.)([A-Z])', r' \1', name).split()
    return " ".join(p.capitalize() for p in parts)


# ============================================================
# Tasks
# ============================================================

def remove_duplicates(root='.'):
    title("Removing duplicate HTML files")
    count = 0

    for dirpath, dirnames, filenames in os.walk(root):
        for fname in filenames:
            for suf in DUP_SUFFIXES:
                if fname.endswith(suf):
                    path = os.path.join(dirpath, fname)
                    try:
                        os.remove(path)
                        ok("Removed: " + path)
                        count += 1
                    except Exception as e:
                        warn("Failed removing " + path + ": " + str(e))
                    break

    hr()
    ok("Total removed: %d" % count)


def populate_music_db():
    title("Populating music database")

    if not os.path.isdir(TABS_HTML_DIR):
        err("Tabs directory not found: " + TABS_HTML_DIR)
        return

    # Clear musics dir
    if os.path.isdir(MUSICS_DIR):
        warn("Cleaning musics directory")
        for d in os.listdir(MUSICS_DIR):
            full = os.path.join(MUSICS_DIR, d)
            if os.path.isdir(full):
                shutil.rmtree(full)
                ok("Deleted: " + full)
    else:
        os.makedirs(MUSICS_DIR)

    count = 0
    now = datetime.now()

    for artist in sorted(os.listdir(TABS_HTML_DIR)):
        artist_dir = os.path.join(TABS_HTML_DIR, artist)
        if not os.path.isdir(artist_dir):
            continue

        for fname in sorted(os.listdir(artist_dir)):
            if not fname.endswith(".html"):
                continue

            basename = os.path.splitext(fname)[0]

            artist_pretty = split_camel(artist)
            title_pretty  = split_camel(basename)

            out_dir = os.path.join(MUSICS_DIR, artist)
            if not os.path.isdir(out_dir):
                os.makedirs(out_dir)

            ts = now - timedelta(seconds=count)
            timestamp = ts.strftime("%Y-%m-%d %H:%M:%S")

            out_file = os.path.join(out_dir, basename + ".html")
            f = open(out_file, "w")
            f.write("---\n")
            f.write("artist: %s\n" % artist_pretty)
            f.write("title: %s\n" % title_pretty)
            f.write("type: music\n")
            f.write("dir: html/tabs/%s/%s.html\n" % (artist, basename))
            f.write("created: !!timestamp '%s'\n" % timestamp)
            f.write("---\n")
            f.close()

            count += 1
            if count <= 10 or count % 50 == 0:
                ok("Music: %s — %s" % (artist_pretty, title_pretty))

    hr()
    ok("Total musics generated: %d" % count)


def gen_site():
    title("Generating website")

    if os.path.exists(PUBLIC_DIR):
        warn("Cleaning public directory")
        for name in os.listdir(PUBLIC_DIR):
            if name in ('.git', '.gitignore'):
                continue
            path = os.path.join(PUBLIC_DIR, name)
            if os.path.isdir(path):
                shutil.rmtree(path)
                ok("Deleted dir: " + name)
            else:
                os.remove(path)
                ok("Deleted file: " + name)
    else:
        os.makedirs(PUBLIC_DIR)

    run(['hyde', 'gen'])
    ok("Website generated")


def update_page():
    title("Publishing to GitHub")

    run(['git', 'pull'], cwd=PUBLIC_DIR)
    run(['git', 'add', '.'], cwd=PUBLIC_DIR)

    ret = subprocess.call(
        ['git', 'commit', '-a', '-m', 'updating site.'],
        cwd=PUBLIC_DIR
    )
    if ret != 0:
        warn("Nothing to commit")

    run(['git', 'push'], cwd=PUBLIC_DIR)
    ok("Website published")


# ============================================================
# Main
# ============================================================

def main():
    title("Gustavo's Build Pipeline (Python 2.7)")

    remove_duplicates()
    populate_music_db()
    gen_site()
    update_page()

    hr()
    ok("All done running build.py")


if __name__ == "__main__":
    main()
