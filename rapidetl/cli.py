import typer
import time
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich import print as rprint
from .rapidetl import run_pipeline

# Create a new Typer app with a default command
app = typer.Typer()
console = Console()

def create_progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[bold green]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    )

# Make this the default command
@app.callback(invoke_without_command=True)
def main(
    config_path: Path = typer.Argument(
        ...,
        help="Path to the pipeline configuration JSON file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    )
):
    """
    RapidETL - Fast and Simple ETL Pipeline Runner
    """
    start_time = time.time()
    
    try:
        # Show welcome message
        console.print(Panel.fit(
            "[bold blue]RapidETL Pipeline Runner[/bold blue]", 
            subtitle="[italic]Fast and Simple ETL Pipelines[/italic]"
        ))
        
        with create_progress() as progress:
            # Add overall progress task
            main_task = progress.add_task("[cyan]Running Pipeline...", total=100)
            
            # Load config
            progress.update(main_task, advance=20, description="[cyan]Loading configuration...")
            config = str(config_path)
            
            # Run pipeline with progress updates
            def progress_callback(stage: str, percent: float):
                progress.update(main_task, 
                              description=f"[cyan]{stage}",
                              completed=20 + (percent * 80))
            
            run_pipeline(config, progress_callback)
            
            # Ensure progress reaches 100%
            progress.update(main_task, completed=100, description="[green]Pipeline Complete!")
        
        # Calculate and show execution time
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Show success message with timing
        console.print("\n[bold green]Pipeline executed successfully! ✨[/bold green]")
        console.print(f"[yellow]Total execution time: {execution_time:.2f} seconds[/yellow]")
        
    except Exception as e:
        # Show error message in red
        console.print(f"\n[bold red]Error running pipeline: {str(e)}[/bold red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app() 