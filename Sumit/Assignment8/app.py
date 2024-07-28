from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
import subprocess

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
CAPTURE_FOLDER = 'captures'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CAPTURE_FOLDER'] = CAPTURE_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CAPTURE_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Capture packets using tshark
            capture_file = os.path.join(app.config['CAPTURE_FOLDER'], f'{filename}.pcap')
            capture_packets(capture_file)
            
            file_url = url_for('send_file', filename=filename)
            capture_url = url_for('send_capture', filename=f'{filename}.pcap')
            
            return f'File saved as {filename}. <a href="{file_url}">Download it here</a>. <a href="{capture_url}">Download capture file</a>.'
    return redirect(url_for('index'))

def capture_packets(output_file):
    # Run tshark to capture packets for a specified duration (e.g., 10 seconds)
    command = ['tshark', '-a', 'duration:10', '-w', output_file]
    subprocess.run(command)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/captures/<filename>')
def send_capture(filename):
    return send_from_directory(app.config['CAPTURE_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
