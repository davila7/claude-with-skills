#!/usr/bin/env python3
"""Generate an interactive collapsible tree visualization of a codebase.

Usage:
    visualize.py [directory]

Arguments:
    directory   Root directory to scan. Defaults to the current directory.

Output:
    codebase-map.html in the current working directory. Opens automatically
    in the default browser.

Ignored directories: .git, node_modules, __pycache__, .venv, venv, dist, build,
and any directory or file whose name starts with a dot.
"""

import json
import sys
import webbrowser
from html import escape
from pathlib import Path
from collections import Counter


IGNORE = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}

# Color map for file extensions — used in both Python (for the sidebar bar chart)
# and injected into the HTML as a JS constant for the tree rendering.
COLORS = {
    ".js": "#f7df1e",
    ".ts": "#3178c6",
    ".jsx": "#61dafb",
    ".tsx": "#3178c6",
    ".py": "#3776ab",
    ".go": "#00add8",
    ".rs": "#dea584",
    ".rb": "#cc342d",
    ".css": "#264de4",
    ".scss": "#c6538c",
    ".html": "#e34c26",
    ".json": "#6b7280",
    ".md": "#083fa1",
    ".mdx": "#083fa1",
    ".yaml": "#cb171e",
    ".yml": "#cb171e",
    ".sh": "#4eaa25",
    ".toml": "#9b4f0f",
    ".xml": "#0060ac",
    ".sql": "#f29111",
    ".swift": "#f05138",
    ".kt": "#7f52ff",
    ".java": "#b07219",
    ".c": "#555555",
    ".cpp": "#f34b7d",
    ".h": "#555555",
    ".cs": "#178600",
    ".php": "#4f5d95",
}


def fmt_size(b):
    """Format a byte count as a human-readable string."""
    if b < 1024:
        return f"{b} B"
    if b < 1_048_576:
        return f"{b / 1024:.1f} KB"
    return f"{b / 1_048_576:.1f} MB"


def scan(path, stats):
    """Recursively scan a directory and return a tree dict.

    Each node is either:
      - A directory: {"name": str, "children": list, "size": int}
      - A file:      {"name": str, "size": int, "ext": str}

    stats is mutated in place:
      stats["files"] += 1 per file
      stats["dirs"]  += 1 per directory (excluding root)
      stats["extensions"][ext] += 1
      stats["ext_sizes"][ext] += size
    """
    node = {"name": path.name, "children": [], "size": 0}
    try:
        for item in sorted(path.iterdir(), key=lambda p: p.name.lower()):
            if item.name in IGNORE or item.name.startswith("."):
                continue
            if item.is_symlink():
                continue
            if item.is_file():
                try:
                    size = item.stat().st_size
                except OSError:
                    size = 0
                ext = item.suffix.lower() or "(no ext)"
                node["children"].append({"name": item.name, "size": size, "ext": ext})
                node["size"] += size
                stats["files"] += 1
                stats["extensions"][ext] += 1
                stats["ext_sizes"][ext] += size
            elif item.is_dir():
                stats["dirs"] += 1
                child = scan(item, stats)
                # Only include directories that contain at least one file
                if child["children"] or any(
                    not c.get("children") for c in child["children"]
                ):
                    node["children"].append(child)
                    node["size"] += child["size"]
    except PermissionError:
        pass
    return node


