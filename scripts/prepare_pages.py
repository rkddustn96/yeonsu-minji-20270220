"""Set absolute social-preview URLs in the Pages deployment checkout."""
import html
import os
from pathlib import Path
import re
from urllib.parse import urlparse


def prepare(source: str, site_url: str) -> str:
    site_url = site_url.rstrip('/')
    parsed = urlparse(site_url)
    if parsed.scheme != 'https' or not parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError('SITE_URL must be an absolute HTTPS website URL')
    image_url = html.escape(site_url + '/img/og.jpg?v=3', quote=True)
    source, count = re.subn(
        r'<meta property="og:image" content="[^"]*">',
        lambda _: f'<meta property="og:image" content="{image_url}">',
        source,
    )
    if count != 1:
        raise ValueError('Expected exactly one og:image tag')
    source = re.sub(r'\n<meta property="og:url" content="[^"]*">', '', source)
    canonical = html.escape(site_url + '/', quote=True)
    return source.replace('<meta property="og:type" content="website">',
                          '<meta property="og:type" content="website">\n'
                          f'<meta property="og:url" content="{canonical}">')


if __name__ == '__main__':
    path = Path(__file__).resolve().parents[1] / 'web' / 'index.html'
    path.write_text(prepare(path.read_text(encoding='utf-8'), os.environ['SITE_URL']), encoding='utf-8')
