#!/usr/bin/env python3
"""Reassemble the original research ZIP; verify every part and the whole."""
from pathlib import Path
import hashlib
import json

PARTS = [{'filename': '11_Full_Research_Archive.zip.001', 'bytes': 61820918, 'sha256': '03d5a93343bebe4b3d4b7a0e8bb41cb2578383851acfab1d2d9c31db1f3c7886'}, {'filename': '11_Full_Research_Archive.zip.002', 'bytes': 61820918, 'sha256': '38e7a24cb2fd9e077c879ce25d1ecbc570a8f0f847595a1999baac10dc7ea3c8'}, {'filename': '11_Full_Research_Archive.zip.003', 'bytes': 61820918, 'sha256': '282871ed17e028828031b4cae66ce253440a3611929a47d5682b0da06efb04b8'}, {'filename': '11_Full_Research_Archive.zip.004', 'bytes': 61820918, 'sha256': '369a630b48fc89c4edc8a588c35b8f0389da163c452bafeca31061d7aa067fdc'}, {'filename': '11_Full_Research_Archive.zip.005', 'bytes': 61820918, 'sha256': 'c3eebe8480e19ed92b07db24cb8719cd753e6ddde6ea296207fc4bffa1d5259b'}, {'filename': '11_Full_Research_Archive.zip.006', 'bytes': 61820918, 'sha256': '33daabfaa01eeac5b938332b6829776d093da00e0e72ea19c6c581cc0d44bc0b'}, {'filename': '11_Full_Research_Archive.zip.007', 'bytes': 61820918, 'sha256': 'a2771930741e79db0323e5be3499fb8f747b6371c273f78edbc8f4d21c82314e'}, {'filename': '11_Full_Research_Archive.zip.008', 'bytes': 61820918, 'sha256': 'd0059b5845b9eadfa502c8f4c58c70d415a334b2a7252db31df42bc06a0cdaeb'}, {'filename': '11_Full_Research_Archive.zip.009', 'bytes': 61820918, 'sha256': '205337abda29c6e8ef3b0ba8283661a8e2c2d95bdc8271ac25240920fb375602'}, {'filename': '11_Full_Research_Archive.zip.010', 'bytes': 61820918, 'sha256': '4c5703576e68c7d1f5347cce67c2333b65943cd9930fa393e291e4c5703a7778'}, {'filename': '11_Full_Research_Archive.zip.011', 'bytes': 61820918, 'sha256': '09fc7ecb1b3c01f71bfe7cf412230a3dda1c1481becfdff86b45c93fb892864f'}, {'filename': '11_Full_Research_Archive.zip.012', 'bytes': 61820918, 'sha256': '3ae84b1e945db6b393ad309c878159be8946141f6bec089af3c88c030514a107'}, {'filename': '11_Full_Research_Archive.zip.013', 'bytes': 61820915, 'sha256': '49fb3cc7954c086f4eb66b96e5a9d2d5a22a2225d762f8fed8b096b87293bdca'}]
EXPECTED = 'cc352f8fa4a3220f1d37f995efc8c135bcf71cac0e2ef06e56b0ce4238c46824'
NAME = '11_Full_Research_Archive.zip'
ROOT = Path(__file__).resolve().parent

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(8*1024*1024), b''):
            h.update(block)
    return h.hexdigest()

def main():
    output = ROOT / NAME
    if output.exists():
        if sha(output) != EXPECTED:
            raise SystemExit('Existing ZIP differs; move it aside before retrying. Nothing overwritten.')
        print('Existing ZIP verified: ' + str(output))
        return
    for p in PARTS:
        path = ROOT / p['filename']
        if not path.is_file() or path.stat().st_size != p['bytes'] or sha(path) != p['sha256']:
            raise SystemExit('Missing or damaged part: ' + p['filename'])
    temporary = ROOT / (NAME + '.assembling')
    if temporary.exists():
        raise SystemExit('An earlier .assembling file exists; move it aside before retrying.')
    h = hashlib.sha256()
    with temporary.open('xb') as out:
        for p in PARTS:
            print('Joining ' + p['filename'], flush=True)
            with (ROOT / p['filename']).open('rb') as src:
                for block in iter(lambda: src.read(8*1024*1024), b''):
                    out.write(block)
                    h.update(block)
    if h.hexdigest() != EXPECTED:
        raise SystemExit('Whole-archive verification failed; .assembling retained for inspection.')
    temporary.rename(output)
    print('VERIFIED: ' + str(output))
    print('SHA-256: ' + EXPECTED)
    print('Extract this ZIP, then follow its README.')

if __name__ == '__main__':
    main()
