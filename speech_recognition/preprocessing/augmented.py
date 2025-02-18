import os
import numpy as np
import librosa
import librosa.display
import soundfile as sf
import random

# Paths
INPUT_DIR = "speech_recognition/preprocessing/output_silence_removal"
OUTPUT_DIR = "speech_recognition/preprocessing/output_augmented"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Sampling rate for consistency
sr_target = 16000  

# Augmentation parameters
PITCH_SHIFT_RANGE = (-2, 2)  # Range of pitch shifting
TIME_STRETCH_RANGE = (0.9, 1.1)  # Speed variation range
NOISE_LEVEL = 0.005  # Noise variance
SHIFT_MAX_SEC = 0.1  # Maximum shift in seconds
VOLUME_CHANGE_RANGE = (0.5, 1.5)  # Amplitude scaling

def add_noise(y):
    """Adds Gaussian noise to the signal."""
    noise = np.random.normal(0, NOISE_LEVEL, y.shape)
    return y + noise

def time_stretch(y):
    """Randomly speeds up or slows down the audio."""
    rate = random.uniform(*TIME_STRETCH_RANGE)
    return librosa.effects.time_stretch(y, rate)

def pitch_shift(y, sr):
    """Shifts pitch randomly within the defined range."""
    n_steps = random.randint(*PITCH_SHIFT_RANGE)
    return librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)

def volume_perturbation(y):
    """Changes volume randomly within the defined range."""
    factor = random.uniform(*VOLUME_CHANGE_RANGE)
    return y * factor

def time_shift(y, sr):
    """Shifts audio in time by a random amount."""
    shift = int(random.uniform(0, SHIFT_MAX_SEC) * sr)
    return np.roll(y, shift)

# Process each file
print("Starting data augmentation...")

for root, dirs, files in os.walk(INPUT_DIR):
    for file in files:
        if file.lower().endswith(".wav"):
            input_path = os.path.join(root, file)
            print(f"Processing: {input_path}")
            
            try:
                # Load audio
                y, sr = librosa.load(input_path, sr=sr_target)

                # Choose 1-2 augmentations randomly
                augmentations = random.sample(
                    [add_noise, time_stretch, pitch_shift, volume_perturbation, time_shift], 
                    k=random.randint(1, 2)
                )

                # Apply augmentations
                for aug in augmentations:
                    y = aug(y) if aug != pitch_shift else aug(y, sr)  # Handle pitch_shift separately

                # Prepare output path
                output_path = os.path.join(OUTPUT_DIR, f"aug_{file}")

                # Save the augmented file
                sf.write(output_path, y, sr)
                print(f"Saved augmented file: {output_path}\n")

            except Exception as e:
                print(f"Error processing {input_path}: {e}")

print("Data augmentation completed.")
