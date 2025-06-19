# Vionnet Pattern Generator - System Overview

## Architecture
The Vionnet Pattern Generator is a Flask-based web application that provides a user-friendly interface for generating trouser patterns based on custom measurements.

## Key Components

### 1. Core Pattern Generation
- **`garment_pattern.py`**: Contains the mathematical algorithms and drawing functions for creating trouser patterns.
  - Handles geometric calculations (bezier curves, point calculations)
  - Draws front and back trouser patterns
  - Exports patterns to PDF format

### 2. Web Application
- **`app.py`**: Main Flask application file that handles:
  - URL routing
  - Form validation
  - Pattern generation workflow
  - PDF file management

### 3. Templates
- **`base.html`**: Base template with common elements (header, footer, styling)
- **`index.html`**: Measurement input form
- **`success.html`**: Pattern download page
- **`about.html`**: Information about application and measurements

### 4. Static Assets
- **`static/patterns/`**: Directory where generated PDF patterns are stored

## Data Flow
1. User enters measurements in the web form
2. Flask validates the input data
3. The application calls functions from `garment_pattern.py` to generate the pattern
4. A PDF file is created and saved to the static directory
5. User is redirected to the success page with a download link

## Dependencies
The application relies on the following key packages:
- Flask: Web framework
- Flask-WTF: Form handling and validation
- Matplotlib: Pattern visualization
- ReportLab: PDF generation
- NumPy: Mathematical calculations

## Deployment Considerations
- The application is configured to run with Gunicorn for production deployment
- Static file handling is managed through Flask's built-in capabilities
- PDF files are stored in the local filesystem (would need cloud storage for production)
