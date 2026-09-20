"""Build the manual's EPUB from README.md and docs/*.md.

The Web manual is the source of truth; the downloadable EPUB (and the XTC/XTCH
files converted from it) must say the same thing.  Run from anywhere:

    python tools/build_manual_epub.py <out.epub> [--version-label "v3.2"]

Structure follows the EPUB that shipped with v3.1.2.9: a cover page, one XHTML
per chapter, a nav document, and every screenshot at its original size.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import re
import sys
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

import markdown

ROOT = Path(__file__).resolve().parents[1]
nl_ = chr(10)
TITLE = '日本語XTC GUI Studio 操作マニュアル'
AUTHOR = '日本語XTC 開発チーム'

STYLE = """@charset "utf-8";
html { font-family: serif; }
body { margin: 0.8em; line-height: 1.7; }
h1 { font-size: 1.5em; margin: 1.2em 0 0.6em; border-bottom: 2px solid #444; padding-bottom: 0.25em; }
h2 { font-size: 1.2em; margin: 1.4em 0 0.5em; border-left: 5px solid #666; padding-left: 0.5em; }
h3 { font-size: 1.05em; margin: 1.2em 0 0.4em; }
p { margin: 0.6em 0; }
ul, ol { margin: 0.6em 0 0.8em 1.4em; padding: 0; }
li { margin: 0.25em 0; }
code { font-family: monospace; font-size: 0.92em; background: #eee; padding: 0 0.2em; }
blockquote { margin: 0.8em 0; padding: 0.5em 0.8em; background: #f2f2f2; border-left: 4px solid #888; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 0.9em; }
th, td { border: 1px solid #999; padding: 0.35em 0.5em; text-align: left; vertical-align: top; }
th { background: #eee; }
figure.shot { margin: 1em 0; page-break-inside: avoid; text-align: center; }
figure.shot img { max-width: 100%; border: 1px solid #999; }
figcaption { font-size: 0.82em; color: #555; margin-top: 0.3em; text-align: left; }
hr { border: none; border-top: 1px solid #bbb; margin: 1.4em 0; }
"""

IMG_RE = re.compile(r'!\[([^\]]*)\]\(\.\./images/([^)\s]+)\)')
LINK_RE = re.compile(r'\]\((?:\.\./)?(?:docs/)?(\d\d-[a-z0-9-]+)\.md(#[^)]*)?\)')
README_LINK_RE = re.compile(r'\[([^\]]+)\]\((?:\.\./)?README\.md(#[^)]*)?\)')
DOWNLOAD_LINK_RE = re.compile(r'\[([^\]]+)\]\((?:\.\./)?download/\)')
PARA_IMG_RE = re.compile(r'<p>(<img [^>]*/>)</p>')


def readme_section(text: str, heading: str) -> str:
    """The README part from `heading` up to the next same-level heading."""
    match = re.search(r'^(#{2,3}) ' + re.escape(heading) + r'.*$', text, re.M)
    if not match:
        raise SystemExit(f'README section not found: {heading}')
    level = len(match.group(1))
    tail = text[match.end():]
    end = re.search(r'^#{2,%d} ' % level, tail, re.M)
    return match.group(0) + (tail[:end.start()] if end else tail)


def front_matter() -> tuple[str, str, str]:
    """Chapter 0: what changed since v3.1.2, and how the a/b editions differ."""
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    parts = [readme_section(readme, 'v3.1.2 からの主な変更点'), readme_section(readme, '設定の並べ方が2通りあります')]
    text = '# このマニュアルについて' + nl_ + nl_ + nl_.join(p.strip() + nl_ for p in parts)
    # README sits one level above docs/, so its image paths need to look like docs/ ones.
    text = text.replace('](images/', '](../images/').replace('](docs/', '](')
    return '00-about', 'このマニュアルについて', text


def chapter_files() -> list[Path]:
    return sorted((ROOT / 'docs').glob('[0-9][0-9]-*.md'))


def first_heading(md_text: str, fallback: str) -> str:
    for line in md_text.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return fallback


def slug(text: str) -> str:
    """GitHub/Jekyll-style heading id, so the Web manual's #anchors also work in the book."""
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text).strip().lower()
    text = re.sub(r'[^\w\- ]', '', text, flags=re.UNICODE)
    return re.sub(r'\s+', '-', text)


def add_heading_ids(body: str) -> str:
    seen: dict[str, int] = {}

    def repl(m: re.Match) -> str:
        base = slug(m.group(2)) or 'section'
        count = seen.get(base, 0)
        seen[base] = count + 1
        ident = base if count == 0 else f'{base}-{count}'
        return f'<h{m.group(1)} id="{ident}">{m.group(2)}</h{m.group(1)}>'

    return re.sub(r'<h([1-6])>(.*?)</h\1>', repl, body, flags=re.S)


# Set by --device-width: build the plain 'for conversion to XTC' variant.
DEVICE_WIDTH = 0


def tables_to_lists(body: str) -> str:
    """The app's EPUB reader flows <table> into one paragraph, so turn each row into a list item.

    The first cell stays as the label; the remaining cells follow it.
    """
    def one_table(match: re.Match) -> str:
        rows = re.findall(r'<tr>(.*?)</tr>', match.group(0), flags=re.S)
        items = []
        for row in rows:
            cells = [re.sub(r'\s+', ' ', c).strip() for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', row, flags=re.S)]
            if not cells:
                continue
            if '<th' in row:
                shown = [c for c in cells if c]
                if shown:
                    items.append('<li><em>（' + ' ／ '.join(shown) + '）</em></li>')
                continue
            if len(cells) == 1:
                items.append(f'<li>{cells[0]}</li>')
            else:
                label = re.sub(r'</?strong>', '', cells[0])
                items.append('<li><strong>' + label + '</strong> … ' + ' ／ '.join(cells[1:]) + '</li>')
        return '<ul>' + ''.join(items) + '</ul>'

    return re.sub(r'<table>.*?</table>', one_table, body, flags=re.S)


def fit_image(src: Path, width: int) -> bytes:
    """A screenshot shrunk to the page width, as grayscale PNG (the device is monochrome)."""
    from io import BytesIO

    from PIL import Image

    image = Image.open(src)
    if image.width > width:
        image = image.resize((width, max(1, round(image.height * width / image.width))), Image.LANCZOS)
    buffer = BytesIO()
    gray = image.convert('L')
    # The screens are pale-on-white, which a 1-bit panel loses entirely. Push everything
    # lighter than the UI background to white and darken the rest so text and borders stay solid.
    gray = gray.point(lambda v: 255 if v >= 232 else int(255 * ((v / 232) ** 2.6)))
    gray.save(buffer, format='PNG', optimize=True)
    return buffer.getvalue()


def to_body(md_text: str) -> str:
    # Screenshots become <figure> so the caption stays with the picture.
    if DEVICE_WIDTH:
        md_text = IMG_RE.sub(lambda m: f'\n\n<p><img src="../images/{m.group(2)}" alt="{html.escape(m.group(1))}"/></p>\n\n<p>{html.escape(m.group(1))}</p>\n\n', md_text)
    else:
        md_text = IMG_RE.sub(lambda m: f'\n\n<figure class="shot"><img src="../images/{m.group(2)}" alt="{html.escape(m.group(1))}"/><figcaption>{html.escape(m.group(1))}</figcaption></figure>\n\n', md_text)
    # Chapter-to-chapter links point at the XHTML files inside the book.
    # The book carries the README's a/b section as chapter 0, so anchors stay valid.
    md_text = README_LINK_RE.sub(lambda m: f'[{m.group(1)}](../text/00-about.xhtml{m.group(2) or ""})' if m.group(2) else m.group(1), md_text)
    md_text = DOWNLOAD_LINK_RE.sub(lambda m: m.group(1), md_text)
    md_text = LINK_RE.sub(lambda m: f'](../text/{m.group(1)}.xhtml{m.group(2) or ""})', md_text)
    body = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'sane_lists', 'md_in_html'], output_format='xhtml')
    if DEVICE_WIDTH:
        body = tables_to_lists(body)
    return add_heading_ids(body)


def xhtml(title: str, body: str) -> str:
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja">\n<head>\n'
        '<meta charset="utf-8"/>\n'
        f'<title>{escape(title)}</title>\n'
        '<link rel="stylesheet" type="text/css" href="../style.css"/>\n</head>\n<body>\n'
        f'{body}\n</body>\n</html>\n'
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('out', type=Path)
    parser.add_argument('--version-label', default='v3.2')
    parser.add_argument('--date', default='', help='ISO timestamp; default is now (UTC)')
    parser.add_argument('--device-width', type=int, default=0,
                        help='plain variant for converting to XTC: shrink images to this width, tables become lists')
    args = parser.parse_args()
    global DEVICE_WIDTH
    DEVICE_WIDTH = args.device_width

    stamp = args.date or datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    chapters = []
    front_stem, front_title, front_text = front_matter()
    chapters.append((front_stem, front_title, to_body(front_text)))
    for path in chapter_files():
        text = path.read_text(encoding='utf-8')
        chapters.append((path.stem, first_heading(text, path.stem), to_body(text)))

    used_images: list[Path] = []
    seen = set()
    for _stem, _title, body in chapters:
        for name in re.findall(r'src="\.\./images/([^"]+)"', body):
            if name not in seen:
                seen.add(name)
                used_images.append(ROOT / 'images' / name)
    missing = [p for p in used_images if not p.is_file()]
    if missing:
        print('missing images:', ', '.join(p.name for p in missing), file=sys.stderr)
        return 1

    cover = (
        f'<h1>{escape(TITLE)}</h1>\n<p>対象バージョン: {escape(args.version_label)}</p>\n<p>{escape(AUTHOR)}</p>\n'
        '<p>このEPUBは、Webマニュアルと同じ内容を電子書籍としてまとめたものです。'
        '画面写真は原寸で収録しているため、リーダーの拡大機能で細部まで確認できます。</p>\n'
    )

    if DEVICE_WIDTH:
        cover = (
            f'<h1>{escape(TITLE)}</h1>' + nl_ + f'<p>対象バージョン: {escape(args.version_label)}</p>' + nl_
            + '<p>このファイルは、マニュアル本体を日本語XTC GUI Studio 自身で変換したものです。'
            + '画面写真は端末の画面幅に合わせて縮小されるため、細部を確認したいときは'
            + 'Web版（GitHub Pages）をご覧ください。</p>' + nl_
        )

    ident = uuid.uuid5(uuid.NAMESPACE_URL, 'https://miya-bee.github.io/nihongo--xtc-gui-studio-manual/')
    manifest = [
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '<item id="css" href="style.css" media-type="text/css"/>',
        '<item id="cover" href="text/cover.xhtml" media-type="application/xhtml+xml"/>',
    ]
    spine = ['<itemref idref="cover"/>']
    nav_items = [f'<li><a href="text/cover.xhtml">{escape(TITLE)}</a></li>']
    for stem, title, _body in chapters:
        manifest.append(f'<item id="{stem}" href="text/{stem}.xhtml" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{stem}"/>')
        nav_items.append(f'<li><a href="text/{stem}.xhtml">{escape(title)}</a></li>')
    for image in used_images:
        manifest.append(f'<item id="img-{hashlib.md5(image.name.encode()).hexdigest()[:8]}" href="images/{image.name}" media-type="image/png"/>')

    opf = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="ja">\n'
        '  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        f'    <dc:identifier id="bookid">urn:uuid:{ident}</dc:identifier>\n'
        f'    <dc:title>{escape(TITLE)}</dc:title>\n'
        f'    <dc:creator>{escape(AUTHOR)}</dc:creator>\n'
        '    <dc:language>ja</dc:language>\n'
        f'    <dc:date>{stamp}</dc:date>\n'
        f'    <meta property="dcterms:modified">{stamp}</meta>\n'
        '  </metadata>\n  <manifest>\n    ' + '\n    '.join(manifest) + '\n  </manifest>\n'
        '  <spine>\n    ' + '\n    '.join(spine) + '\n  </spine>\n</package>\n'
    )
    nav = (
        '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="ja" lang="ja">\n'
        '<head><meta charset="utf-8"/><title>目次</title></head>\n<body>\n'
        '  <nav epub:type="toc" id="toc">\n    <h1>目次</h1>\n    <ol>\n      '
        + '\n      '.join(nav_items) + '\n    </ol>\n  </nav>\n</body>\n</html>\n'
    )
    container = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
        '  <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>\n'
        '</container>\n'
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.out, 'w') as z:
        z.writestr(zipfile.ZipInfo('mimetype'), 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml', container, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr('OEBPS/content.opf', opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr('OEBPS/nav.xhtml', nav, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr('OEBPS/style.css', STYLE, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr('OEBPS/text/cover.xhtml', xhtml(TITLE, cover), compress_type=zipfile.ZIP_DEFLATED)
        for stem, title, body in chapters:
            z.writestr(f'OEBPS/text/{stem}.xhtml', xhtml(title, body), compress_type=zipfile.ZIP_DEFLATED)
        for image in used_images:
            if DEVICE_WIDTH:
                z.writestr(f'OEBPS/images/{image.name}', fit_image(image, DEVICE_WIDTH), compress_type=zipfile.ZIP_STORED)
            else:
                z.write(image, f'OEBPS/images/{image.name}', compress_type=zipfile.ZIP_STORED)
    print(f'wrote {args.out} ({args.out.stat().st_size / 1048576:.2f} MB): {len(chapters)} chapters, {len(used_images)} images')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
