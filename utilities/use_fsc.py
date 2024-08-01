import os

def add_fsc_to_path(project_path):
    fsc_path = os.path.join(project_path, "fsc28_linux64")
    
    # Get the current PATH
    path = os.getenv("PATH")
    
    # Add the fsc_path to PATH if it's not already there
    if fsc_path not in path:
        os.environ["PATH"] = f"{path}:{fsc_path}"
        print("Added fsc28 to PATH")
    else:
        print("fsc28 is already in PATH")

    # Check if fsc28 is now in PATH
    path = os.getenv("PATH")
    if fsc_path in path:
        print("IN PATH")
    else:
        print("NOT IN PATH")
