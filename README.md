# teacher

Claude/Codex skill for Korean teacher administrative documents: HWP/HWPX forms, XLS/XLSX templates, official documents, resumes, achievement statements, training/career lists, and HTML-based class or training slides.

## Repository Layout

- `teacher/`: publishable Claude/Codex skill folder
- `teacher/SKILL.md`: shared skill metadata and core workflow
- `teacher/agents/openai.yaml`: Codex UI metadata
- `teacher/references/`: workflow notes loaded only when needed
- `teacher/scripts/`: HWPX utilities and verification helpers
- `teacher/templates/`: reusable HWPX XML templates

## Not Included

This release folder intentionally excludes private project data such as personal profiles, signatures, ID cards, certificates, bankbook images, original evidence files, and completed submission outputs.

## Install Locally

For Codex, copy `teacher/` into your Codex skills directory:

```powershell
Copy-Item -Recurse -Force .\teacher "$env:USERPROFILE\.codex\skills\teacher"
```

For Claude Code, copy the same `teacher/` folder into Claude's skills directory:

```powershell
Copy-Item -Recurse -Force .\teacher "$env:USERPROFILE\.claude\skills\teacher"
```

## Usage Notes

- Name a long-running teacher workspace folder with `(AI)` at the end to make it a teacher workspace.
- On first setup, the skill indexes folder names, filenames, and extensions first, then creates `docs/00_폴더지도.md`, `docs/01_분류기준.md`, and `docs/02_자료목록.md`.
- The skill does not read every source document during setup. It opens originals only when relevant to the current task or a requested summary.
- For a one-off file outside the workspace, the result is saved next to the source file with `_완성본` appended.

## Pre-Publish Checks

Run these from this `github-ready/` folder before publishing:

```powershell
rg -n "PRIVATE_NAME|PRIVATE_PHONE|PRIVATE_EMAIL|PRIVATE_ADDRESS|PRIVATE_ACCOUNT" teacher
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .\teacher
```
