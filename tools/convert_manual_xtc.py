"""Convert the manual EPUB into the downloadable XTC / XTCH files.

Uses the app's own converter (tategakiXTC_gui_core), with default typesetting,
so the files double as format-comparison data.  Needs the app repository:

    python tools/convert_manual_xtc.py <epub> <out_dir> --app <app repo> [--device x4|x3] [--format xtc|xtch]

Devices: x4 = 480x800, x3 = 528x792.  Both formats are made for both devices.
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
import time
from pathlib import Path

DEVICES = {'x4': (480, 800), 'x3': (528, 792)}
TITLE = '日本語XTC GUI Studio 操作マニュアル'
AUTHOR = '日本語XTC 開発チーム'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('epub', type=Path)
    parser.add_argument('out_dir', type=Path)
    parser.add_argument('--app', type=Path, required=True, help='path to the app repository')
    parser.add_argument('--device', choices=sorted(DEVICES), action='append')
    parser.add_argument('--format', choices=('xtc', 'xtch'), action='append')
    parser.add_argument('--name', default='nihongo-xtc-manual_v3.2')
    args = parser.parse_args()

    sandbox = Path(tempfile.mkdtemp(prefix='manual-xtc-'))
    (sandbox / 'appdata').mkdir()
    os.environ['TATEGAKI_XTC_APP_DATA_DIR'] = str(sandbox / 'appdata')
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    sys.path.insert(0, str(args.app))

    import tategakiXTC_gui_core as core

    font = args.app / 'font' / 'NotoSansJP-Regular.ttf'
    if not font.is_file():
        print('bundled font not found:', font, file=sys.stderr)
        return 1

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for device in args.device or sorted(DEVICES):
        width, height = DEVICES[device]
        for fmt in args.format or ('xtc', 'xtch'):
            # Same look as the manual that shipped with v3.1.2.9: horizontal text,
            # a generated cover, and a page number and progress bar for reading.
            conv = core.ConversionArgs(
                width=width, height=height, output_format=fmt,
                writing_mode='horizontal', font_size=22, line_spacing=32,
                page_number_enabled=True, progress_bar_enabled=True,
                cover_mode='generated',
                cover_title=TITLE, cover_author=AUTHOR,
                title_page_title=TITLE, title_page_author=AUTHOR,
                book_language='ja',
            )
            out = args.out_dir / f'{args.name}_{device}.{fmt}'
            started = time.time()
            core.process_epub(args.epub, font, conv, out)
            print(f'{out.name}: {out.stat().st_size / 1048576:.2f} MB in {time.time() - started:.0f}s')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
