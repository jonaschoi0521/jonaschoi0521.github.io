# Workflow — Write a new post

## Objective

Take a thought from the user's head to a post on the blog.

## Post format

No frontmatter. Just a dated filename and your writing:

```
posts/2026-05-03.md
```

```markdown
# Your title here

Your post body in markdown.
```

- **Filename** = the date you wrote it (`YYYY-MM-DD.md`)
- **First line** = `# Title` — becomes the H1 on the post page
- **Rest** = your content in markdown
- If you write two posts on the same day: `2026-05-03-second.md`

## Steps

1. **Create the file.**
   ```
   python3 tools/new_post.py
   ```
   Creates `posts/YYYY-MM-DD.md` (today's date) with `# ` on line 1.
   Or just create the file directly in your editor — same thing.

2. **Write.** Replace `# ` with your title, then write the body below it.

3. **Tell Claude "completed"** when done. Claude will rebuild the site and confirm the post is live at http://localhost:8000.

## Markdown reference

- `## Section`, `### Sub-section`
- `**bold**`, `*italic*`
- `[link text](url)`
- `> blockquote`
- `` `inline code` `` and fenced code blocks ( ` ``` ` )
- `---` horizontal rule
- Tables, footnotes (`[^1]`)

## Notes

- Filename becomes the URL: `2026-05-03.md` → `/2026-05-03.html`. Don't rename after publishing.
- Posts sort newest first by date in the filename.
- If the build fails: `pip3 install --user markdown jinja2`
- To self-preview before saying "completed": `python3 tools/serve.py` → http://localhost:8000
