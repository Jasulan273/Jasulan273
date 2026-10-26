"""Render the public GitHub contribution calendar; Python standard library only."""
from pathlib import Path
from html.parser import HTMLParser
from datetime import date
from urllib.request import Request, urlopen
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'td' and a.get('data-date') and a.get('data-level'):
            self.days.append({'date': a['data-date'], 'level': int(a['data-level'])})

def render(days):
    days = sorted(days, key=lambda d: d['date'])
    if len(days) < 300:
        raise ValueError('Incomplete GitHub calendar; keeping the previous image.')
    colors = ['#202b24', '#3c5338', '#6b8e4e', '#9bbd68', '#d7f790']
    first = date.fromisoformat(days[0]['date'])
    offset = (first.weekday() + 1) % 7
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="276" viewBox="0 0 1200 276" role="img" aria-label="GitHub contribution calendar"><rect width="1200" height="276" rx="18" fill="#101514"/><text x="32" y="38" font-family="monospace" font-size="12" letter-spacing="2" fill="#afbeb3">CONTRIBUTIONS / PAST YEAR</text>']
    parts.append(f'<text x="1168" y="38" text-anchor="end" font-family="monospace" font-size="11" fill="#75867b">{days[0]["date"]} — {days[-1]["date"]}</text>')
    months = set()
    for i, d in enumerate(days):
        n = offset + i
        x, y = 40 + (n // 7) * 21, 82 + (n % 7) * 21
        current = date.fromisoformat(d['date'])
        if (current.year,current.month) not in months and i > 6:
            months.add((current.year,current.month))
            parts.append(f'<text x="{x}" y="68" font-family="monospace" font-size="10" fill="#75867b">{current.strftime("%b").upper()}</text>')
        level = max(0, min(4, int(d['level'])))
        parts.append(f'<rect x="{x}" y="{y}" width="16" height="16" rx="4" fill="{colors[level]}"><title>{d["date"]}: intensity {level}/4</title></rect>')
    parts.append('<text x="40" y="252" font-family="monospace" font-size="10" fill="#75867b">GITHUB / JASULAN273</text>')
    for i,color in enumerate(colors):
        parts.append(f'<rect x="{1050+i*21}" y="239" width="15" height="15" rx="4" fill="{color}"/>')
    parts.append('</svg>')
    (ROOT/'assets/activity.svg').write_text(''.join(parts), encoding='utf-8')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        days = json.loads(Path(sys.argv[1]).read_text())
    else:
        request = Request('https://github.com/users/Jasulan273/contributions', headers={'User-Agent': 'GitHub-Profile-Calendar'})
        with urlopen(request, timeout=30) as response:
            html = response.read().decode('utf-8')
        parser = CalendarParser()
        parser.feed(html)
        days = parser.days
    render(days)
