import os
from flask import Blueprint, request, render_template, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from app.models.detection import Detection
from app.ml.inference import predict_disease

detection_bp = Blueprint('detection', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@detection_bp.route('/detect', methods=['GET', 'POST'])
def detect():
    # Only logged-in users (or we can allow guests, but requirement says "registered user")
    if 'user_id' not in session:
        flash('Please login to detect crop diseases.', 'error')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No image part', 'error')
            return redirect(request.url)
            
        file = request.files['image']
        if file.filename == '':
            flash('No selected image', 'error')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Create a unique filename based on time
            import time
            unique_filename = f"{int(time.time())}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # Predict
            crop, disease, confidence = predict_disease(filepath)
            
            # Save detection history
            relative_path = f"uploads/{unique_filename}"
            detection_id = Detection.save_detection(
                session['user_id'], 
                crop, 
                disease, 
                confidence, 
                relative_path
            )
            
            return redirect(url_for('detection.result', detection_id=detection_id))
            
    return render_template('detection.html')

@detection_bp.route('/result/<detection_id>')
def result(detection_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    detection_record = Detection.get_detection(detection_id)
    if not detection_record or str(detection_record.get('user_id')) != session['user_id']:
        flash('Result not found or unauthorized access.', 'error')
        return redirect(url_for('main.dashboard'))
        
    return render_template('result.html', detection=detection_record)
