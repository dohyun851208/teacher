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

## Pre-Publish Checks

Run these from this `github-ready/` folder before publishing:

```powershell
rg -n "PRIVATE_NAME|PRIVATE_PHONE|PRIVATE_EMAIL|PRIVATE_ADDRESS|PRIVATE_ACCOUNT" teacher
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .\teacher
```
