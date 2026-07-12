"""
Source fonts from google/fonts, instance variable fonts, place with OFL.txt.
"""
import os, sys, hashlib, json, shutil, subprocess, tempfile, requests
from pathlib import Path

PR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_FONTS = os.path.join(PR, 'static', 'fonts')
GOOGLE_FONTS_SHA = 'ec0464b978de222073645d6d3366f3fdf03376d8'

# Source URLs pinned to exact commit SHA
RAW = 'https://raw.githubusercontent.com/google/fonts/' + GOOGLE_FONTS_SHA

SOURCES = {
    'playfair-display': {
        'files': {
            'PlayfairDisplay[wght].ttf': f'{RAW}/ofl/playfairdisplay/PlayfairDisplay[wght].ttf',
            'OFL.txt': f'{RAW}/ofl/playfairdisplay/OFL.txt',
        },
        'type': 'variable',
        'var_file': 'PlayfairDisplay[wght].ttf',
        'variations': {
            'PlayfairDisplay-Regular.ttf': 'wght=400',
            'PlayfairDisplay-Bold.ttf': 'wght=700',
        },
    },
    'cormorant': {
        'files': {
            'Cormorant[wght].ttf': f'{RAW}/ofl/cormorant/Cormorant[wght].ttf',
            'OFL.txt': f'{RAW}/ofl/cormorant/OFL.txt',
        },
        'type': 'variable',
        'var_file': 'Cormorant[wght].ttf',
        'variations': {
            'Cormorant-Regular.ttf': 'wght=400',
            'Cormorant-Bold.ttf': 'wght=700',
        },
    },
    'poppins': {
        'files': {
            'Poppins-Regular.ttf': f'{RAW}/ofl/poppins/Poppins-Regular.ttf',
            'Poppins-Bold.ttf': f'{RAW}/ofl/poppins/Poppins-Bold.ttf',
            'OFL.txt': f'{RAW}/ofl/poppins/OFL.txt',
        },
        'type': 'static',
    },
}

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def download(url, dest):
    print(f'  Downloading {os.path.basename(dest)}...')
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    with open(dest, 'wb') as f:
        f.write(r.content)
    return dest

provenance = []

tmpdir = tempfile.mkdtemp(prefix='fonts_')

for family, cfg in SOURCES.items():
    print(f'\n=== {family} ===')
    fam_dir = os.path.join(tmpdir, family)
    os.makedirs(fam_dir, exist_ok=True)
    src_hashes = {}

    for fname, url in cfg['files'].items():
        dest = os.path.join(fam_dir, fname)
        download(url, dest)
        h = sha256(dest)
        src_hashes[fname] = h
        print(f'  SHA256 {fname}: {h}')

    if cfg['type'] == 'variable':
        var_path = cfg['var_file']
        var_full = os.path.join(fam_dir, var_path)
        var_hash = src_hashes[var_path]
        print(f'  Source variable hash: {var_hash}')

        for out_name, axis_arg in cfg['variations'].items():
            out_path = os.path.join(fam_dir, out_name)
            cmd = [
                sys.executable, '-m', 'fontTools.varLib.instancer',
                var_full, axis_arg,
                '--output', out_path,
                '--update-name-table',
            ]
            print('  Instancing {}: {}'.format(out_name, ' '.join(cmd[-6:])))
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f'  ERROR: {result.stderr}')
                sys.exit(1)
            # Normalize metadata for reproducibility
            from fontTools.ttLib import TTFont
            import fontTools.misc.timeTools as _ttTimeTools
            _orig_now = _ttTimeTools.timestampNow
            _ttTimeTools.timestampNow = lambda: 2082844800  # fixed timestamp: 2036-01-01
            try:
                font = TTFont(out_path)
                name_records = [(r.nameID, r.toUnicode()) for r in font['name'].names if r.nameID in (1, 2, 4, 6)]
                print(f'  name table: {name_records}')
                os2 = font['OS/2']
                print(f'  usWeightClass: {os2.usWeightClass}')
                assert os2.usWeightClass in (400, 700), f'Unexpected weight: {os2.usWeightClass}'
                font.save(out_path)
                font.close()
            finally:
                _ttTimeTools.timestampNow = _orig_now
            out_hash = sha256(out_path)
            print(f'  Normalized SHA256 {out_name}: {out_hash}')

            provenance.append({
                'family': family,
                'file': out_name,
                'source_var': var_path,
                'source_hash': var_hash,
                'output_hash': out_hash,
                'normalized': True,
                'weight': os2.usWeightClass,
                'instancer_cmd': ' '.join(cmd),
                'name_table_updated': True,
                'type': 'instanced',
            })

    else:  # static
        for fname in cfg['files']:
            if fname == 'OFL.txt':
                continue
            h = src_hashes[fname]
            # Validate
            from fontTools.ttLib import TTFont
            font = TTFont(os.path.join(fam_dir, fname))
            name_records = [(r.nameID, r.toUnicode()) for r in font['name'].names if r.nameID in (1, 2, 4, 6)]
            print(f'  name table: {name_records}')
            os2 = font['OS/2']
            print(f'  usWeightClass: {os2.usWeightClass}')
            font.close()
            provenance.append({
                'family': family,
                'file': fname,
                'source_var': None,
                'source_hash': h,
                'output_hash': h,
                'weight': os2.usWeightClass,
                'instancer_cmd': None,
                'name_table_updated': False,
                'type': 'static',
            })

# Place files
print(f'\n=== PLACING FILES ===')
for family, cfg in SOURCES.items():
    target_dir = os.path.join(STATIC_FONTS, family)
    os.makedirs(target_dir, exist_ok=True)
    for fname in cfg['files']:
        src = os.path.join(tmpdir, family, fname)
        dst = os.path.join(target_dir, fname)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f'  {dst}')
    # Also copy instanced files
    if cfg['type'] == 'variable':
        for out_name in cfg['variations']:
            src = os.path.join(tmpdir, family, out_name)
            dst = os.path.join(target_dir, out_name)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                print(f'  {dst}')

# Print provenance table
print(f'\n=== PROVENANCE TABLE ===')
for p in provenance:
    print('-' * 60)
    for k, v in p.items():
        print(f'  {k}: {v}')

# Save provenance JSON
with open(os.path.join(PR, 'tmp_font_provenance.json'), 'w') as f:
    json.dump(provenance, f, indent=2)
print(f'\nProvenance saved to tmp_font_provenance.json')

# Cleanup tmp
shutil.rmtree(tmpdir, ignore_errors=True)
print(f'\nDone!')
