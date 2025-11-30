import os
from pathlib import Path
import re
from datetime import datetime

# ব্লগ পোস্টের directory (Markdown ফাইল)
BLOG_DIR = "posts"  # এখানে adjust করো তোমার ব্লগ পোস্ট folder অনুযায়ী

# README path
README_PATH = Path("README.md")

# ব্লগ পোস্ট লিস্ট
blog_posts = []

for md_file in Path(BLOG_DIR).glob("*.md"):
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Markdown first line থেকে title বের করা (H1)
    title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = md_file.stem

    # Markdown metadata থেকে date বের করা (frontmatter format: yyyy-mm-dd)
    date_match = re.search(r'^date:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
    if date_match:
        post_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
    else:
        post_date = datetime.fromtimestamp(md_file.stat().st_mtime)  # যদি না থাকে, file modified time

    # URL তৈরি (spaces -> hyphens, lowercase)
    url = f"https://www.iptvpulse.top/{md_file.stem.replace(' ', '-').lower()}"
    
    blog_posts.append((post_date, f"- [{title}]({url})"))

# Sort descending by date (latest first)
blog_posts.sort(key=lambda x: x[0], reverse=True)
blog_posts_text = [item[1] for item in blog_posts]

# README update
if README_PATH.exists():
    readme_content = README_PATH.read_text(encoding="utf-8")
else:
    readme_content = ""

start_tag = "<!--START_SECTION:blog-posts-->"
end_tag = "<!--END_SECTION:blog-posts-->"

new_section = f"{start_tag}\n" + "\n".join(blog_posts_text) + f"\n{end_tag}"

if start_tag in readme_content and end_tag in readme_content:
    pattern = re.compile(f"{start_tag}.*?{end_tag}", re.DOTALL)
    updated_content = pattern.sub(new_section, readme_content)
else:
    updated_content = readme_content + "\n\n" + new_section

README_PATH.write_text(updated_content, encoding="utf-8")
print("✅ README.md updated with latest blog posts")
