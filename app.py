from flask import Flask, render_template, request, send_file, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import os
import uuid
from datetime import datetime

# Configure matplotlib to use non-interactive backend before importing it elsewhere
import matplotlib
matplotlib.use('Agg')  # This prevents the 'Matplotlib is currently using agg' warning

import io

# Import the pattern generation functions after matplotlib configuration
from garment_pattern import draw_trouser_pattern_points, draw_trouser_front_pattern, draw_trouser_back_pattern, save_to_pdf

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-key-for-forms'
app.config['UPLOAD_FOLDER'] = 'static/patterns'

# Ensure the patterns directory exists
os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)

# Default example values from garment_pattern.py
DEFAULT_WAIST = 100.33  # cm
DEFAULT_SEAT = 107.95  # cm
DEFAULT_BODY_RISE = 29.21  # cm
DEFAULT_INSEAM = 86.36  # cm
DEFAULT_TROUSER_BOTTOM_WIDTH = 22.6  # cm
DEFAULT_WAISTBAND_DEPTH = 4  # cm

class MeasurementForm(FlaskForm):
    waist = FloatField('Waist (cm)', validators=[DataRequired(), NumberRange(min=50, max=200)], 
                      default=DEFAULT_WAIST)
    seat = FloatField('Seat (cm)', validators=[DataRequired(), NumberRange(min=50, max=200)],
                     default=DEFAULT_SEAT)
    body_rise = FloatField('Body Rise (cm)', validators=[DataRequired(), NumberRange(min=10, max=50)],
                          default=DEFAULT_BODY_RISE)
    inseam = FloatField('Inseam (cm)', validators=[DataRequired(), NumberRange(min=50, max=120)],
                       default=DEFAULT_INSEAM)
    trouser_bottom_width = FloatField('Trouser Bottom Width (cm)', validators=[DataRequired(), NumberRange(min=10, max=50)],
                                     default=DEFAULT_TROUSER_BOTTOM_WIDTH)
    waistband_depth = FloatField('Waistband Depth (cm)', validators=[DataRequired(), NumberRange(min=2, max=10)],
                                default=DEFAULT_WAISTBAND_DEPTH)
    submit = SubmitField('Generate Pattern')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MeasurementForm()
    if form.validate_on_submit():
        # Get measurements from form
        waist = form.waist.data
        seat = form.seat.data
        body_rise = form.body_rise.data
        inseam = form.inseam.data
        trouser_bottom_width = form.trouser_bottom_width.data
        waistband_depth = form.waistband_depth.data
        
        # Generate a unique filename with UUID (to match existing pattern)
        filename = f"trouser_pattern_{uuid.uuid4().hex[:8]}.pdf"
        
        # Ensure the patterns directory exists
        patterns_dir = os.path.join(app.static_folder, "patterns")
        os.makedirs(patterns_dir, exist_ok=True)
        
        # Set the full path for the PDF file
        pdf_path = os.path.join(patterns_dir, filename)
        
        try:
            # Log the measurements for debugging
            app.logger.info(f"Generating pattern with measurements: waist={waist}, seat={seat}, body_rise={body_rise}, inseam={inseam}, trouser_bottom_width={trouser_bottom_width}, waistband_depth={waistband_depth}")
            
            # Convert measurements to float to avoid potential string issues
            waist = float(waist)
            seat = float(seat)
            body_rise = float(body_rise)
            inseam = float(inseam)
            trouser_bottom_width = float(trouser_bottom_width)
            waistband_depth = float(waistband_depth)
            
            # Calculate pattern points
            trouser_points = draw_trouser_pattern_points(
                body_rise, waist, waistband_depth, trouser_bottom_width, inseam, seat, show_plot=False
            )
            
            # Save pattern to PDF
            save_to_pdf(
                body_rise, waist, waistband_depth, trouser_bottom_width, inseam, seat, pdf_path
            )
            
            # Redirect to the success page with the filename for download
            return redirect(url_for('success', filename=os.path.basename(pdf_path)))
        except ValueError as e:
            flash(f"Invalid measurement value: {e}")
            return render_template('index.html', form=form)
        except Exception as e:
            app.logger.error(f"Error generating pattern: {str(e)}", exc_info=True)
            flash(f"Error generating pattern: {str(e)}")
            return render_template('index.html', form=form)
    
    return render_template('index.html', form=form)

@app.route('/success')
def success():
    filename = request.args.get('filename')
    if not filename:
        flash("No pattern file specified. Please generate a new pattern.")
        return redirect(url_for('index'))
    
    # Check if the file exists
    pdf_path = os.path.join(app.static_folder, 'patterns', filename)
    if not os.path.exists(pdf_path):
        flash("PDF file not found. Please generate a new pattern.")
        return redirect(url_for('index'))
    
    return render_template('success.html', pdf_basename=filename)
    
@app.route('/download/<filename>')
def download_pdf(filename):
    # Ensure the file exists in the patterns directory
    pdf_path = os.path.join(app.static_folder, 'patterns', filename)
    if not os.path.exists(pdf_path):
        flash("PDF file not found. Please generate a new pattern.")
        return redirect(url_for('index'))
        
    # Return the file as an attachment for download
    return send_file(pdf_path, 
                     mimetype='application/pdf',
                     as_attachment=True,
                     download_name=filename)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
