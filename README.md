# Vionnet Pattern Generator

A web application that generates custom trouser patterns based on user measurements.

## Features

- Input custom body measurements through a user-friendly web interface
- Generate accurate trouser patterns based on your specific measurements
- Download patterns as ready-to-print PDF files
- Responsive design that works on desktop and mobile devices

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourname/vionnet.git
cd vionnet
```

2. Create and activate a virtual environment (Python 3.11 recommended for compatibility):
```bash
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

   Note: If you encounter dependency issues, make sure you're using Python 3.11 as newer versions may have compatibility problems with some dependencies.

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask development server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5001/
```

3. Enter your measurements in the form and click "Generate Pattern"

4. Download the generated PDF pattern from the success page

## Required Measurements

- **Waist (cm)**: Circumference around your natural waistline
- **Seat (cm)**: Circumference around the fullest part of your buttocks
- **Body Rise (cm)**: Distance from waist to seat when seated
- **Inseam (cm)**: Length from crotch to floor along the inside of your leg
- **Trouser Bottom Width (cm)**: Desired width of each trouser leg at the hem
- **Waistband Depth (cm)**: Desired width of the waistband

## Project Structure

```
vionnet/
├── app.py                 # Main Flask application
├── garment_pattern.py     # Pattern generation functions
├── requirements.txt       # Project dependencies
├── CHANGELOG.md           # Record of changes
├── SYSTEM_OVERVIEW.md     # System architecture documentation
├── static/                # Static files
│   └── patterns/          # Generated pattern PDFs
└── templates/             # HTML templates
    ├── base.html          # Base template with common elements
    ├── index.html         # Pattern generation form
    ├── success.html       # Download page
    └── about.html         # Information page
```

## How It Works

The application uses mathematical algorithms to generate precise trouser patterns based on key body measurements. The core pattern generation logic is contained in `garment_pattern.py`, which handles:

1. Calculating all necessary points based on measurements
2. Drawing curved and straight pattern lines
3. Creating both front and back trouser panels
4. Exporting the pattern to a printable PDF format

## License

[MIT License](LICENSE)
