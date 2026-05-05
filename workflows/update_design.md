# Workflow — Update the design

## Objective

Tweak the visual design without breaking the Anthropic-aesthetic feel.

## Required inputs

- The user's actual complaint or request ("font feels too small," "I want more space between paragraphs," "the accent is too orange").

## Where the design lives

Everything visual is in **`static/style.css`**. There are no Sass files, no design tokens in JSON, no theme provider. One file.

The CSS variables at the top of `style.css` are the design tokens — most tweaks are a one-line change there:

```
--bg          background color
--ink         body text color
--muted       secondary text (meta, summary)
--rule        hairlines and borders
--accent      links, blockquote bar, hover
--accent-dk   accent hover state
--serif       body font stack
--sans        meta/UI font stack
--content-width  max width of the reading column
```

## Steps

1. **Identify the smallest possible change.** Most requests are a CSS variable tweak. Resist rewriting whole sections.
2. **Edit `static/style.css` directly.** Do not regenerate the file.
3. **Rebuild and preview.**
   ```
   python3 tools/serve.py
   ```
4. **Hard-refresh the browser** (Cmd-Shift-R). The CSS file path doesn't change, so the browser may cache the old version.
5. **Sanity check on a real post**, not just the index. Long-form reading is the test.
6. **Sanity check on mobile.** DevTools responsive mode at iPhone widths. The `@media (max-width: 560px)` block at the bottom handles this.

## Hard rules

- **Do not add web fonts** (Google Fonts, Adobe Fonts). The system serif chain is intentional — instant load, no FOUT, no third-party request.
- **Do not add JavaScript** to the templates. v0 is HTML+CSS only.
- **Do not introduce a CSS framework** (Tailwind, Bootstrap, etc.).
- **Don't expand the color palette beyond the variables.** If a new color is genuinely needed, add it as a variable so the whole design stays coherent.

## When to ask before changing

- Switching the body typeface (the serif feel is a load-bearing design choice)
- Widening the content column past ~720px (breaks readability on long-form)
- Changing the accent color away from the warm-terracotta family (changes the brand)
