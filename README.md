# Interactive Python GUI Application

This is a simple local app built with python. It was built by myself, Henry Pharris, with icons by Icons8. It uses a bootleg justwatch api along with control macros to automatically search for and open videos and movies to your current position. Im unsure if this violates streaming services' TOS so use at your own risk.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the application in development mode:
```bash
python main.py
```

## Building the Executable

To create a standalone executable:
```bash
python build.py
```

The executable will be created in the `dist` folder.

## Features

- Modern GUI interface
- Interactive buttons and input fields
- Responsive layout
- Easy to extend and modify 