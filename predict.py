from utils import load_speakers
from utils import extract_features
from scipy.io import wavfile
import numpy as np
import speech_recognition as sr


def get_speaker_id(audio_file_path):
    speakers_ids, speakers_gmms = load_speakers()
    sample_rate, signal_data = wavfile.read(audio_file_path)
    features = extract_features(sample_rate, signal_data)

    speakers_scores = np.empty(len(speakers_gmms))
    for i in range(len(speakers_gmms)):
        speaker_gmm = speakers_gmms[i]
        speaker_score = np.sum(speaker_gmm.score(features))
        speakers_scores[i] = speaker_score

    best_candidate_index = np.argmax(speakers_scores)
    speaker_id = speakers_ids[best_candidate_index]
    return speaker_id


def get_audio_transcript(audio_file_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = r.record(source)

    audio_transcript = ""
    try:
        audio_transcript = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    return audio_transcript


