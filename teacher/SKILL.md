---
name: teacher
description: Create, fill, and verify Korean school teacher administrative documents and teaching materials. Use when working with HWP/HWPX forms, XLS/XLSX templates, applications, official letters, reports, resumes, achievement statements, training or career lists, HTML-based class or training slides, any current/project folder whose name ends with "(AI)", or an external single-file Korean school document path supplied by the user, especially when preserving form layout, merged cells, HWPX XML structure, signatures, or browser-presented slide decks matters.
---

# Teacher

## Overview

Use this skill to route Korean teacher paperwork requests into the right document workflow, preserve original form structure, and keep private profile data outside the reusable skill package.

Start every task by reading `references/routing.md`, then load only the workflow reference that matches the request and file type.

For first-time `(AI)` teacher workspaces, folder indexing, source-to-Markdown summaries, or external single-file handling, use `references/project-setup.md`.

## Context And Privacy

- Treat user-provided project files as the source of truth for personal data, evidence files, forms, and design references.
- Prefer structured Markdown in the user's `docs/` folder before opening original evidence files.
- If the current folder or nearest project root ends with `(AI)`, follow this skill's routing even when the user does not explicitly type `$teacher`.
- If the user supplies an external file path for a one-off school document, process it in place as a single-file task and save the result next to the source file with `_완성본` appended.
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
2. Identify whether the task is filling an existing form, creating a new document, creating spreadsheet data, or building slides.
3. Load the matching reference:
   - HWP/HWPX forms: `references/hwpx-forms.md`
   - XLS/XLSX forms: `references/xlsx-forms.md`
   - Applications, official letters, reports, resumes, achievement statements: `references/teacher-admin-rules.md`
   - HTML slides and training materials: `references/html-slides.md`
   - Design references for HTML slides: `references/html-slide-design-sources.md`
   - Apple-style slide preset: `references/html-slide-apple-style.md`
4. Preserve original formatting, merged cells, tables, images, margins, fonts, and alignment unless the user asks for a redesign.
5. Verify the result by reopening, extracting text, checking workbook structure, rendering, or screenshotting as appropriate.

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

## Teacher Documents

For applications, reports, official letters, resumes, achievement statements, recommendations, plans, training lists, and career summaries:

- Follow the user's explicit instructions first.
- Prefer the user's `docs/*.md` summaries over raw evidence files.
- Use official school names unless the form width requires abbreviations.
- Fit long content to the form width by summarizing rather than overflowing.
- Keep temporary analysis files and private notes out of final deliverables.

## HTML Slides

When the user asks for new presentation materials, training materials, class materials, slides, or "PPT", default to HTML slides unless they explicitly request `.pptx` or provide an existing PowerPoint file to edit.

Build for desktop classroom or training presentation first, usually 1920x1080. Use the user's `design.md`, existing HTML/CSS, PDF, screenshots, or images as design sources when present. Verify in a local browser and check representative screenshots for overflow, clipped Korean line breaks, and overlapping elements.
