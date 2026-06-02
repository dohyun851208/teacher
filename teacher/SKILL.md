---
name: teacher
description: Create, fill, and verify Korean school teacher administrative documents and teaching materials. Use when working with HWP/HWPX forms, XLS/XLSX templates, applications, official letters, reports, resumes, achievement statements, training or career lists, HTML-based class or training slides, any current/project folder whose name ends with "(AI)", or an external single-file Korean school document path supplied by the user, especially when preserving form layout, merged cells, HWPX XML structure, signatures, or browser-presented slide decks matters.
---

# Teacher

## Overview

Use this skill to route Korean teacher paperwork requests into the right document workflow, preserve original form structure, and keep private profile data outside the reusable skill package.

Start every task by reading `references/routing.md`, then load only the format workflow and content-rule references that match the request.

For first-time `(AI)` teacher workspaces, folder indexing, source-to-Markdown summaries, or external single-file handling, use `references/project-setup.md`.

## Context And Privacy

- Treat user-provided project files as the source of truth for personal data, evidence files, forms, and design references.
- Interpret project-internal paths as relative to the current work folder unless the user explicitly provides an external absolute path.
- Prefer structured Markdown in the user's `docs/` folder before opening original evidence files.
- If the current folder or nearest project root ends with `(AI)`, follow this skill's routing even when the user does not explicitly type `$teacher`.
- Save modified, completed, and submission-ready outputs inside a `완성본/` folder under the current work folder. Create the folder if it does not exist, and do not overwrite the original file.
- If the user supplies an external file path for a one-off school document, treat the source file's parent as the work folder and save the result inside that folder's `완성본/` subfolder.
- Do not scan or read every original file during first setup. Start from folder names, filenames, and extensions; open source files only when they are relevant to the user's current task or a requested summary.
- Use `references/profile-schema.md` as the recommended private-project data layout.
- Do not copy actual personal data, signatures, ID cards, certificates, bankbook images, or completed output files into this skill.
- Save created or modified text files as UTF-8. In Python, pass `encoding="utf-8"` whenever reading or writing text.
- In PowerShell sessions that handle Korean paths or text, set UTF-8 output first:

```powershell
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

## Workflow Routing

1. Read `references/routing.md`.
2. Choose the output-format workflow first:
   - HWP/HWPX forms or HWPX documents: `references/workflows/hwpx-forms.md`
   - XLS/XLSX forms or spreadsheet tables: `references/workflows/xlsx-forms.md`
   - HTML slides and training/class materials: `references/workflows/html-slides.md`
   - Existing `.ppt`/`.pptx` files: use a PowerPoint workflow only when the user explicitly asks to edit the provided file.
3. If the task is a resume, achievement statement, application, official letter, report, training list, or career summary, also load `references/teacher-admin-rules.md` and the matching `references/content-rules/*.md` file.
4. For HTML slides, also load the relevant style reference:
   - Design sources: `references/html-slide-design-sources.md`
   - Apple-style preset: `references/html-slide-apple-style.md`
   - **My Slides preset (Korean Edu Pastel, default for PPT/slide requests): `references/my-slides/SKILL.md`** — pastel blue-grey background, cream cards, Plus Jakarta Sans, drawing canvas, inline-edit dot toggle, viewport/accessibility safeguards. Use this by default when the user asks for slides, PPT, presentation, training, or class materials, unless they specify a different style.
5. Preserve original formatting, merged cells, tables, images, margins, fonts, and alignment unless the user asks for a redesign.
6. Verify the result by reopening, extracting text, checking workbook structure, rendering, or screenshotting as appropriate.

## HWP And HWPX

For `.hwp`, first produce a `.hwpx` working copy. Prefer Hancom Office COM conversion when available; otherwise use `scripts/convert_hwp.py` as a fallback or analysis helper.

For `.hwpx`, analyze before editing:

```bash
python scripts/clone_form.py --analyze input.hwpx
python scripts/text_extract.py input.hwpx
```

For simple form text replacement, preserve the ZIP/XML structure:

```bash
python scripts/clone_form.py input.hwpx output.hwpx --map map.json
```

For blank table cells, inspect actual cell addresses in `Contents/section0.xml` and write only the target cell content. Keep the final deliverable as `.hwpx`; do not save back to `.hwp`.

For low-level HWPX creation or repair, use the bundled helpers and templates:

- `scripts/build_hwpx.py`
- `scripts/md2hwpx.py`
- `scripts/fix_namespaces.py`
- `scripts/validate.py`
- `scripts/verify_hwpx.py`
- `templates/`
- `references/hwpx/`

## XLS And XLSX

Use `openpyxl` for `.xls` and `.xlsx` workflows when possible. Before writing values, inspect sheet names, merged ranges, header rows, and the data region. Write values only to the top-left cell of a merged range, preserve styles, and reopen the workbook after saving to confirm values, merges, borders, fonts, alignment, and row heights.

## Content Rules

Applications, reports, official letters, resumes, achievement statements, recommendations, plans, training lists, and career summaries are content rules layered on top of a format workflow, not separate file workflows.

Load `references/teacher-admin-rules.md` as the content-rule index, then load only the needed detail file under `references/content-rules/`.

## HTML Slides

When the user asks for new presentation materials, training materials, class materials, slides, or "PPT", default to HTML slides unless they explicitly request `.pptx` or provide an existing PowerPoint file to edit.

**Default style is the My Slides preset** at `references/my-slides/` (Korean Edu Pastel — pastel blue-grey background, cream cards, Plus Jakarta Sans, drawing canvas, dot-toggle inline editing). Follow `references/my-slides/SKILL.md` for the full workflow, `references/my-slides/html-template.md` for the CSS/JS template and component library, and `references/my-slides/animation-patterns.md` for mood-based animation patterns.

Override the default only when the user supplies their own `design.md`, a PDF/screenshot/HTML design source, or explicitly asks for a different preset (e.g., Apple style -> `references/html-slide-apple-style.md`).

Build for desktop classroom or training presentation first, usually 1920x1080. Verify in a local browser and check representative screenshots for overflow, clipped Korean line breaks, and overlapping elements.
