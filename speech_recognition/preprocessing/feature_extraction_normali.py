import os
import glob
import numpy as np
import librosa
from sklearn.preprocessing import StandardScaler
from joblib import Parallel, delayed, dump

# Directories:
# Input directory contains augmented audio files.
# Output directory will store the normalized feature arrays and scalers.
input_audio_dir = "/home/user/Desktop/voice-to-text/speech_recognition/preprocessing/output_augmented"
output_feature_dir = "/home/user/Desktop/voice-to-text/speech_recognition/preprocessing/output_feature_normalise"
os.makedirs(output_feature_dir, exist_ok=True)

# Parameters for feature extraction
n_mfcc = 13  # Number of MFCCs to extract

def process_audio_file(audio_file):
    try:
        # Load audio file with its native sampling rate.
        audio, sr = librosa.load(audio_file, sr=None)
        
        # Set n_fft based on signal length
        if len(audio) < 2048:
            n_fft = len(audio)  # Use the signal length as n_fft for very short signals
        else:
            n_fft = 2048
        
        # Extract MFCC features using the adjusted n_fft
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft)
        # mfcc shape is (n_mfcc, number_of_frames)
        
        # Normalize features using StandardScaler.
        # Transpose so each frame becomes an observation with n_mfcc features,
        # then scale and transpose back.
        scaler = StandardScaler()
        mfcc_norm = scaler.fit_transform(mfcc.T).T
        
        # Define base name and paths for saving features and the scaler.
        base_name = os.path.splitext(os.path.basename(audio_file))[0]
        feature_file = os.path.join(output_feature_dir, base_name + ".npy")
        scaler_file = os.path.join(output_feature_dir, base_name + "_scaler.pkl")
        
        # Save the normalized features as a NumPy array.
        np.save(feature_file, mfcc_norm)
        
        # Save the scaler using joblib.
        dump(scaler, scaler_file)
        
        print(f"Processed and saved features and scaler for {base_name}")
    except Exception as e:
        print(f"Error processing {audio_file}: {e}")

# Get list of all WAV files in the input directory.
audio_files = glob.glob(os.path.join(input_audio_dir, "*.wav"))
print(f"Found {len(audio_files)} audio files for feature extraction.")

# Process files in parallel using all available cores.
Parallel(n_jobs=-1)(delayed(process_audio_file)(audio_file) for audio_file in audio_files)

print("Feature extraction and normalization complete.")
