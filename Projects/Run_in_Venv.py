import subprocess

def create_run_project_bat(script_name):
    batch_content = fr"""@echo off
                        cls
                        title Script Runner
                        color 2
                        if exist venv (
                            echo Virtual environment already exists. Activating...
                            call venv\Scripts\activate.bat
                        ) else (
                            echo Create a virtual environment in the current folder
                            python -m venv venv
                            echo Activate the virtual environment
                            call venv\Scripts\activate.bat
                            poetry export -f requirements.txt --output requirements.txt --without-hashes
                            echo Install dependencies from requirements.txt
                            python.exe -m pip install --upgrade pip
                            pip install -r requirements.txt
                        )
                        echo Run the script using the virtual environment's python
                        timeout 2
                        cls
                        echo ---=[ Start of Script ]=---
                        echo.
                        python {script_name}
                        echo.
                        echo ---=[ End of Script ]=---
                        timeout 60
                    """

    with open("run_project.bat", "w", encoding="utf-8") as f:
        f.write(batch_content)
    return "run_project.bat"

# Example usage: pass the script filename you'd like to run
subprocess.Popen(create_run_project_bat("__init__.py"), creationflags=subprocess.CREATE_NEW_CONSOLE)
