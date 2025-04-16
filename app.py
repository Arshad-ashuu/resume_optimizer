# FLASK APP - Run the app using flask --app app.py run
from flask import Flask, render_template, request, session, send_file
from flask_session import Session
import pdfkit
import os, sys
from pypdf import PdfReader 
import json
from resumeparser import ats_extractor




sys.path.insert(0, os.path.abspath(os.getcwd()))


UPLOAD_PATH = r"__DATA__"
app = Flask(__name__)

app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    return render_template('index.html')



@app.route("/process", methods=["POST"])
def ats():
    doc = request.files['pdf_doc']
    doc.save(os.path.join(UPLOAD_PATH, "file.pdf"))
    doc_path = os.path.join(UPLOAD_PATH, "file.pdf")
    data = _read_file_from_path(doc_path)
    data = ats_extractor(data)

    return render_template('index.html', data=data)

 
def _read_file_from_path(path):
    reader = PdfReader(path) 
    data = ""

    for page_no in range(len(reader.pages)):
        page = reader.pages[page_no] 
        data += page.extract_text()

    return data 




@app.route('/resume', methods=['GET', 'POST'])
def resume():
    if request.method == 'POST':
        session['resume'] = request.form.to_dict()
        return render_template('preview.html', data=session['resume'])
    return render_template('resume.html')

@app.route('/save', methods=['POST'])
def save_resume():
    session['resume'] = request.form.to_dict()
    return 'Saved'

@app.route('/export_pdf')
def export_pdf():
    rendered = render_template('preview.html', data=session.get('resume', {}))
    pdf_path = "/mnt/data/resume.pdf"
    pdfkit.from_string(rendered, pdf_path)
    return send_file(pdf_path, as_attachment=True)



# if __name__ == "__main__":
#     app.run(port=8000, debug=True)







