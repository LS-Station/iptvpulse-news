import os
from pathlib import Path
import re
from datetime import datetime

# ----------------------------
# Configuration
# ----------------------------
BLOG_DIR = "."  # যেখানে Markdown ফাইল আছে, "." = root
README_PATH = Path("README.md")
BASE_URL = "https://www.iptvpulse.top/"  # তোমার ব্লগ URL

# ----------------------------
# Collect blog posts
# ----------------------------
blog_posts = []

for md_file in Path(BLOG_DIR).rglob("*.md"):
    # Skip README.md itself
    if md_file.name.lower() == "readme.md":
        continue

    print(f"Processing file: {md_file}")

    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    # H1 (# Title) detect
    title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else md_file.stem

    # date: yyyy-mm-dd detect
    date_match = re.search(r'^date:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
    post_date = datetime.strptime(date_match.group(1), "%Y-%m-%d") if date_match else datetime.fromtimestamp(md_file.stat().st_mtime)

    # URL generate
    slug = md_file.stem.replace(' ', '-').lower()
    url = BASE_URL + slug

    print(f"Title: {title}, Date: {post_date.date()}, URL: {url}")

    blog_posts.append((post_date, f"- [{title}]({url})"))

# Sort by date descending
blog_posts.sort(key=lambda x: x[0], reverse=True)
blog_posts_text = [item[1] for item in blog_posts]

# ----------------------------
# Update README.md
# ----------------------------
start_tag = "<!--START_SECTION:blog-posts-->"
end_tag = "<!--END_SECTION:blog-posts-->"

new_section = f"{start_tag}\n" + "\n".join(blog_posts_text) + f"\n{end_tag}"

if README_PATH.exists():
    readme_content = README_PATH.read_text(encoding="utf-8")
else:
    readme_content = ""

if start_tag in readme_content and end_tag in readme_content:
    pattern = re.compile(f"{start_tag}.*?{end_tag}", re.DOTALL)
    updated_content = pattern.sub(new_section, readme_content)
else:
    updated_content = readme_content + "\n\n" + new_section

README_PATH.write_text(updated_content, encoding="utf-8")
print("✅ README.md updated with latest blog posts")
