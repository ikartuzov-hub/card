#!/usr/bin/env python3
"""
sync-links.py — разносит ссылки из links.json по всем страницам визитки.

Как пользоваться:
  1. Поменять адрес в links.json: новый в "url", прежний дописать в "aliases".
  2. python3 tools/sync-links.py          — показать, что изменится (сухой прогон)
  3. python3 tools/sync-links.py --apply  — применить

Правило: ссылки в HTML и в igor-kartuzov.vcf руками не правятся никогда.
Единственная точка правки — links.json.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "tools", "_archive"}
SKIP_EXT = {".jpg", ".jpeg", ".png", ".webp", ".ico", ".zip"}
SKIP_FILES = {"links.json"}


def load_links():
    with open(os.path.join(ROOT, "links.json"), encoding="utf-8") as f:
        return json.load(f)["links"]


def targets():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn in SKIP_FILES:
                continue
            if os.path.splitext(fn)[1].lower() in SKIP_EXT:
                continue
            yield os.path.join(dirpath, fn)


def main():
    apply = "--apply" in sys.argv
    links = load_links()

    # Более длинные алиасы заменяем первыми, иначе короткий префикс съест длинный.
    pairs = []
    for key, item in links.items():
        for alias in item.get("aliases", []):
            if alias and alias != item["url"]:
                pairs.append((alias, item["url"], key))
    pairs.sort(key=lambda p: len(p[0]), reverse=True)

    total = 0
    touched = []

    for path in targets():
        # newline="" обязателен: без него Python схлопывает CRLF в LF при
        # чтении и записи. Для igor-kartuzov.vcf это порча формата —
        # vCard по RFC 6350 требует CRLF. Один раз уже наступили.
        try:
            with open(path, encoding="utf-8", newline="") as f:
                text = f.read()
        except (UnicodeDecodeError, OSError):
            continue

        original = text
        hits = []
        for alias, url, key in pairs:
            n = text.count(alias)
            if n:
                text = text.replace(alias, url)
                hits.append((key, alias, url, n))

        if text != original:
            rel = os.path.relpath(path, ROOT)
            touched.append((rel, hits))
            total += sum(h[3] for h in hits)
            if apply:
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(text)

    if not touched:
        print("Всё синхронно — устаревших ссылок не найдено.")
        return

    mode = "ПРИМЕНЕНО" if apply else "СУХОЙ ПРОГОН (запусти с --apply, чтобы записать)"
    print(f"{mode}\n")
    for rel, hits in touched:
        print(f"  {rel}")
        for key, alias, url, n in hits:
            print(f"      [{key}] ×{n}  {alias}  →  {url}")
    print(f"\nВсего замен: {total} в {len(touched)} файлах.")

    if apply:
        print("\nПроверь глазами хотя бы одну страницу перед коммитом.")


if __name__ == "__main__":
    main()
