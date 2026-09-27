import os
import sys
import subprocess
import pathlib
import markdown

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    CHROME_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CSS_STYLES = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

@page {
    size: A4;
    margin: 18mm 16mm 20mm 16mm;
    @bottom-right {
        content: counter(page);
    }
}

* {
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: #1e293b;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
}

/* Document Header Banner */
.doc-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
    color: #ffffff;
    padding: 24px 28px;
    border-radius: 10px;
    margin-bottom: 24px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
}

.doc-header h1 {
    font-size: 20pt;
    font-weight: 800;
    margin: 0 0 6px 0;
    color: #ffffff;
    letter-spacing: -0.02em;
}

.doc-header .doc-subtitle {
    font-size: 12pt;
    color: #38bdf8;
    font-weight: 600;
    margin-bottom: 12px;
}

.doc-header .doc-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    font-size: 8.5pt;
    color: #cbd5e1;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    padding-top: 10px;
    margin-top: 10px;
}

.doc-meta span {
    background: rgba(255, 255, 255, 0.1);
    padding: 3px 8px;
    border-radius: 4px;
}

/* Headings */
h1 {
    font-size: 16pt;
    font-weight: 700;
    color: #0f172a;
    margin-top: 24px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 2px solid #0284c7;
    page-break-after: avoid;
    break-after: avoid;
}

h2 {
    font-size: 13pt;
    font-weight: 700;
    color: #1e3a8a;
    margin-top: 20px;
    margin-bottom: 10px;
    padding-bottom: 4px;
    border-bottom: 1px solid #e2e8f0;
    page-break-after: avoid;
    break-after: avoid;
}

h3 {
    font-size: 11pt;
    font-weight: 600;
    color: #0369a1;
    margin-top: 16px;
    margin-bottom: 8px;
    page-break-after: avoid;
    break-after: avoid;
}

h4 {
    font-size: 10pt;
    font-weight: 600;
    color: #334155;
    margin-top: 12px;
    margin-bottom: 6px;
    page-break-after: avoid;
    break-after: avoid;
}

p {
    margin-top: 0;
    margin-bottom: 10px;
    text-align: justify;
}

/* Lists */
ul, ol {
    margin-top: 0;
    margin-bottom: 12px;
    padding-left: 22px;
}

