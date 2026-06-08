# アイリス / Iris

A small terminal AI companion built with Python.

Iris is a lightweight CLI wrapper for chatting with LLMs from the terminal. It is made for clean output, local control, simple code, and future tool support.

> Not a heavy IDE. Not a huge framework. Just a small CLI that grows step by step.

---

## Features

- Python based CLI
- OpenRouter API support
- Rich powered terminal UI
- Markdown response rendering
- Reasoning / thinking display
- Custom UI helper layer
- Termux friendly design

---

## Project Goal

Iris is not only for chatting.

The long term goal is to make a personal CLI assistant that can:

- read project files
- understand local project context
- use small tools
- help with code
- suggest Git commit messages
- check repo status
- push changes safely
- host a lightweight browser code view

---

## Current Status

Iris is still early.

Working now:

- basic chat loop
- API request handling
- terminal response rendering
- local UI helpers

Planned next:

- streaming without flicker
- file read tool
- tool calling system
- command completer
- `@file` autocomplete
- project memory
- Git helper commands
- browser code viewer

---

## Tech Stack

- Python
- Rich
- Requests
- OpenRouter
- Termux / Linux

---

## Structure

```txt
Iris/
├── LICENSE
├── README.md
├── main.py
├── prompts/
│   ├── __init__.py
│   └── sys.py
├── sv1.py
├── theme.py
├── tools/
│   ├── __init__.py
│   ├── mentions.py
│   └── read_file.py
└── ui/
    ├── config.py
    ├── logo.py
    ├── msg_state.py
    ├── rui.py
    └── ui.py
```

---

## Basic Flow

```txt
user input
   ↓
messages
   ↓
to_api()
   ↓
ask_ai()
   ↓
response()
```

---

## Setup

```bash
git clone https://github.com/ssannssarr/Iris
cd Iris
pip install rich requests
```

Set your API key:

```bash
export OPENROUTER_API_KEY="your_api_key_here"
```

Run:

```bash
python main.py
```

---

## Roadmap

### v0.1

- stable chat loop
- clean terminal rendering
- config cleanup

### v0.2

- streaming output
- better markdown rendering
- theme config

### v0.3

- file reader tool
- `@file` autocomplete
- command completer

### v0.4

- Git status helper
- commit message suggestion
- push helper

### v0.5

- local browser code view
- project memory
- small tool system

---

## Author

Built by [Sann](https://github.com/ssannssarr).

A student learning AI, security, Python, CLI systems, and local-first tooling.

---

## License

MIT License
