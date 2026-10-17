#!/usr/bin/env python3
"""Validate built GitHub Pages output, including URLs used by App Store Connect."""
import json,re,sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote

ROOT=Path(__file__).resolve().parents[1]
BUILD=Path(sys.argv[1] if len(sys.argv)>1 else ROOT/'_site').resolve()
class Page(HTMLParser):
    def __init__(self,path):
        super().__init__(); self.links=[]; self.ids=[]; self.h1=0; self.canonical=[]; self.lang=''; self.images=0
        self.feed(path.read_text())
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='html':self.lang=a.get('lang','')
        if tag=='h1':self.h1+=1
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
        if tag in ['a','link','img','script']:
            ref=a.get('href') or a.get('src')
            if ref:self.links.append(ref)
        if tag=='img':
            assert 'alt' in a,'Image without alt'
            assert a.get('width') and a.get('height'),'Image without intrinsic size'
            self.images+=1

def resolve(path):
    p=BUILD/path.lstrip('/')
    if p.is_dir():return p/'index.html'
    if p.is_file():return p
    if not p.suffix:return p.with_suffix('.html')
    return p

pages={p:Page(p) for p in BUILD.rglob('*.html')}
assert pages,'Build the site first'
locales=json.loads((ROOT/'_data/content.json').read_text())
required=['/','/privacy','/privacy.html','/privacy/']+[v['home'] for v in locales.values()]+[v['privacy'] for v in locales.values()]
for url in required:assert resolve(url).is_file(),f'Missing stable route: {url}'
assert (ROOT/'CNAME').read_text().strip()=='growquest.xyz'
for p,doc in pages.items():
    assert doc.lang,f'Missing lang: {p.name}'
    assert doc.h1==1,f'Expected one H1: {p.name}'
    assert len(doc.ids)==len(set(doc.ids)),f'Duplicate IDs: {p.name}'
    assert len(doc.canonical)==1 and doc.canonical[0].startswith('https://growquest.xyz/'),f'Canonical: {p.name}'
    raw=p.read_text()
    assert '{{' not in raw and '{%' not in raw,f'Unresolved Liquid: {p.name}'
    assert 'We may collect anonymous crash logs' not in raw
    assert 'devsuperx@gmail.com' not in raw,f'Old contact email: {p.name}'
    assert 'mailto:support@growquest.xyz' in doc.links,f'Missing support email: {p.name}'
    for ref in doc.links:
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        target=resolve(unquote(u.path)) if u.path else p
        assert target.is_file(),f'Broken link: {p.name} -> {ref}'
        if u.fragment and target in pages:
            assert unquote(u.fragment) in pages[target].ids,f'Broken anchor: {p.name} -> {ref}'
for code,t in locales.items():
    p=resolve(t['home']);doc=pages[p]
    assert doc.lang==t['lang'] and doc.images==6,f'Home incomplete: {code}'
    for link in ['https://apps.apple.com/app/6756180778','https://github.com/embbnux/growquest-app/issues/new']:
        assert link in doc.links,f'Existing external link lost: {code}'
    assert t['soon'] in p.read_text() and t['release_note'] in p.read_text()
    if code=='zh':
        assert not re.search(r'Apple Intelligence|Private Cloud Compute|智能解析|\bAI\b',p.read_text()),'Simplified Chinese marketing must follow D3'
print(f'PASS: {len(pages)} HTML pages; {len(locales)} languages; stable routes, links, fragments, image metadata, release labels and privacy-copy regression checks.')
