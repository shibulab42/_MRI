"""researchmap の新着論文を profile.txt（Publications）と news.txt（What's New）に追加する。

- researchmap の公開API（認証不要）から論文一覧を取得
- まだ取り込んでいない論文（researchmap_seen.json に無い & DOI/タイトルが profile.txt に無い）だけを追加
- 追加後は convert_data.py で data.js を作り直す（GitHub Actions のワークフローが続けて実行）

使い方:
  python update_from_researchmap.py            # 追加を実行
  python update_from_researchmap.py --dry-run  # 追加される内容を表示するだけ
"""
import json
import os
import re
import sys
import urllib.request

PERMALINK = 'shuhei_shibukawa'
API_URL = f'https://api.researchmap.jp/{PERMALINK}/published_papers?limit=100'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_PATH = os.path.join(BASE_DIR, 'profile.txt')
NEWS_PATH = os.path.join(BASE_DIR, 'news.txt')
SEEN_PATH = os.path.join(BASE_DIR, 'researchmap_seen.json')

# プレプリント（査読前論文）は載せない
PREPRINT_DOI_PREFIXES = ('10.21203/', '10.1101/', '10.31234/', '10.48550/', '10.2139/ssrn', '10.22541/', '10.20944/preprints')

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

SECTION_HEADERS = {
    'international_journals': '原著論文(国際)',
    'domestic_journals': '原著論文(国内)',
}


def fetch_papers():
    items = []
    url = API_URL
    while url:
        req = urllib.request.Request(url, headers={'User-Agent': 'shibukawa-lab-homepage-updater'})
        with urllib.request.urlopen(req, timeout=60) as res:
            data = json.load(res)
        items.extend(data.get('items', []))
        nxt = data.get('_links', {}).get('next')
        url = nxt['href'] if nxt else None
    return items


def pick(d, *langs):
    if not isinstance(d, dict):
        return d or ''
    for lang in langs or ('en', 'ja'):
        if d.get(lang):
            return d[lang]
    return next(iter(d.values()), '')


def get_doi(item):
    dois = (item.get('identifiers') or {}).get('doi') or []
    return dois[0].strip() if dois else ''


def norm(text):
    return re.sub(r'[^a-z0-9぀-ヿ一-鿿]', '', (text or '').lower())


def is_japanese(item):
    return 'jpn' in (item.get('languages') or [])


def format_author(name):
    name = name.strip()
    if re.search(r'[぀-ヿ一-鿿]', name):
        return name  # 日本語表記はそのまま
    if ',' in name:  # "Shibukawa, Shuhei"
        last, first = [p.strip() for p in name.split(',', 1)]
    else:
        parts = name.split()
        if len(parts) == 1:
            return name
        # 既に "Shibukawa S" 形式ならそのまま
        if re.fullmatch(r'[A-Z]{1,3}', parts[-1]):
            return name
        last, first = parts[-1], ' '.join(parts[:-1])
    initials = ''.join(p[0].upper() for p in re.split(r'[\s\-.]+', first) if p)
    return f'{last} {initials}'


def format_citation(item):
    jp = is_japanese(item)
    langs = ('ja', 'en') if jp else ('en', 'ja')
    authors = pick(item.get('authors') or {}, *langs) or []
    author_str = ', '.join(format_author(a.get('name', '')) for a in authors if a.get('name'))
    title = pick(item.get('paper_title'), *langs).strip().rstrip('.')
    journal = pick(item.get('publication_name'), *langs).strip()

    date = item.get('publication_date', '')
    y, m, d = (date.split('-') + ['', ''])[:3]
    date_str = y
    if m:
        date_str += f' {MONTHS[int(m) - 1]}'
    if d:
        date_str += f' {int(d)}'

    vol, num = item.get('volume', ''), item.get('number', '')
    sp, ep = item.get('starting_page', ''), item.get('ending_page', '')
    detail = ''
    if vol:
        detail += vol
        if num:
            detail += f'({num})'
        if sp:
            detail += f':{sp}' + (f'-{ep}' if ep and ep != sp else '')

    parts = []
    if author_str:
        parts.append(author_str + '.')
    parts.append(title + '.')
    if journal:
        parts.append(journal + '.')
    parts.append(date_str + (f';{detail}' if detail else '') + '.')
    doi = get_doi(item)
    if doi:
        parts.append(f'doi: {doi}.')
    return ' '.join(parts)


