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
            "panel": "bright_magenta",
            "prompt": "white",
            "statusline": "bold violet"
        }


def save_ui(data):
    with open(UI_FILE, "w") as f:
        json.dump(data, f, indent=4)


def preview(color):
    try:
        console.print(
            f"[{color}]████████████████████[/] {color}"
        )
    except Exception:
        console.print(
            f"[red]Cannot preview:[/] {color}"
        )


def is_hex(color):
    if color.startswith("#"):
        color = color[1:]

    return len(color) in (3, 6) and all(
        c in "0123456789abcdefABCDEF"
        for c in color
    )


def is_rgb(color):
    parts = color.split(",")

    if len(parts) != 3:
        return False

    try:
        nums = [int(p.strip()) for p in parts]
        return all(0 <= n <= 255 for n in nums)
    except ValueError:
        return False


def pick_color(prompt):
    console.print(
        "\n1. Hex (#89b4fa)"
        "\n2. RGB (137,180,250)"
        "\n3. Rich color name (cyan)"
    )

    while True:
        mode = input("\nColor type: ").strip()
        if mode in ("1", "2", "3"):
            break
        console.print(
            "[red]Invalid option. Choose 1, 2 or 3[/]"
        )

    while True:
        color = input(f"{prompt}: ").strip()

        if mode == "1":
            if is_hex(color):
                if not color.startswith("#"):
                    color = "#" + color
                return color

            console.print("[red]Invalid hex color[/]")

        elif mode == "2":
            if is_rgb(color):
                r, g, b = [
                    int(x.strip())
                    for x in color.split(",")
                ]
                return f"rgb({r},{g},{b})"

            console.print(
                "[red]Invalid RGB. Example: 137,180,250[/]"
            )

        elif mode == "3":
            return color


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
            console.print(
                "\n[green]Theme saved![/]"
            )
            break

        if 1 <= choice <= len(keys):
            key = keys[choice - 1]

            console.print(
                f"\nEditing: [bold]{key}[/]"
            )

            color = pick_color("New color")

            console.print("\nPreview:")
            preview(color)

            confirm = input(
                "\nUse this color? (y/n): "
            ).lower()

            if confirm == "y":
                ui[key] = color


if __name__ == "__main__":
    main()