def generate_html(tree, stats, output_path):
    """Write a self-contained HTML file to output_path."""
    ext_sizes = stats["ext_sizes"]
    total_size = sum(ext_sizes.values()) or 1
    sorted_exts = sorted(ext_sizes.items(), key=lambda x: -x[1])[:8]

    bar_rows_html = ""
    for ext, size in sorted_exts:
        pct = size / total_size * 100
        color = COLORS.get(ext, "#6b7280")
        bar_rows_html += (
            f'<div class="bar-row">'
            f'<span class="bar-label">{escape(ext)}</span>'
            f'<div class="bar" style="width:{pct:.1f}%;background:{color}"></div>'
            f'<span class="bar-pct">{pct:.1f}%</span>'
            f"</div>\n"
        )

    colors_json = json.dumps(COLORS)
    tree_json = json.dumps(tree)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Codebase Explorer — {escape(tree["name"])}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}
    body {{
      font: 14px/1.5 system-ui, -apple-system, sans-serif;
      margin: 0;
      background: #1a1a2e;
      color: #e8e8f0;
    }}
    .container {{ display: flex; height: 100vh; overflow: hidden; }}
    .sidebar {{
      width: 280px;
      flex-shrink: 0;
      background: #252542;
      padding: 20px;
      border-right: 1px solid #3d3d5c;
      overflow-y: auto;
    }}
    .main {{ flex: 1; padding: 20px; overflow-y: auto; }}
    h1 {{ margin: 0 0 16px 0; font-size: 18px; font-weight: 600; }}
    h2 {{
      margin: 20px 0 8px 0;
      font-size: 11px;
      font-weight: 600;
      color: #888;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    .stat {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 7px 0;
      border-bottom: 1px solid #3d3d5c;
      font-size: 13px;
    }}
    .stat-label {{ color: #aaa; }}
    .stat-value {{ font-weight: 600; }}
    .bar-row {{
      display: flex;
      align-items: center;
      margin: 5px 0;
      gap: 6px;
    }}
    .bar-label {{
      width: 62px;
      font-size: 11px;
      color: #aaa;
      flex-shrink: 0;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .bar {{
      height: 14px;
      border-radius: 2px;
      min-width: 2px;
      flex-shrink: 0;
    }}
    .bar-pct {{ font-size: 11px; color: #666; white-space: nowrap; }}
    ul.tree {{
      list-style: none;
      padding-left: 18px;
      margin: 0;
    }}
    ul.tree > li:first-child {{ padding-top: 0; }}
    details > summary {{
      list-style: none;
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 3px 8px;
      border-radius: 4px;
      cursor: pointer;
      user-select: none;
    }}
    details > summary::-webkit-details-marker {{ display: none; }}
    details > summary:hover {{ background: #2d2d50; }}
    .folder-icon {{ color: #ffd700; font-style: normal; font-size: 13px; }}
    .folder-name {{ flex: 1; font-weight: 500; }}
    .file-row {{
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 3px 8px;
      border-radius: 4px;
    }}
    .file-row:hover {{ background: #2d2d50; }}
    .file-name {{ flex: 1; }}
    .size-tag {{
      color: #666;
      font-size: 12px;
      white-space: nowrap;
      flex-shrink: 0;
    }}
    .dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      flex-shrink: 0;
    }}
  </style>
</head>
<body>
<div class="container">
  <div class="sidebar">
    <h1>Summary</h1>
    <div class="stat">
      <span class="stat-label">Files</span>
      <span class="stat-value">{stats["files"]:,}</span>
    </div>
    <div class="stat">
      <span class="stat-label">Directories</span>
      <span class="stat-value">{stats["dirs"]:,}</span>
    </div>
    <div class="stat">
      <span class="stat-label">Total size</span>
      <span class="stat-value">{fmt_size(tree["size"])}</span>
    </div>
    <div class="stat">
      <span class="stat-label">File types</span>
      <span class="stat-value">{len(stats["extensions"]):,}</span>
    </div>
    <h2>By file type</h2>
    {bar_rows_html}
  </div>
  <div class="main">
    <h1>{escape(tree["name"])}</h1>
    <ul class="tree" id="root"></ul>
  </div>
</div>
<script>
(function () {{
  var tree = {tree_json};
  var colors = {colors_json};

  function fmt(b) {{
    if (b < 1024) return b + ' B';
    if (b < 1048576) return (b / 1024).toFixed(1) + ' KB';
    return (b / 1048576).toFixed(1) + ' MB';
  }}

  function esc(s) {{
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }}

  function renderNode(node, parentEl, depth) {{
    var li = document.createElement('li');

    if (Array.isArray(node.children)) {{
      // Directory node
      var det = document.createElement('details');
      if (depth === 0) det.open = true;

      var sum = document.createElement('summary');
      sum.innerHTML =
        '<span class="folder-icon">+</span>' +
        '<span class="folder-name">' + esc(node.name) + '</span>' +
        '<span class="size-tag">' + fmt(node.size) + '</span>';
      det.appendChild(sum);

      // Sort: directories first, then files, both alphabetically
      var children = node.children.slice().sort(function (a, b) {{
        var aIsDir = Array.isArray(a.children) ? 0 : 1;
        var bIsDir = Array.isArray(b.children) ? 0 : 1;
        if (aIsDir !== bIsDir) return aIsDir - bIsDir;
        return a.name.localeCompare(b.name);
      }});

      var ul = document.createElement('ul');
      ul.className = 'tree';
      children.forEach(function (child) {{
        renderNode(child, ul, depth + 1);
      }});
      det.appendChild(ul);
      li.appendChild(det);
    }} else {{
      // File node
      var row = document.createElement('div');
      row.className = 'file-row';
      var color = colors[node.ext] || '#6b7280';
      row.innerHTML =
        '<span class="dot" style="background:' + color + '"></span>' +
        '<span class="file-name">' + esc(node.name) + '</span>' +
        '<span class="size-tag">' + fmt(node.size) + '</span>';
      li.appendChild(row);
    }}

    parentEl.appendChild(li);
  }}

  var root = document.getElementById('root');
  if (Array.isArray(tree.children)) {{
    tree.children.forEach(function (child) {{
      renderNode(child, root, 0);
    }});
  }}
}})();
</script>
</body>
</html>"""

    output_path.write_text(html, encoding="utf-8")


def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

    if not target.exists():
        print(f"Error: directory not found: {target}", file=sys.stderr)
        sys.exit(1)
    if not target.is_dir():
        print(f"Error: not a directory: {target}", file=sys.stderr)
        sys.exit(1)

    stats = {
        "files": 0,
        "dirs": 0,
        "extensions": Counter(),
        "ext_sizes": Counter(),
    }

    print(f"Scanning {target} ...")
    tree = scan(target, stats)

    output = Path("codebase-map.html")
    generate_html(tree, stats, output)

    abs_output = output.absolute()
    print(f"Generated: {abs_output}")
    print(
        f"  {stats['files']:,} files, "
        f"{stats['dirs']:,} directories, "
        f"{len(stats['extensions'])} file types"
    )

    webbrowser.open(f"file://{abs_output}")


if __name__ == "__main__":
    main()
