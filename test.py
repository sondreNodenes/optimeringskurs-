import subprocess
import sys

def check_pipx():
    try:
        result = subprocess.run(["pipx", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("pipx er installert:", result.stdout.strip())
        else:
            print("pipx er ikke installert eller fungerer ikke.")
    except FileNotFoundError:
        print("pipx er ikke installert.")

def check_pyomo():
    try:
        import pyomo
        print("Pyomo er installert, versjon:", pyomo.__version__)
    except ImportError:
        print("Pyomo er ikke installert.")

if __name__ == "__main__":
    check_pipx()
    check_pyomo()