# Changelog

## [2025-06-19]

- Restored application functionality after period of inactivity.
  - Purpose: Ensure the application runs correctly on current system.
  - Technical details:
    - Created new Python 3.11 virtual environment to resolve compatibility issues
    - Installed all dependencies from requirements.txt
    - Verified application runs correctly on port 5001
    - Updated README.md to correctly reference port 5001 instead of 5000
  - Affected files:
    - `README.md`: Updated port reference from 5000 to 5001
    - `.venv`: Recreated with Python 3.11

## [2025-05-14]

- Created Flask web application structure for trouser pattern generator.
  - Purpose: Transform the existing Python script into a web application where users can input measurements and download custom trouser patterns as PDFs.
  - Affected files:
    - `app.py`: Main Flask application
    - `templates/base.html`: Base template with common elements
    - `templates/index.html`: Input form for measurements
    - `templates/success.html`: Download page for generated patterns
    - `templates/about.html`: Information about the application
    - `requirements.txt`: Dependencies needed for the application
  - Note: Original functionality from `garment_pattern.py` is preserved and integrated into the web application flow.

## [2025-05-14 13:30]

- Modified Flask application to use port 5001 instead of default port 5000.
  - Purpose: To resolve conflict with AirPlay Receiver service on macOS which uses port 5000.
  - Affected files:
    - `app.py`: Updated the app.run() line to specify port=5001
  - Note: This change ensures the application can run without port conflicts on macOS systems.

## [2025-05-14 14:05]

- Fixed variable scope issue in pattern generation.
  - Purpose: Fix the "cannot access local variable 'points'" error when generating patterns.
  - Affected files:
    - `garment_pattern.py`: Added initialization of the points dictionary in the save_to_pdf function.
  - Note: This ensures proper variable scoping when generating PDF patterns.

## [2025-05-14 14:15]

- Fixed variable naming inconsistency in pattern generation.
  - Purpose: Fix the "name 'point7' is not defined" error when generating patterns.
  - Affected files:
    - `garment_pattern.py`: Standardized all point references to use the points dictionary in the save_to_pdf function.
  - Note: This ensures consistent variable naming throughout the pattern generation process.

## [2025-05-14 14:18]

- Improved Matplotlib configuration in the web application.
  - Purpose: Fix the warning "Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure."
  - Affected files:
    - `app.py`: Configured Matplotlib to use the non-interactive 'Agg' backend before importing other modules.
  - Note: This ensures proper behavior when running in a web server environment without a display.

## [2025-05-14 14:21]

- Fixed PDF download functionality.
  - Purpose: Resolve issue where clicking "Download PDF Pattern" downloaded an HTML file instead of a PDF.
  - Affected files:
    - `app.py`: Added dedicated download route with proper MIME type handling and file serving.
    - `templates/success.html`: Updated download link to use the new download route.
  - Note: This ensures proper file delivery with correct Content-Type headers and attachment handling.

## [2025-05-14 17:50]

- Added back pattern to PDF output.
  - Purpose: Include both front and back trouser patterns in the generated PDF.
  - Affected files:
    - `garment_pattern.py`: Modified the save_to_pdf function to generate a two-page PDF with front and back patterns.
  - Technical details:
    - Created a second page in the PDF for the back pattern
    - Adjusted key measurements for the back pattern (wider seat, different crotch curve)
    - Added title labels and seam allowance instructions
  - Note: This provides a complete pattern set for users to create both front and back trouser pieces.

## [2025-05-14 18:08]

- Refactored pattern generation architecture to improve consistency.
  - Purpose: Ensure the PDF generation uses the same pattern construction logic as the visualization functions.
  - Affected files:
    - `garment_pattern.py`: Added new functions and restructured code organization.
  - Technical details:
    - Created `draw_trouser_front_pattern_to_pdf` function that mirrors the drawing logic of `draw_trouser_front_pattern`
    - Created `draw_trouser_back_pattern_to_pdf` function that mirrors the drawing logic of `draw_trouser_back_pattern`
    - Modified `save_to_pdf` to use these new functions instead of direct drawing code
    - Preserved all original functions while adding the new PDF-specific versions
  - Note: This architectural change ensures consistency between on-screen visualization and PDF output while reducing code duplication.

## [2025-05-14 18:19]

- Fixed bugs in PDF generation and download functionality.
  - Purpose: Resolve errors when generating and downloading pattern PDFs.
  - Affected files:
    - `garment_pattern.py`: Fixed point calculation and error handling in the `save_to_pdf` function.
    - `app.py`: Fixed file path handling for PDF generation and download.
  - Technical details:
    - Added robust error handling with try/except blocks in the pattern generation code
    - Fixed point "5" reference error that was causing pattern generation to fail
    - Ensured consistent file path handling between generation and download
    - Added defensive point existence checks before attempting to use each point
    - Fixed the download route to properly send files as attachments
  - Note: These changes make the application more robust by preventing errors during pattern generation and ensuring PDFs can be successfully downloaded.

## [2025-05-15 11:08]
- Enhanced trouser back pattern drawing in PDF output.
  - Purpose: Improve the back pattern design with proper curves and easier debugging.
  - Affected files:
    - `garment_pattern.py`: Added detailed drawing for back pattern pieces.
  - Technical details:
    - Created helper functions for geometry calculations (find_midpoint, point_at_distance_with_fixed_x)
    - Improved back fork curve using bezier curves with strategic control points
    - Added numbered point labels for easier debugging and pattern adjustment
    - Implemented curved side seams and hem with proper inward curves
    - Designed proper dart construction with precise angles and position
  - Note: The pattern PDF now includes a complete back trouser pattern with proper garment construction techniques and easy-to-read point labels.