def load_seen():
    if os.path.exists(SEEN_PATH):
        with open(SEEN_PATH, encoding='utf-8') as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    with open(SEEN_PATH, 'w', encoding='utf-8') as f:
        json.dump(sorted(seen), f, indent=2)
        f.write('\n')


def insert_publications(profile_text, section_key, citations):
    """profile.txt の該当セクション先頭に論文を追加し、番号を振り直す。"""
    header = SECTION_HEADERS[section_key]
    lines = profile_text.split('\n')
    try:
        start = next(i for i, l in enumerate(lines) if l.strip().startswith(header))
    except StopIteration:
        # セクションが無ければ Publications: の直後に作る
        pub = next(i for i, l in enumerate(lines) if l.strip() == 'Publications:')
        lines.insert(pub + 1, header)
        start = pub + 1
    end = start + 1
    while end < len(lines) and re.match(r'^\s*\d+\.\s', lines[end]):
        end += 1
    existing = [re.sub(r'^\s*\d+\.\s*', '', l) for l in lines[start + 1:end]]
    merged = citations + existing
    numbered = [f'{i}.\t{c}' for i, c in enumerate(merged, 1)]
    lines[start + 1:end] = numbered
    return '\n'.join(lines)


def main():
    dry_run = '--dry-run' in sys.argv
    papers = fetch_papers()
    print(f'researchmap: {len(papers)} papers')

    with open(PROFILE_PATH, encoding='utf-8') as f:
        profile = f.read()
    pubs_text = profile.split('Publications:', 1)[-1]
    pubs_lower, pubs_norm = pubs_text.lower(), norm(pubs_text)
    seen = load_seen()

    new_items = []
    for item in papers:
        rid = item.get('rm:id')
        if item.get('display') != 'disclosed' or rid in seen:
            continue
        doi = get_doi(item).lower()
        title = pick(item.get('paper_title'))
        already = (doi and doi in pubs_lower) or (len(norm(title)) >= 20 and norm(title)[:60] in pubs_norm)
        if already or doi.startswith(PREPRINT_DOI_PREFIXES):
            seen.add(rid)
            continue
        new_items.append(item)

    new_items.sort(key=lambda x: x.get('publication_date', ''), reverse=True)
    if not new_items:
        print('新着論文はありません。')
        if not dry_run:
            save_seen(seen)
        return

    by_section = {'international_journals': [], 'domestic_journals': []}
    news_entries = []
    for item in new_items:
        cite = format_citation(item)
        key = 'domestic_journals' if is_japanese(item) else 'international_journals'
        by_section[key].append(cite)
        y, m = (item.get('publication_date', '') + '--').split('-')[:2]
        when = f'{y}.{int(m)}' if m else y
        doi = get_doi(item)
        link = f' | https://doi.org/{doi}' if doi else ''
        news_entries.append(f'{when} [Publication] 論文が公開されました！\n{cite}{link}\n')
        print(f'  + [{key}] {cite}')

    if dry_run:
        print('(dry-run のため書き込みはしていません)')
        return

    for key, cites in by_section.items():
        if cites:
            profile = insert_publications(profile, key, cites)
    with open(PROFILE_PATH, 'w', encoding='utf-8') as f:
        f.write(profile)

    with open(NEWS_PATH, encoding='utf-8') as f:
        news = f.read()
    with open(NEWS_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(news_entries) + '\n' + news)

    seen.update(item['rm:id'] for item in new_items)
    save_seen(seen)
    print(f'{len(new_items)} 件を追加しました。')


if __name__ == '__main__':
    main()
