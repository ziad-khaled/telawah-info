import numpy as np
from sklearn.mixture import GaussianMixture
from pathlib import Path
from scipy.io import wavfile
from joblib import dump
from utils import extract_features


def enroll_speaker():
    speaker_files_path = input('speaker audio files path: ')

    speaker_dir = Path(speaker_files_path)
    speaker_name = speaker_dir.name

    audio_files_paths = list(speaker_dir.glob('*.wav'))
    print('speaker audio files: ')
    i = 1
    for file in audio_files_paths:
        print('\t' + i.__str__() + '. ' + file.name + '\n')
    
    speaker_gmm = GaussianMixture(32)

    features = []
    for file_path in audio_files_paths:
        print('extracting data from ' + file_path.name + '\n')
        sample_rate, signal_data = wavfile.read(file_path)
        file_features = extract_features(sample_rate, signal_data)
        features.extend(file_features)

    speaker_gmm.fit(features)
    dump(speaker_gmm, speaker_name + '.gmm')
    print('file dumped\n')


if __name__ == '__main__':
    enroll_speaker()
