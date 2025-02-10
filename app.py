import qrcode
import random
import string
from flask import Flask, render_template, request, session, jsonify, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For session management

# Dummy storage
attendance_records = {}  # {student_id: {'date': '2024-09-30', 'device': 'IP/MAC'}}
current_qr = ""

# Define classroom GPS location
CLASSROOM_LAT, CLASSROOM_LON = 12.9716, 77.5946  # Example coordinates
GEO_TOLERANCE = 0.0005  # Acceptable deviation

def generate_random_code(length=6):
    """Generate a random alphanumeric QR code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route('/')
def home():
    """Render the main page with the QR code."""
    return render_template('index.html')

@app.route('/generate_qr')
def generate_qr():
    global current_qr
    current_qr = generate_random_code()

    qr = qrcode.make(f"{url_for('mark_attendance', token=current_qr, _external=True)}")
    qr_path = "static/qrs/qr_code.png"
    qr.save(qr_path)

    return jsonify({'qr_url': qr_path})

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    token = request.args.get("token")
    print(token, 'Heeeey')
    """Verify location & allow only one device per student per day."""
    data = request.json
    student_id = data.get('student_id')
    scanned_qr = data.get('qr_code')
    lat, lon = data.get('latitude'), data.get('longitude')
    user_device = request.remote_addr  # Get student's IP (for device tracking)
    today = datetime.today().strftime('%Y-%m-%d')

    # Verify QR Code
    if scanned_qr != current_qr:
        return jsonify({'error': 'Invalid QR Code!'}), 400

    # Verify Location
    if abs(lat - CLASSROOM_LAT) > GEO_TOLERANCE or abs(lon - CLASSROOM_LON) > GEO_TOLERANCE:
        return jsonify({'error': 'You are not in class!'}), 403

    # Check if student has already marked attendance today
    if student_id in attendance_records:
        record = attendance_records[student_id]
        if record['date'] == today:
            return jsonify({'error': 'Attendance already marked from another device!'}), 403

    # Mark attendance
    attendance_records[student_id] = {'date': today, 'device': user_device}
    return jsonify({'message': 'Attendance marked successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=1008, host='0.0.0.0')
