import os
import sys
import subprocess

def build_executable():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Clean up previous builds
    for dir_name in ['build', 'dist']:
        dir_path = os.path.join(current_dir, dir_name)
        if os.path.exists(dir_path):
            print(f"Cleaning up {dir_name} directory...")
            if sys.platform == 'win32':
                subprocess.run(['rmdir', '/s', '/q', dir_path], shell=True)
            else:
                subprocess.run(['rm', '-rf', dir_path])
    
    # Build the executable
    print("Building executable...")
    subprocess.run([
        'pyinstaller',
        '--name=InteractiveApp',
        '--windowed',  # No console window
        '--onefile',   # Single executable
        '--clean',     # Clean PyInstaller cache
        'main.py'
    ])
    
    print("\nBuild completed!")
    print("The executable can be found in the 'dist' folder.")

if __name__ == "__main__":
    build_executable() 