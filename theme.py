import json
from rich.console import Console

console = Console()

UI_FILE = ".ui.json"


def load_ui():
    try:
        with open(UI_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "panel": "#89b4fa",
            "thinking": "#74c7ec",
            "assistant": "#a6e3a1",
            "error": "#f38ba8"
        }


def save_ui(data):
    with open(UI_FILE, "w") as f:
        json.dump(data, f, indent=4)


def preview(color):
    console.print(
        f"[{color}]████████████████████[/] {color}"
    )


def pick_hex(prompt):
    while True:
        color = input(f"{prompt}: ").strip()

        if color.startswith("#"):
            color = color[1:]

        if len(color) in (3, 6) and all(
            c in "0123456789abcdefABCDEF"
            for c in color
        ):
            return f"#{color}"

        console.print("[red]Invalid hex color[/]")


def main():
    ui = load_ui()

    while True:
        console.print("\n[bold]Theme Editor[/]\n")

        keys = list(ui.keys())

        for i, key in enumerate(keys, start=1):
            console.print(
                f"{i}. {key:<12} {ui[key]}"
            )
            preview(ui[key])

        console.print("\n0. Save & Exit")

        try:
            choice = int(input("\nChoice: "))
        except ValueError:
            continue

        if choice == 0:
            save_ui(ui)
            console.print("\n[green]Theme saved![/]")
            break

        if 1 <= choice <= len(keys):
            key = keys[choice - 1]

            console.print(f"\nEditing: [bold]{key}[/]")
            color = pick_hex("New hex")

            preview(color)

            confirm = input(
                "Use this color? (y/n): "
            ).lower()

            if confirm == "y":
                ui[key] = color


if __name__ == "__main__":
    main()
