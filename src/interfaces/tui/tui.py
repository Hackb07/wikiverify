import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from engine.engine import WikiVerifyEngine
import sys

def run_tui():
    parser = argparse.ArgumentParser(description="WikiVerify Pro TUI - Intelligence Auditor")
    parser.add_argument("--flowchart", action="store_true", help="Generate a structure flowchart of the article")
    parser.add_argument("--key-points", action="store_true", help="Extract key points from the article")
    parser.add_argument("--cross-lang", action="store_true", help="Perform cross-language audit (requires French path)")
    args, unknown = parser.parse_known_args()

    console = Console()

    console.print(Panel.fit(
        "[bold magenta]WikiVerify Pro TUI[/bold magenta]\n[italic]The Intelligence Auditor for Global Knowledge[/italic]",
        border_style="magenta"
    ))

    en_data_path = input("Enter English Parquet path (e.g., './data/enwiki/*.parquet'): ")
    if not en_data_path:
        console.print("[red]Error: Data path is required.[/red]")
        return

    engine = WikiVerifyEngine(en_data_path)

    # If cross-lang is requested, ask for the French path
    fr_data_path = None
    if args.cross_lang:
        fr_data_path = input("Enter French Parquet path (e.g., './data/frwiki/*.parquet'): ")

    while True:
        topic = Prompt.ask("\n[bold cyan]Enter a topic to audit[/bold cyan] (or 'exit' to quit)")

        if topic.lower() == 'exit':
            break

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Auditing Wikipedia evidence...", total=None)
            article = engine.search_article(topic)

        if not article:
            console.print("[bold red]❌ Article not found. Please try a more specific topic.[/bold red]")
            continue

        # --- CROSS LANGUAGE AUDIT ---
        if args.cross_lang and fr_data_path:
            console.print("\n[bold blue]🌐 Global Audit Results:[/bold blue]")
            audit_res = engine.cross_language_audit(topic, fr_data_path)
            en_score = audit_res['en']['overall_score'] if audit_res['en'] else 0
            fr_score = audit_res['fr']['overall_score'] if audit_res['fr'] else 0
            console.print(f"English Score: [bold]{en_score}%[/bold] | French Score: [bold]{fr_score}%[/bold]")
            console.print(f"Verdict: [italic]{audit_res['comparison']}[/italic]")

        # Standard Credibility Report
        report = engine.analyze_credibility(article)
        console.print(f"\n[bold yellow]Audit Report for:[/bold yellow] {report['name']}")
        console.print(f"[blue]URL:[/blue] {report['url']}")

        color = "green" if report['overall_score'] > 80 else "yellow" if report['overall_score'] > 50 else "red"
        console.print(Panel(
            f"[bold {color}]Overall Credibility Score: {report['overall_score']}%[/bold {color}]",
            title="Verdict", border_style=color
        ))

        # Metric Table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="dim")
        table.add_column("Value")
        table.add_row("Verified Sections", str(report['verified_sections']))
        table.add_row("Risk Areas", f"[yellow]{report['risk_areas']}[/yellow]")
        table.add_row("Unsupported Claims", f"[red]{report['unsupported_claims']}[/red]")
        table.add_row("Unique Sources", str(report['source_count']))
        table.add_row("Source Diversity", report['diversity'])
        console.print(table)

        # --- KEY POINTS ---
        if args.key_points:
            console.print("\n[bold magenta]📌 Key Points Summary:[/bold magenta]")
            points = engine.extract_key_points(article)
            for point in points:
                console.print(f"• {point}")

        # --- FLOWCHART ---
        if args.flowchart:
            console.print("\n[bold magenta]🗺️ Article Structure Flowchart (Mermaid):[/bold magenta]")
            flowchart = engine.generate_flowchart(article)
            console.print(Panel(flowchart, title="Copy to mermaid.live", border_style="blue"))

if __name__ == "__main__":
    run_tui()
