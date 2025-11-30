import re
from pathlib import Path
from datetime import datetime

BLOG_DIR = "."
README_PATH = Path("README.md")
BASE_URL = "https://www.iptvpulse.top/"

blog_posts = []

for md_file in Path(BLOG_DIR).rglob("*.md"):
    if md_file.name.lower() == "readme.md":
        continue

    try:
        content = md_file.read_text(encoding="utf-8")
    except:
        continue

    title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else md_file.stem

    date_match = re.search(r'^date:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
    post_date = datetime.strptime(date_match.group(1), "%Y-%m-%d") if date_match else datetime.fromtimestamp(md_file.stat().st_mtime)

    slug = md_file.stem.replace(' ', '-').lower()
    url = BASE_URL + slug

    # append without any condition
    blog_posts.append((post_date, f"- [{title}]({url})"))

# sort descending
blog_posts.sort(key=lambda x: x[0], reverse=True)
blog_posts_text = [item[1] for item in blog_posts]

start_tag = "<!--START_SECTION:blog-posts-->"
end_tag = "<!--END_SECTION:blog-posts-->"
new_section = f"{start_tag}\n" + "\n".join(blog_posts_text) + f"\n{end_tag}"

if README_PATH.exists():
    readme_content = README_PATH.read_text(encoding="utf-8")
else:
    readme_content = ""

if start_tag in readme_content and end_tag in readme_content:
    import re
    pattern = re.compile(f"{start_tag}.*?{end_tag}", re.DOTALL)
    updated_content = pattern.sub(new_section, readme_content)
else:
    updated_content = readme_content + "\n\n" + new_section

README_PATH.write_text(updated_content, encoding="utf-8")
print("✅ README.md updated with latest blog posts")
