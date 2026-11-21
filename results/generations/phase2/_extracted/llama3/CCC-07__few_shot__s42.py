"""Download addresses of the files of a text simplification dataset.

Public entry point: run(name). Do not change its name or signature; the rest
of the file may be freely reorganized.
"""

_URL_LIST = [
    (
        'human_ratings.csv',
        'https://raw.githubusercontent.com/facebookresearch/asset/main/human_ratings/human_ratings.csv',
    ),
    (
        'asset.valid.orig',
        'https://raw.githubusercontent.com/facebookresearch/asset/main/dataset/asset.valid.orig',
    ),
    (
        'asset.test.orig',
        'https://raw.githubusercontent.com/facebookresearch/asset/main/dataset/asset.test.orig',
    ),
]

_URLs = _URL_LIST[:]

for spl in ['valid', 'test']:
    for i in range(10):
        _URLs.append((f'asset.{spl}.simp.{i}', f'https://raw.githubusercontent.com/facebookresearch/asset/main/dataset/asset.{spl}.simp.{i}'))

def run(name):
    """Returns the download address of the named file. Public entry point of
    this unit."""
    return _URLs[name]
