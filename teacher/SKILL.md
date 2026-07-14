---
name: teacher
description: Create, fill, and verify Korean school teacher administrative documents and teaching materials. Use when any referenced target file path, filename, or attachment ends in .hwp, .hwpx, .xls, or .xlsx; OR when working with HWP/HWPX forms, XLS/XLSX templates, applications, official letters, reports, resumes, achievement statements, meeting minutes, budget requests, training or career lists, HTML-based class or training slides; OR when the current folder or any ancestor/project folder name ends with "(AI)" or "(ai)" case-insensitively; OR when an external single-file Korean school document path is supplied, especially when preserving form layout, merged cells, HWPX XML structure, signatures, or browser-presented slide decks matters.
---

# Teacher

## Overview

Use this skill to route Korean teacher paperwork requests into the right document workflow, preserve original form structure, and keep private profile data outside the reusable skill package.

Start every task by reading `references/routing.md`, then load only the format workflow and content-rule references that match the request.

For first-time `(AI)` teacher workspaces, folder indexing, source-to-Markdown summaries, or external single-file handling, use `references/project-setup.md`.

## Context And Privacy

- Treat user-provided project files as the source of truth for personal data, evidence files, forms, and design references.
- Treat `(AI)` workspace detection and target-file extension detection as OR conditions: follow this skill if the current/ancestor work folder ends with `(AI)` or if the user request references any target path, filename, or attachment ending in `.hwp`, `.hwpx`, `.xls`, or `.xlsx`, even outside an `(AI)` workspace.
- If the user gives a target file or folder path, decide the teacher workspace from that target path before using the current shell folder. If the target path or one of its ancestor folders ends with `(AI)` case-insensitively, use the nearest such `(AI)` folder as the work folder.
- Interpret project-internal paths as relative to the chosen work folder unless the user explicitly provides another external absolute path.
- Prefer structured Markdown in the user's `docs/` folder before opening original evidence files.
- If the current folder or any ancestor/project folder name ends with `(AI)` case-insensitively, follow this skill's routing even when the user does not explicitly type `$teacher`. For example, work inside `./양식(AI)/서명넣기/` is still inside the `양식(AI)` teacher workspace.
- When modifying or filling an existing source file, save the output next to the source file with a suffix such as `_완성본`, `_제출용`, or `_검토본`; do not create a separate `완성본/` folder unless the user explicitly asks for one. Do not overwrite the original file. For newly created files with no source file, save in the current work folder using the same suffix rule.
- If the user supplies an external file path whose path and ancestors do not include an `(AI)` folder, treat the source file's parent as the work folder and save the result next to the source file using a suffix such as `_완성본`, `_제출용`, or `_검토본`.
- Do not scan or read every original file during first setup. Start from folder names, filenames, and extensions; open source files only when they are relevant to the user's current task or a requested summary.
- Use `references/profile-schema.md` as the recommended private-project data layout.
- Do not copy actual personal data, signatures, ID cards, certificates, bankbook images, or completed output files into this skill.
- Select the shell for the current operation, not for the whole skill or conversation. Use PowerShell for every shell command that opens, converts, edits, or validates `.hwp`/`.hwpx`, or invokes Hancom COM. Re-select when the target format changes; use the current workflow's shell for XLS/XLSX, general Python, and HTML work.
- Do not assume the working directory, interpreter variables, or environment variables persist when changing shells. Prefer absolute paths and repeat the HWP/HWPX PowerShell UTF-8 bootstrap whenever that workflow resumes.
- Treat user-provided Korean source documents as valid by default. Garbled console output alone is a display or decoding issue, not evidence of source corruption. Do not re-encode or overwrite the source; inspect raw bytes only when explicit parsing or structural validation also fails.
- Save created or modified text files as UTF-8. In Python, pass `encoding="utf-8"` whenever reading or writing text.
- In Bash commands that run Python with Korean paths or text, use the per-command prefix `PYTHONUTF8=1 PYTHONIOENCODING=utf-8`; do not assume an earlier `export` persists. When the producer's encoding is unclear, do not create Korean text files through `>` redirection; use the agent's file-writing tool or Python with explicit UTF-8 instead.
- At the start of each PowerShell HWP/HWPX operation, set UTF-8 explicitly:

```powershell
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
```

## Workflow Routing

1. Read `references/routing.md`.
2. Choose the output-format workflow first:
   - HWP/HWPX forms or HWPX documents: `references/workflows/hwpx-forms.md`
   - XLS/XLSX forms or spreadsheet tables: `references/workflows/xlsx-forms.md`
   - HTML slides and training/class materials: `references/workflows/html-slides.md`
   - Existing `.ppt`/`.pptx` files: use a PowerPoint workflow only when the user explicitly asks to edit the provided file.
3. If the task is a resume, achievement statement, application, meeting minutes, budget request, official letter, report, training list, or career summary, also load `references/teacher-admin-rules.md` and the matching `references/content-rules/*.md` file.
4. For HTML slides, also load the relevant style reference:
   - Design sources: `references/html-slide-design-sources.md`
   - Apple-style preset: `references/html-slide-apple-style.md`
   - **My Slides preset (Korean Edu Pastel, default for PPT/slide requests): `references/my-slides/SKILL.md`** — pastel blue-grey background, cream cards, Plus Jakarta Sans, drawing canvas, inline-edit dot toggle, viewport/accessibility safeguards. Use this by default when the user asks for slides, PPT, presentation, training, or class materials, unless they specify a different style.
