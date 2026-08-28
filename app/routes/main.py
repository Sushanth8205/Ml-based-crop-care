from flask import Blueprint, render_template, session, redirect, url_for, request
from app.models.user import User
from app.models.appointment import Appointment
from app.models.detection import Detection

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', active_tab=None)

@main_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_data = User.get_by_id(session['user_id'])
    if not user_data:
        session.clear()
        return redirect(url_for('auth.login'))

    role = session.get('role', 'user')
    active_tab = request.args.get('tab', 'home')
    appointments = []
    history = []

    if role == 'user':
        appointments = Appointment.get_farmer_appointments(session['user_id'])
        for appt in appointments:
            advisor = User.get_by_id(appt['advisor_id'])
            appt['advisor_name'] = advisor['name'] if advisor else 'Unknown'
        history = Detection.get_user_history(session['user_id'])

    elif role == 'advisor':
        appointments = Appointment.get_advisor_appointments(session['user_id'])
        for appt in appointments:
            farmer = User.get_by_id(appt['farmer_id'])
            appt['farmer_name'] = farmer['name'] if farmer else 'Unknown'

    return render_template(
        'dashboard.html',
        user=user_data,
        role=role,
        active_tab=active_tab,
        appointments=appointments,
        history=history
    )
