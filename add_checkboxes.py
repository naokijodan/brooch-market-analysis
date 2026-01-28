#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ブローチHTMLにチェックボックス機能を追加するスクリプト
"""

import re

# HTMLファイルを読み込む
with open('/Users/naokijodan/Desktop/ブローチ市場データ_統合版_2026-01-27.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# チェックボックス用のCSSを追加
checkbox_css = '''        .search-checkbox {
            margin-left: 5px;
            margin-right: 10px;
            cursor: pointer;
            width: 16px;
            height: 16px;
            vertical-align: middle;
        }
'''

# CSSセクションを見つけて、最後の @media の前に挿入
css_insertion_pattern = r'(@media \(max-width: 768px\))'
html_content = re.sub(
    css_insertion_pattern,
    checkbox_css + r'\1',
    html_content,
    count=1
)

# チェックボックス用のJavaScript（localStorage管理）を追加
checkbox_js = '''
        // チェックボックスのlocalStorage管理
        function initCheckboxes() {
            document.addEventListener('DOMContentLoaded', function() {
                // ページ読み込み時にチェック状態を復元
                const checkboxes = document.querySelectorAll('.search-checkbox');
                checkboxes.forEach(checkbox => {
                    const checkboxId = checkbox.getAttribute('data-id');
                    if (checkboxId) {
                        const isChecked = localStorage.getItem(`checkbox_${checkboxId}`) === 'true';
                        checkbox.checked = isChecked;
                    }

                    // チェックボックスの変更を監視
                    checkbox.addEventListener('change', function() {
                        const checkboxId = this.getAttribute('data-id');
                        if (checkboxId) {
                            localStorage.setItem(`checkbox_${checkboxId}`, this.checked);
                        }
                    });
                });
            });
        }

        // 初期化関数を呼び出し
        initCheckboxes();
'''

# JavaScriptセクションを見つけて、</script>の前に挿入
js_insertion_pattern = r'(</script>\s*</body>)'
html_content = re.sub(
    js_insertion_pattern,
    checkbox_js + r'\1',
    html_content,
    count=1
)

# リンク生成部分にチェックボックスを追加
# 既存: <a href="..." class="link-btn link-ebay">eBay</a>
#       <a href="..." class="link-btn link-mercari">メルカリ</a>
# 新規: <a href="..." class="link-btn link-ebay">eBay</a>
#       <input type="checkbox" class="search-checkbox" data-id="...">
#       <a href="..." class="link-btn link-mercari">メルカリ</a>
#       <input type="checkbox" class="search-checkbox" data-id="...">

# JavaScriptのテーブル生成部分を修正
# パターン1: ハイブランド、デザイナーブランド、キャラクター/コラボ、カメオ
old_pattern1 = r'''(<a href="https://www\.ebay\.com/sch/i\.html\?\$\{ebayQuery\}&LH_Sold=1&LH_Complete=1" target="_blank" class="link-btn link-ebay">eBay</a>)
                        (<a href="https://jp\.mercari\.com/search\?keyword=\$\{searchQuery\}&status=on_sale" target="_blank" class="link-btn link-mercari">メルカリ</a>)'''

new_pattern1 = r'''\1
                        <input type="checkbox" class="search-checkbox" data-id="brooch_${category}_${item.brand}_${item.subcategory || 'none'}_ebay">
                        \2
                        <input type="checkbox" class="search-checkbox" data-id="brooch_${category}_${item.brand}_${item.subcategory || 'none'}_mercari">'''

html_content = re.sub(old_pattern1, new_pattern1, html_content, flags=re.MULTILINE)

# パターン2: ヴィンテージ、まとめ売り（subcategory がない場合）
old_pattern2 = r'''(<a href="https://www\.ebay\.com/sch/i\.html\?\$\{ebayQuery}&LH_Sold=1&LH_Complete=1" target="_blank" class="link-btn link-ebay">eBay</a>)
                        (<a href="https://jp\.mercari\.com/search\?keyword=\$\{encodeURIComponent\(item\.title\)\}&status=on_sale" target="_blank" class="link-btn link-mercari">メルカリ</a>)'''

new_pattern2 = r'''\1
                        <input type="checkbox" class="search-checkbox" data-id="brooch_${category}_${item.title.replace(/[^a-zA-Z0-9]/g, '_')}_ebay">
                        \2
                        <input type="checkbox" class="search-checkbox" data-id="brooch_${category}_${item.title.replace(/[^a-zA-Z0-9]/g, '_')}_mercari">'''

html_content = re.sub(old_pattern2, new_pattern2, html_content, flags=re.MULTILINE)

# より汎用的なパターンでキャッチ
# link-ebay の後にチェックボックスを追加（まだ追加されていない場合）
if '<input type="checkbox"' not in html_content:
    # シンプルな置換: eBayリンクの後にチェックボックスを追加
    html_content = re.sub(
        r'(<a href="https://www\.ebay\.com/[^"]*" target="_blank" class="link-btn link-ebay">eBay</a>)',
        r'\1\n                        <input type="checkbox" class="search-checkbox" data-id="brooch_item_ebay">',
        html_content
    )

    # メルカリリンクの後にチェックボックスを追加
    html_content = re.sub(
        r'(<a href="https://jp\.mercari\.com/[^"]*" target="_blank" class="link-btn link-mercari">メルカリ</a>)',
        r'\1\n                        <input type="checkbox" class="search-checkbox" data-id="brooch_item_mercari">',
        html_content
    )

# 保存
output_file = '/Users/naokijodan/Desktop/ブローチ市場データ_統合版_2026-01-27.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ チェックボックス機能を追加しました: {output_file}")
print(f"📊 ファイルサイズ: {len(html_content):,} 文字")
