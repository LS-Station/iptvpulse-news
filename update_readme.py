import re
from pathlib import Path
from datetime import datetime

# Configuration
BLOG_DIR = "."  # Markdown files root folder
README_PATH = Path("README.md")
BASE_URL = "https://www.iptvpulse.top/"

blog_posts = []

# Detect all Markdown files recursively
for md_file in Path(BLOG_DIR).rglob("*.md"):
    if md_file.name.lower() == "readme.md":
        continue  # skip README

    # Read content safely
    try:
        content = md_file.read_text(encoding="utf-8")
    except:
        continue

    # Use H1 as title if exists, else filename
    title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else md_file.stem

    # Use frontmatter date if exists, else file modified time
    date_match = re.search(r'^date:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
    post_date = datetime.strptime(date_match.group(1), "%Y-%m-%d") if date_match else datetime.fromtimestamp(md_file.stat().st_mtime)

    # URL generate
    slug = md_file.stem.replace(' ', '-').lower()
    url = BASE_URL + slug

    # Append all files
    blog_posts.append((post_date, f"- [{title}]({url})"))

# Sort by date descending
blog_posts.sort(key=lambda x: x[0], reverse=True)
blog_posts_text = [item[1] for item in blog_posts]

# Prepare README section
start_tag = "<!--START_SECTION:blog-posts-->"
end_tag = "<!--END_SECTION:blog-posts-->"
new_section = f"{start_tag}\n" + "\n".join(blog_posts_text) + f"\n{end_tag}"

# Read existing README
if README_PATH.exists():
    readme_content = README_PATH.read_text(encoding="utf-8")
else:
    readme_content = ""

# Replace or append section
if start_tag in readme_content and end_tag in readme_content:
    pattern = re.compile(f"{start_tag}.*?{end_tag}", re.DOTALL)
    updated_content = pattern.sub(new_section, readme_content)
else:
    updated_content = readme_content + "\n\n" + new_section

# Write updated README
README_PATH.write_text(updated_content, encoding="utf-8")
print(f"✅ README.md updated with {len(blog_posts)} posts")
