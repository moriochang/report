#!/usr/bin/env python3
"""掃描 FY*/Q*/*.html，依 FY→Q→W 產生 index.html（GitHub Pages 首頁）。
新增每週報告後執行： python3 build_index.py
"""
import re
import pathlib
import datetime

ROOT = pathlib.Path(__file__).parent
PAT = re.compile(r"FY(\d+)Q(\d+)W(\d+)")

def collect():
    items = []
    for p in ROOT.glob("FY*/Q*/*.html"):
        m = PAT.search(p.name)
        if not m:
            continue
        fy, q, w = (int(x) for x in m.groups())
        mtime = datetime.date.fromtimestamp(p.stat().st_mtime)
        rel = "/".join(p.relative_to(ROOT).parts)
        items.append({"fy": fy, "q": q, "w": w, "path": rel, "date": mtime})
    return items

def build():
    items = collect()
    # FY 由新到舊、Q 由新到舊、W 由小到大
    tree = {}
    for it in items:
        tree.setdefault(it["fy"], {}).setdefault(it["q"], []).append(it)

    sections = []
    for fy in sorted(tree, reverse=True):
        q_blocks = []
        for q in sorted(tree[fy], reverse=True):
            weeks = sorted(tree[fy][q], key=lambda x: x["w"])
            rows = "\n".join(
                f'        <a class="wk" href="{w["path"]}">'
                f'<span class="w">W{w["w"]}</span>'
                f'<span class="d">{w["date"]:%Y/%m/%d}</span></a>'
                for w in weeks
            )
            q_blocks.append(
                f'      <div class="q">\n'
                f'        <h3>Q{q}</h3>\n'
                f'        <div class="weeks">\n{rows}\n        </div>\n'
                f'      </div>'
            )
        sections.append(
            f'    <section class="fy">\n'
            f'      <h2>FY{fy}</h2>\n' + "\n".join(q_blocks) + "\n    </section>"
        )

    updated = datetime.date.today().strftime("%Y/%m/%d")
    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>中區每週營運報告</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin:0; font-family:-apple-system,"Segoe UI","Noto Sans TC",sans-serif;
    background:#f5f6f8; color:#1c2530; }}
  header {{ background:#0d1b2a; color:#fff; padding:28px 20px; }}
  header h1 {{ margin:0; font-size:22px; }}
  header p {{ margin:6px 0 0; color:#9db0c6; font-size:13px; }}
  main {{ max-width:900px; margin:0 auto; padding:24px 16px 60px; }}
  .fy {{ background:#fff; border-radius:12px; padding:20px 22px; margin-bottom:20px;
    box-shadow:0 1px 3px rgba(0,0,0,.08); }}
  .fy h2 {{ margin:0 0 14px; font-size:18px; color:#0d1b2a;
    border-bottom:2px solid #e3e8ef; padding-bottom:8px; }}
  .q {{ margin:14px 0; }}
  .q h3 {{ margin:0 0 10px; font-size:14px; color:#4a5a70; letter-spacing:.5px; }}
  .weeks {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(140px,1fr)); gap:10px; }}
  .wk {{ display:flex; flex-direction:column; text-decoration:none; padding:12px 14px;
    border:1px solid #e3e8ef; border-radius:9px; background:#fbfcfe; transition:.15s; }}
  .wk:hover {{ border-color:#2f6df0; background:#f0f6ff; transform:translateY(-1px); }}
  .wk .w {{ font-weight:700; font-size:15px; color:#0d1b2a; }}
  .wk .d {{ font-size:12px; color:#7a8798; margin-top:2px; }}
  footer {{ text-align:center; color:#9aa6b5; font-size:12px; padding:20px; }}
</style>
</head>
<body>
<header>
  <h1>中區每週營運報告</h1>
  <p>依 FY → 季 → 週分類 · 最後更新 {updated}</p>
</header>
<main>
{chr(10).join(sections)}
</main>
<footer>moriochang/report</footer>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print(f"index.html 已產生，共 {len(items)} 份報告")

if __name__ == "__main__":
    build()
