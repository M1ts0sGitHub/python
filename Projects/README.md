Poetry Project Creator 🚀
A streamlined Python script that automates the creation of Poetry projects with virtual environment setup, dependency management, and a ready-to-run batch file.
Features ✨

Automated Poetry Project Creation: Creates a complete Poetry project structure with one command
Interactive Dependency Management: Prompts for libraries and installs them automatically
Virtual Environment Setup: Generates a batch file that handles venv creation and activation
Ready-to-Code Template: Creates a main script with a clean template and best practices
Developer-Friendly: Opens your editor and Poetry shell automatically

Requirements 📋

Python 3.7+
Poetry installed and available in PATH
Windows OS (batch file support)

Installation 🔧

Save the script as create_poetry_project.py
Ensure Poetry is installed:

bash   pip install poetry
Usage 🎯

Run the script:

bash   python create_poetry_project.py

Enter your project name when prompted:

   Project name: myproject

Add dependencies interactively (or press Enter to skip):

   📦 Add dependencies (press Enter with empty input to finish):
     Library 1 (or Enter to skip): streamlit
     Library 2 (or Enter to skip): pandas
     Library 3 (or Enter to skip):

The script will:

Create the Poetry project structure
Install all specified dependencies
Generate a run_myproject.bat file
Open your main script in Notepad
Launch a Poetry shell in a new terminal



Generated Project Structure 📁
myproject/
├── run_myproject.bat          # Batch file to run your project
├── pyproject.toml             # Poetry configuration
├── README.md                  # Project readme
├── tests/                     # Test directory
└── src/
    └── myproject/
        ├── __init__.py        # Package init (empty)
        └── myproject.py       # Your main script ⭐
Running Your Project ▶️
Simply double-click or run the generated batch file:
bashrun_myproject.bat
The batch file will:

Create a virtual environment (first run only)
Install dependencies via Poetry (first run only)
Activate the virtual environment
Run your main script

Main Script Template 📝
The generated {project_name}.py includes:
pythondef main():
    """Main entry point for {project_name}"""
    print("🚀 {project_name} is running!")
    print("=" * 50)
    
    # Your code here
    
    print("=" * 50)
    print("✅ Done!")

if __name__ == "__main__":
    main()
Adding More Dependencies Later 📦
You can add more libraries anytime:

Use the opened Poetry shell:

bash   poetry add library_name

Or activate Poetry shell manually:

bash   cd myproject
   poetry shell
   poetry add library_name
How It Works 🔍

Project Creation: Uses poetry new to create the standard Poetry structure
Dependency Installation: Runs poetry add for each specified library
Batch File Generation: Creates a smart batch file that:

Checks for existing venv
Creates and activates venv on first run
Installs dependencies via poetry install
Runs your Python script


Developer Tools: Opens Notepad with your script and a Poetry shell for immediate work

Customization 🎨
You can modify the script to:

Change the text editor (replace notepad with your preferred editor)
Adjust the batch file template
Modify the main script template
Add additional setup steps

Troubleshooting 🔧
Poetry command not found:

Ensure Poetry is installed and in your PATH
Restart your terminal after installing Poetry

Dependencies not installing:

Check your internet connection
Verify the package name is correct on PyPI

Batch file not running:

Ensure Python is in your PATH
Run python --version to verify

License 📄
Free to use and modify as needed.
Author ✍️
Created for rapid Python project setup with Poetry.
