"""Create a new Poetry project with automatic setup and batch runner."""

import os
import subprocess
from pathlib import Path


BATCH_TEMPLATE = """@echo off
cls
title {project_name} Runner
color 2

if exist venv (
    echo Activating existing virtual environment...
    call venv\\Scripts\\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\\Scripts\\activate.bat
    echo Upgrading pip...
    python.exe -m pip install --upgrade pip
    echo Installing Poetry dependencies...
    poetry install
)

cd /d "%~dp0"
cls
echo ---=[ {project_name} ]=---
echo.
python src\\{project_name}\\{project_name}.py
echo.
pause
"""


def create_poetry_project(name: str) -> Path:
    """Create Poetry project and return its path."""
    subprocess.run(['poetry', 'new', name], check=True)
    return Path.cwd() / name


def create_batch_runner(project_dir: Path, project_name: str):
    """Create a simple batch file to run the project."""
    batch_file = project_dir / f"run_{project_name}.bat"
    batch_file.write_text(BATCH_TEMPLATE.format(project_name=project_name))


def create_main_script(project_dir: Path, project_name: str):
    """Create main script file with default template."""
    script_file = project_dir / "src" / project_name / f"{project_name}.py"
    
    template = f'''"""
{project_name} - Main script
"""

def main():
    """Main entry point for {project_name}"""
    print("🚀 {project_name} is running!")
    print("=" * 50)
    
    # Your code here
    
    print("=" * 50)
    print("✅ Done!")


if __name__ == "__main__":
    main()
'''
    script_file.write_text(template, encoding='utf-8')
    return script_file


def prompt_for_dependencies() -> list[str]:
    """Ask user for dependencies to install."""
    print("\n📦 Add dependencies (press Enter with empty input to finish):")
    dependencies = []
    
    while True:
        lib = input(f"  Library {len(dependencies) + 1} (or Enter to skip): ").strip()
        if not lib:
            break
        dependencies.append(lib)
    
    return dependencies


def install_dependencies(project_dir: Path, dependencies: list[str]):
    """Install dependencies using poetry add."""
    if not dependencies:
        print("⏭️  Skipping dependency installation")
        return
    
    print(f"\n📥 Installing {len(dependencies)} dependencies...")
    for lib in dependencies:
        print(f"  - Installing {lib}...")
        subprocess.run(
            ['poetry', 'add', lib],
            cwd=project_dir,
            check=True
        )
    print("✅ All dependencies installed!")


def setup_project_structure(project_dir: Path, project_name: str):
    """Setup the project with batch runner and open tools."""
    # Create batch runner
    create_batch_runner(project_dir, project_name)
    
    # Create main script file
    script_file = create_main_script(project_dir, project_name)
    
    # Ask for dependencies and install them
    dependencies = prompt_for_dependencies()
    install_dependencies(project_dir, dependencies)
    
    # Open main script file for editing
    subprocess.Popen(['notepad', str(script_file)])
    
    # Open Poetry shell for additional commands
    subprocess.Popen(
        f'cmd /k "cd /d {project_dir} && poetry shell && echo Ready! Use: poetry add ^<library^>"',
        shell=True
    )


def main():
    """Main entry point."""
    os.system('cls')
    project_name = input("Project name: ").strip()
    
    if not project_name:
        print("❌ Project name cannot be empty!")
        return
    
    print(f"🚀 Creating project '{project_name}'...")
    project_dir = create_poetry_project(project_name)
    
    print("⚙️  Setting up project structure...")
    setup_project_structure(project_dir, project_name)
    
    print(f"✅ Project '{project_name}' created successfully!")
    print(f"📁 Location: {project_dir}")
    print(f"▶️  Run with: run_{project_name}.bat")


if __name__ == "__main__":
    main()