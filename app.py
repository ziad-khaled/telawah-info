import os

from flask import Flask, render_template, flash
from flask import request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect, secure_filename

from predict import get_speaker_id, get_audio_transcript
from utils import to_wav

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'flac, wav, aac, m4a, mp3, ogg'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reciters.db'
db = SQLAlchemy(app)


class Reciter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    arabic_name = db.Column(db.String(80), unique=True, nullable=False)
    english_name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Reciter %r>' % self.english_name


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        if 'audio_file' not in request.files:
            return render_template("result.html", result=None)

        audio_file = request.files['audio_file']
        if audio_file.filename == '':
            return render_template("result.html", result=None)

        if audio_file and allowed_file(audio_file.filename):
            filename = secure_filename(audio_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio_file.save(file_path)
            to_wav(file_path)
            file_path = file_path + '.wav'
            speaker_id = get_speaker_id(file_path)
            reciter_name = Reciter.arabic_name
            audio_transcript = get_audio_transcript(file_path)
            result = {"reciter_name": reciter_name, "audio_transcript": audio_transcript}
            return render_template("result.html", result=result)
