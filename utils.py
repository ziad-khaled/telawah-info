import os

from python_speech_features import delta
from python_speech_features import mfcc
import numpy as np
from pathlib import Path
from joblib import load


def extract_features(sample_rate, signal_data):
    mfcc_features = mfcc(signal_data, sample_rate, numcep=20)
    delta_mfcc = delta(mfcc_features, 2)
    combined_features = np.hstack((mfcc_features, delta_mfcc))
    return combined_features


def load_speakers():
    speakers_dir = Path('./speakers_models')
    speakers_gmms_paths = speakers_dir.glob('*.gmm')

    speakers_names = list()
    speakers_gmms = list()
    for gmm_path in speakers_gmms_paths:
        speaker_gmm = load(gmm_path)
        speaker_name = gmm_path.name.split('.')[0]

        speakers_gmms.append(speaker_gmm)
        speakers_names.append(speaker_name)

    return speakers_names, speakers_gmms


def to_wav(audio_file_path):
    # ffmpeg here
    os.system("ffmpeg -i " + audio_file_path + " -acodec pcm_s16le -ac 1 -ar 16000 " + audio_file_path + ".wav")
