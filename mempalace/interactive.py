import sys
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.panel import Panel
import shlex

console = Console()

COMMANDS = {
    "init": "Detect rooms from folder structure",
    "mine": "Ingest project files or conversations",
    "search": "Find anything in your palace",
    "wake-up": "Show essential context (L0 + L1)",
    "status": "Show what's been filed",
    "split": "Split mega-files into sessions",
    "compress": "Compress drawers (~30x reduction)",
    "repair": "Rebuild vector index",
}

EXAMPLES = {
    "init": ".",
    "mine": ". --wing my-app",
    "search": '"why did we use GraphQL?"',
    "wake-up": "--wing my-app",
    "split": "chats/ --output-dir sessions/",
    "compress": "--wing my-app",
}

def show_interactive_menu():
    console.clear()
    console.print(Panel.fit(
        "[bold magenta]MemPalace[/bold magenta] [white]Interactive Selection[/white]",
        border_style="magenta",
        padding=(0, 2)
    ))

    choices = [
        Choice(name=f"{cmd.ljust(10)} - {desc}", value=cmd)
        for cmd, desc in COMMANDS.items()
    ]
    choices.append(Choice(value=None, name="Exit"))

    selected_cmd = inquirer.select(
        message="Choose a command:",
        choices=choices,
        default="init",
        pointer=">",
        qmark='-',
        amark='>'
    ).execute()

    if selected_cmd is None:
        sys.exit(0)

    # Pre-fill example parameters
    example = EXAMPLES.get(selected_cmd, "")
    console.print(f"\n[bold yellow]Parameters for {selected_cmd}[/bold yellow]")
    if example:
        console.print(f"[dim]Suggestion: {example}[/dim]")

    params = inquirer.text(
        message=f"mempalace {selected_cmd}",
        default=example,
        qmark='>',
        amark='>',
    ).execute()

    console.print("\n[bold green] Executing command...[/bold green]\n")

    try:
        args_list = [selected_cmd] + shlex.split(params)
    except ValueError:
        args_list = [selected_cmd] + params.split()

    return args_list

if __name__ == "__main__":
    show_interactive_menu()