li {
    margin-bottom: 4px;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
    margin-bottom: 18px;
    font-size: 8.8pt;
    page-break-inside: avoid;
    break-inside: avoid;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

th {
    background-color: #1e3a8a;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 7px 10px;
    border: 1px solid #1e3a8a;
}

td {
    padding: 6px 10px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
}

tr:nth-child(even) {
    background-color: #f8fafc;
}

tr:hover {
    background-color: #f1f5f9;
}

/* Code & Pre */
code {
    font-family: 'JetBrains Mono', Consolas, Monaco, monospace;
    font-size: 8.5pt;
    background-color: #f1f5f9;
    color: #0369a1;
    padding: 2px 5px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
}

pre {
    background-color: #0f172a;
    color: #f8fafc;
    padding: 12px 14px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 8pt;
    line-height: 1.45;
    margin-top: 10px;
    margin-bottom: 14px;
    page-break-inside: avoid;
    break-inside: avoid;
    border: 1px solid #334155;
}

pre code {
    background-color: transparent;
    color: #f8fafc;
    padding: 0;
    border: none;
    font-size: inherit;
}

/* Blockquotes & Callouts */
blockquote {
    border-left: 4px solid #0284c7;
    background-color: #f0f9ff;
    color: #0c4a6e;
    padding: 10px 14px;
    margin: 12px 0;
    border-radius: 0 6px 6px 0;
    font-style: normal;
    page-break-inside: avoid;
    break-inside: avoid;
}

blockquote p:last-child {
    margin-bottom: 0;
}

/* Badges and tags */
.badge {
    display: inline-block;
    padding: 2px 6px;
    font-size: 7.5pt;
    font-weight: 600;
    border-radius: 4px;
    text-transform: uppercase;
}
.badge-blue { background: #e0f2fe; color: #0369a1; }
.badge-green { background: #dcfce7; color: #15803d; }
.badge-amber { background: #fef3c7; color: #b45309; }

/* Horizontal rule */
hr {
    border: 0;
    height: 1px;
    background: #e2e8f0;
    margin: 18px 0;
}

/* Footer for print */
.footer-text {
    position: fixed;
    bottom: -12mm;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-between;
    font-size: 7.5pt;
    color: #94a3b8;
    border-top: 1px solid #e2e8f0;
    padding-top: 4px;
}
"""

def convert_md_to_html(md_file_path, title, subtitle, doc_type="DOCUMENT"):
    with open(md_file_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Convert markdown to html
    html_content = markdown.markdown(
        md_text,
        extensions=[
            "extra",
            "tables",
            "fenced_code",
            "codehilite",
            "toc",
            "nl2br",
            "sane_lists"
        ]
    )

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
{CSS_STYLES}
</style>
</head>
<body>

<div class="doc-header">
    <h1>{title}</h1>
    <div class="doc-subtitle">{subtitle}</div>
    <div class="doc-meta">
        <span><strong>Client / Organization:</strong> Oil India Limited (OIL)</span>
        <span><strong>Initiative:</strong> Smart India Hackathon (SIH 2026)</span>
        <span><strong>Document Type:</strong> {doc_type}</span>
        <span><strong>Version:</strong> 1.0 (Production Blueprint)</span>
        <span><strong>Classification:</strong> Engineering Specification</span>
    </div>
</div>

<div class="content-body">
{html_content}
</div>

</body>
</html>"""
    return full_html


def generate_pdf_from_html(html_str, output_pdf_path):
    temp_html_path = output_pdf_path.replace(".pdf", "_temp.html")
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(html_str)

    abs_html = os.path.abspath(temp_html_path)
    abs_pdf = os.path.abspath(output_pdf_path)
    file_uri = pathlib.Path(abs_html).as_uri()

    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={abs_pdf}",
        file_uri
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

    if os.path.exists(abs_pdf) and os.path.getsize(abs_pdf) > 0:
        print(f"[SUCCESS] Generated: {output_pdf_path} ({os.path.getsize(abs_pdf) / 1024:.1f} KB)")
        return True
    else:
        print(f"[ERROR] Failed to generate {output_pdf_path}. Result: {result.stderr}")
        return False


def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))

    docs = [
        {
            "md": os.path.join(base_dir, "NWIS_PRD.md"),
            "pdf": os.path.join(base_dir, "NWIS_PRD.pdf"),
            "title": "Product Requirements Document (PRD)",
            "subtitle": "Nearby Wells Intelligence System (NWIS) — Oil India Limited (SIH 2026)",
            "type": "Product Requirements Document (PRD)"
        },
        {
            "md": os.path.join(base_dir, "NWIS_TRD.md"),
            "pdf": os.path.join(base_dir, "NWIS_TRD.pdf"),
            "title": "Technical Requirements Document (TRD)",
            "subtitle": "Nearby Wells Intelligence System (NWIS) — Technical Blueprint & Architecture",
            "type": "Technical Requirements Document (TRD)"
        },
        {
            "md": os.path.join(base_dir, "NWIS_MASTER_DOCUMENTATION.md"),
            "pdf": os.path.join(base_dir, "NWIS_MASTER_DOCUMENTATION.pdf"),
            "title": "Master Specification & Architecture Document",
            "subtitle": "Nearby Wells Intelligence System (NWIS) — Consolidated PRD + TRD",
            "type": "Master Engineering Blueprint"
        },
        {
            "md": os.path.join(base_dir, "PROJECT_OVERVIEW_EXPLAINED.md"),
            "pdf": os.path.join(base_dir, "PROJECT_OVERVIEW_EXPLAINED.pdf"),
            "title": "NWIS Project Guide & Architecture Explained",
            "subtitle": "Nearby Wells Intelligence System — Problem Statement, Purpose & Solution Mechanics",
            "type": "Comprehensive Project Overview"
        },
        {
            "md": os.path.join(base_dir, "DEMO_SCREEN_RECORDING_SCRIPT.md"),
            "pdf": os.path.join(base_dir, "DEMO_SCREEN_RECORDING_SCRIPT.pdf"),
            "title": "3-Minute Prototype Demo Video Script",
            "subtitle": "भू-DRISHTI: Subsurface Intelligence & Autonomous Well-Control Copilot • Oil India Limited",
            "type": "Presentation Pitch Script"
        },
        {
            "md": os.path.join(base_dir, "TEAM_818_CAFFEINE_CREW_CAMERA_PITCH.md"),
            "pdf": os.path.join(base_dir, "TEAM_818_CAFFEINE_CREW_CAMERA_PITCH.pdf"),
            "title": "Team 818_CAFFEINE CREW Camera Presentation Script",
            "subtitle": "PS ID 26121: eRTMAC-NWIS • भू-DRISHTI for Oil India Limited (SIH 2026)",
            "type": "Judges Pitch Speech"
        },
        {
            "md": os.path.join(base_dir, "TEAM_818_CAFFEINE_CREW_1MIN_CAMERA_PITCH.md"),
            "pdf": os.path.join(base_dir, "TEAM_818_CAFFEINE_CREW_1MIN_CAMERA_PITCH.pdf"),
            "title": "Team 818_CAFFEINE CREW 1-Minute Elevator Camera Pitch",
            "subtitle": "PS ID 26121: eRTMAC-NWIS • भू-DRISHTI for Oil India Limited (SIH 2026)",
            "type": "60-Second Video Pitch Script"
        }
    ]

    for item in docs:
        if os.path.exists(item["md"]):
            print(f"Processing {item['md']} -> {item['pdf']}...")
            html = convert_md_to_html(item["md"], item["title"], item["subtitle"], item["type"])
            generate_pdf_from_html(html, item["pdf"])
        else:
            print(f"[WARNING] Markdown file not found: {item['md']}")


if __name__ == "__main__":
    main()
