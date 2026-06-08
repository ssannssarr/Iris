# Iris v0.1 Pre-release Notes

First public checkpoint of Iris.

Iris is still early, but the base CLI idea is now shaped: a small Python terminal AI wrapper with clean Rich UI, simple API calls, and space for future tools.

---

## Status

**Version:** v0.1 pre-release  
**Branch:** main  
**State:** experimental

This is not a stable release yet. It is a working base for testing, rebuilding, and improving the core flow.

---

## What works now

- Basic terminal chat loop
- OpenRouter API connection
- Assistant response rendering
- Rich-based terminal UI helpers
- Markdown-style output
- Separate UI helper files
- Early reasoning/thinking display support
- Simple project structure for future growth

---

## Main idea

Iris is not meant to be a heavy IDE or a big framework.

The goal is:

- small CLI assistant
- readable Python code
- clean terminal output
- local project awareness later
- tool-calling support later
- phone-friendly development through Termux

---

## Known limitations

- Streaming is not fully stable yet
- Tool calling is not connected yet
- File reading tool is planned but not finished
- Theme/config system is still early
- Some code may still need cleanup
- README and docs are still being shaped

---

## Planned for next builds

- Stable streaming output
- Less flicker in terminal rendering
- `@file` autocomplete
- Command completer
- File read tool
- Git status helper
- Commit message suggestion
- `iris push` helper
- Project memory loading
- Lightweight browser code view mode

---

## Notes

This pre-release is mainly a marker:

> Iris has started walking.

Next step is making it useful, stable, and less spaghetti.