5. Preserve original formatting, merged cells, tables, images, margins, fonts, and alignment unless the user asks for a redesign.
6. Verify the result by extracting text, checking structure, or using the format-specific workflow. For HWPX-only deliverables, use structural validation and key value checks by default, not PDF/image rendering or extra HWPX verification copies.

## HWP And HWPX

Assume Hancom COM automation is always available; never ask the user about availability. The only pre-check is `scripts/setup_env.py`, run once on a machine's first HWP task (or whenever `hwp_to_hwpx.py` prints `WARN: 보안모듈 등록 실패`): it verifies pywin32 and Hancom COM, and if the HWP automation security module is missing it copies the bundled `scripts/FilePathCheckerModule.dll` to `%LOCALAPPDATA%\FilePathCheckerModule\` and registers it under HKCU so no security-approval dialogs interrupt or hang automation. It is idempotent — safe to re-run on an already-configured PC. For a source `.hwp`, immediately run one COM conversion to a temporary `.hwpx` with `scripts/hwp_to_hwpx.py`, then edit the HWPX ZIP/XML directly, validate, and save only `*_완성본.hwpx` next to the source. Never re-save the final HWPX through Hancom COM and never create a final `.hwp`.

```powershell
& $py "scripts/hwp_to_hwpx.py" "원본.hwp" -o "임시작업본.hwpx"
```

`references/workflows/hwpx-forms.md` is the canonical HWP/HWPX workflow. Follow it for the full default path, prohibited fallbacks, conversion-failure handling, and verification rules.

For `.hwpx`, analyze before editing:

```powershell
& $py "scripts/clone_form.py" --analyze "input.hwpx"
```

Confirm table text and key values by inspecting `Contents/section0.xml` directly. Use `scripts/text_extract.py` only as optional extra validation when `python-hwpx` is already available; it must not be part of the default path.

For simple form text replacement, preserve the ZIP/XML structure:

```powershell
& $py "scripts/clone_form.py" "input.hwpx" "output.hwpx" --map "map.json"
```

For filling table cells by address (empty or already filled), use the bundled filler as the default path. `--list` prints every table and cell address with its current text; `--map` fills cells from a JSON map, then automatically reports a structure comparison and per-cell PASS/FAIL — no separate verification pass needed:

```powershell
& $py "scripts/fill_cells.py" "input.hwpx" --list
& $py "scripts/fill_cells.py" "input.hwpx" "output.hwpx" --map "cells.json"
```

Fall back to editing `Contents/section0.xml` by hand only when `fill_cells.py` cannot express the change (for example mixed character styles inside one cell). When editing manually, prefer preserving each target cell's original paragraph/run structure and replacing text inside existing runs; clear leftover runs so stale text cannot remain. Keep the final deliverable as `.hwpx`; do not save back to `.hwp`.

For low-level HWPX creation or repair, use the bundled helpers and templates:

- `scripts/build_hwpx.py`
- `scripts/md2hwpx.py`
- `scripts/fix_namespaces.py`
- `scripts/validate.py`
- `scripts/verify_hwpx.py`
- `templates/`
- `references/hwpx/`

Do not use `md2hwpx.py` or a rebuilt Markdown table as a fallback for filling an existing HWP form unless the user explicitly accepts a redesigned/recreated form. It does not preserve the original table widths, row heights, merged cells, or border details.

## XLS And XLSX

Use `openpyxl` for `.xls` and `.xlsx` workflows when possible. Before writing values, inspect sheet names, merged ranges, header rows, and the data region. Write values only to the top-left cell of a merged range, preserve styles, and reopen the workbook after saving to confirm values, merges, borders, fonts, alignment, and row heights.

## Content Rules

Applications, reports, official letters, resumes, achievement statements, meeting minutes, budget requests, recommendations, plans, training lists, and career summaries are content rules layered on top of a format workflow, not separate file workflows.

Load `references/teacher-admin-rules.md` as the content-rule index, then load only the needed detail file under `references/content-rules/`.

## HTML Slides

When the user asks for new presentation materials, training materials, class materials, slides, or "PPT", default to HTML slides unless they explicitly request `.pptx` or provide an existing PowerPoint file to edit.

**Default style is the My Slides preset** at `references/my-slides/` (Korean Edu Pastel — pastel blue-grey background, cream cards, Plus Jakarta Sans, drawing canvas, dot-toggle inline editing). Follow `references/my-slides/SKILL.md` for the full workflow, `references/my-slides/html-template.md` for the CSS/JS template and component library, and `references/my-slides/animation-patterns.md` for mood-based animation patterns.

Override the default only when the user supplies their own `design.md`, a PDF/screenshot/HTML design source, or explicitly asks for a different preset (e.g., Apple style -> `references/html-slide-apple-style.md`).

Build for desktop classroom or training presentation first, usually 1920x1080. Verify in a local browser and check representative screenshots for overflow, clipped Korean line breaks, and overlapping elements.
