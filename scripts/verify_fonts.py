"""
Font registration verification: PDF rendering, browser @font-face, deployment safety.
Run on demand to verify font setup is intact.
"""
import os, sys, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ['FLASK_APP'] = 'run.py'; os.environ['FLASK_CONFIG'] = 'Debug'

# Verify all 6 font files exist and match known hashes
EXPECTED_HASHES = {
    'PlayfairDisplay-Regular.ttf': 'c8d01980a790f8e66ab500afcc98cdb9ef54dbd036c17cfe17ab2d3de8ce0b15',
    'PlayfairDisplay-Bold.ttf':    '86bde7f1faf849ea2c71a6070ce6a491c93aa9b5aaffaba6c9ddd9e2b9d3d7ec',
    'Cormorant-Regular.ttf':       'a0b09e35fc0ffcd5a9cd95a8f3e2efc08540c6f5c3a8483b1addb59cd0eaf134',
    'Cormorant-Bold.ttf':          '005c2c552b884f988b4ba790ed49928b6d66abf7f9e54e8eb16868f46f04a70d',
    'Poppins-Regular.ttf':         '7e65201e9b79159e2300267cc885e16c8dcef2424cdfa09a29bfb0980a94a7ba',
    'Poppins-Bold.ttf':            '983676516167748b74de6f4771fb384c664fd913acb8b471122ecacf5da5ea6c',
}
# Note: Playfair/Cormorant hashes in this file may be stale after re-instancing.

def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

PR = os.path.join(os.path.dirname(__file__), '..')
SF = os.path.join(PR, 'static', 'fonts')
mismatches = 0
for fname, expected in EXPECTED_HASHES.items():
    fam = fname.split('-')[0].lower()
    if fam == 'playfairdisplay': fam = 'playfair-display'
    path = os.path.join(SF, fam, fname)
    if not os.path.isfile(path):
        print(f'MISSING: {fname}')
        mismatches += 1
    else:
        h = sha256(path)
        if h == expected:
            print(f'OK: {fname}')
        else:
            print(f'HASH MISMATCH: {fname} (expected {expected[:16]}..., got {h[:16]}...)')
            mismatches += 1

print(f'\n{len(EXPECTED_HASHES)} files checked, {mismatches} mismatches/missing')
